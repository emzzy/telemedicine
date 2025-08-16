from django.contrib import admin
from .models import ChatRoom, Conversation, Message

# admin.site.register(ChatRoom)
admin.site.register(Conversation)
admin.site.register(Message)