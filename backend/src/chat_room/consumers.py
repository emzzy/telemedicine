import json
from users.models import UserAccount
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message']
            user_email = data['email']
            room = data['room']

            if user_email != self.scope['user'].email:
                return

            await self.save_message(user_email, room, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user_email': user_email,
                    'user_name': f'{self.scope['user'].first_name} {self.scope['user'].last_name}',
                    'timestamp': str(timezone.now())
                }
            )
        except json.JSONDecodeError:
            pass

    # Receive message from room group
    async def chat_message(self, event):
        # message = event['message']
        # user_email = event['user_email']
        # user_name = event['user_name']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user_email': event['user_email'],
            'user_name': event['user_name'],
            'timestamp': event.get('timestamp', '')
        }))

    @database_sync_to_async
    def save_message(self, user_email, room, message):
        try:
            user = UserAccount.objects.get(email=user_email)
            room_obj = ChatRoom.objects.get(slug=room)
            Message.objects.create(user=user, room=room_obj, content=message)

        except (UserAccount.DoesNotExist, ChatRoom.DoesNotExist):
            pass