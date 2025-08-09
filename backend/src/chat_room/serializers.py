from rest_framework import serializers
from .models import ChatRoom, Message
from users import models as user_models
from shared import serializers as user_serializers


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'slug']

class MessageSerializer(serializers.ModelSerializer):
    user = user_serializers.UserAccountSerializer
    
    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'date_added']