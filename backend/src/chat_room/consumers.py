import json
# from users.models import UserAccount
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import jwt
from django.utils import timezone
from django.conf import settings
from urllib.parse import parse_qs


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'

#         if self.scope['user'].is_anonymous:
#             await self.close()
#         else:
#             await self.channel_layer.group_add(
#                 self.room_group_name,
#                 self.channel_name
#             )
#             await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         try:
#             data = json.loads(text_data)
#             message = data['message']
#             user_email = data['email']
#             room = data['room']

#             if user_email != self.scope['user'].email:
#                 return

#             await self.save_message(user_email, room, message)

#             # Send message to room group
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'chat_message',
#                     'message': message,
#                     'user_email': user_email,
#                     'user_name': f'{self.scope['user'].first_name} {self.scope['user'].last_name}',
#                     'timestamp': str(timezone.now())
#                 }
#             )
#         except json.JSONDecodeError:
#             pass

#     # Receive message from room group
#     async def chat_message(self, event):
#         # message = event['message']
#         # user_email = event['user_email']
#         # user_name = event['user_name']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'user_email': event['user_email'],
#             'user_name': event['user_name'],
#             'timestamp': event.get('timestamp', '')
#         }))

#     @database_sync_to_async
#     def save_message(self, user_email, room, message):
#         try:
#             user = UserAccount.objects.get(email=user_email)
#             room_obj = ChatRoom.objects.get(slug=room)
#             Message.objects.create(user=user, room=room_obj, content=message)

#         except (UserAccount.DoesNotExist, ChatRoom.DoesNotExist):
#             pass

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        #User = get_user-model()
        query_string = self.scope['query_string'].decode('utf-8')
        params = parse_qs(query_string)
        token = params.get('token', [None])[0] # retrieve token

        if token:
            try:
                decode_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                self.user = await self.get_user(decode_data['user_id']) # get the user from token
                self.scope['user'] = self.user
            except jwt.ExpiredSignatureError:
                await self.close(code=4000) # close connection if token is expired
            except jwt.InvalidTokenError:
                await self.close(code=4001) # close the connection if token is invalid
                return
        else:
            await self.close(code=4002) # close the connection if no token is provided
            return
        
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        # Add channel to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        user_data = await self.get_user_data(self.User)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_status',
                'online_users': [user_data],
                'status': 'online',
            }
        )

    async def disconnect(self, code):
        if hasattr(self, 'room_group_name'):
            # Notify other users about disconnect
            user_data = await self.get_user_data(self.scope['user'])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'online_status',
                    'online_users': [user_data],
                    'status': 'offline',
                }
            )

            # Remove channel from the group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        event_type = text_data_json.get('type')
        
        if event_type == 'chat_message':
            message_content = text_data_json.get('message')
            user_id = text_data_json.get('user')

            try:
                from .serializers import UserListSerializer

                user = await self.get_user(user_id)
                conversation = await self.get_conversation(self.conversation_id)
                user_data = UserListSerializer(user).data

                # Save message to the group or Database
                message = await self.save_message(conversation, user, message_content)
                
                # Broadcast the message to the group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message.content,
                        'user': user_data,
                        'timestamp': message.timestamp.isoformat(),
                    }
                )
            except Exception as e:
                print(f'Error: {e}')
        
        if event_type == 'typing':
            try:
                user_data = await self.get_user_data(self.scope['user'])
                receiver_id = text_data_json.get('receiver_id')

                if receiver_id is not None:
                    if isinstance(receiver_id, (str, int, float)):
                        receiver_id = int(receiver_id)

                        if receiver_id != self.scope['user'].id:
                            print(f'{user_id['username']} is typing for Receiver: {receiver_id}')
                            await self.channel_layer.group_send(
                                self.room_group_name,
                                {
                                    'type': 'typing',
                                    'user': user_data,
                                    'receiver_id': receiver_id,
                                }
                            )
                        else:
                            print(f'{user_id['first_name']} is typing for themselves')
                    else:
                        print(f'Invalid receiver ID: {type(receiver_id)}')
                else:
                    print('No receiver ID provided')
            except ValueError as e:
                print(f'Error parsing receiver ID: {e}')
            except Exception as e:
                print(f'Error getting user data: {e}')
    
    # Helper functions
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        timestamp = event['timestamp']
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'user': user,
            'timestamp': timestamp
        }))

    async def typing(self, event):
        user = event['user']
        receiver = event.get('receiver_id')
        is_typing = event.get('is_typing', False)
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': user,
            'receiver': receiver,
            'is_typing': is_typing
        }))

    async def online_status(self, event):
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_user_model(self):
        from django.contrib.auth import get_user_model
        return get_user_model()

    @sync_to_async
    def get_user(self, user_id):
        from users.models import UserAccount
        return UserAccount.objects.get(id=user_id)
    
    @sync_to_async
    def get_user_data(self, user):
        from .serializers import UserListSerializer

        return UserListSerializer(user).data
    
    @sync_to_async
    def get_conversation(self, conversation_id):
        from .models import Conversation
        try:
            return Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            print(f'Conversation qith id {conversation_id} does not exist')
            return None
    
    @sync_to_async
    def save_message(self, conversation, user, content):
        from .models import Message
        message = Message.objects.create(
            conversation=conversation,
            sender=user,
            content=content
        )
        return message