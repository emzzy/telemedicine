from rest_framework import serializers
from .models import Message, Conversation
from users import models as user_models
from shared import serializers as user_serializers


class USerSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.UserAccount
        fields = ('id', 'first_name', 'password')
    
        def create(self, validated_data):
            user = user_models.UserAccount.objects.create(**validated_data)
            return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.UserAccount
        fields = ('id', 'first_name')

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserListSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'participants', 'created_at')

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            return representation

class MessageSerializer(serializers.ModelSerializer):
    sender = UserListSerializer()
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('id', 'conversation', 'sender', 'content', 'timestamp', 'participants')

        def get_participants(self, obj):
            return UserListSerializer(obj.conversation.participants.all(), many=True).data

class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('conversation', 'content')