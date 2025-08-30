from django.db import models
from users.models import UserAccount
from django.db.models import Prefetch

from django_cryptography.fields import encrypt


class ConversationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch('participants', queryset=UserAccount.objects.only('id', 'email'))
        )
    
class Conversation(models.Model):
    participants = models.ManyToManyField(UserAccount, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ConversationManager()

    def __str__(self):
        participants_names = ' ,'.join([user.email for user in self.participants.all()])
        return f'Conversation with {participants_names}'
    
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    sender = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    content = encrypt(models.TextField())
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.first_name} in {self.content[:20]}'
    
