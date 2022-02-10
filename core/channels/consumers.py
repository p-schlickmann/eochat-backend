import json

from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import DenyConnection

from core.models import Message, Chat
from core.serializers import MessageSerializer


def enforce_authentication_and_return_user(query_from_scope):
    User = get_user_model()
    _, token = query_from_scope.decode('utf-8').split('=')
    try:
        return User.objects.get(auth_token=token)
    except User.DoesNotExist:
        raise DenyConnection()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        try:
            self.chat_code = self.scope['url_route']['kwargs']['chat_code']
            self.chat_code_int = int(self.chat_code)
        except (ValueError, KeyError):
            raise DenyConnection()
        enforce_authentication_and_return_user(self.scope['query_string'])
        try:
            self.chat_obj = Chat.objects.get(code=self.chat_code_int)
        except Chat.DoesNotExist:
            raise DenyConnection()
        # Join chat
        async_to_sync(self.channel_layer.group_add)(
            self.chat_code,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_code,
            self.channel_name
        )

    def fetch_messages(self, data):
        page = int(data['page'])
        page_size = 50
        limit = page_size * page
        offset = 0 if page == 1 else page_size * page - 1
        messages = Message.objects.select_related('author').filter(
            chat__code=self.chat_code_int
        ).order_by('id')[offset-1 if offset > 0 else offset:limit]
        self.send(
            text_data=json.dumps({
                'type': 'fetch_messages',
                'chat_name': self.chat_obj.name,
                'messages': MessageSerializer(messages, many=True).data
            })
        )

    def send_message(self, data):
        try:
            msg = Message.objects.create(author_id=data['user'], chat=self.chat_obj, content=data['content'])
        except Exception as error:
            print(error)
            self.close()
            return
        async_to_sync(self.channel_layer.group_send)(
            self.chat_code,
            {
                'type': 'chat_message',
                'message_id': str(msg.id)
            }
        )

    websocket_types = {
        'fetch_messages': fetch_messages,
        'send_message': send_message,
    }

    # Receive message from room group
    def chat_message(self, event):
        try:
            message_obj = Message.objects.select_related('author').get(id=int(event['message_id']))
        except Exception as error:
            print(error)
            return
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': {
                'author': message_obj.author.username,
                'content': message_obj.content,
                'created_at': message_obj.created_at.isoformat(),
            }
        }))

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        # Send message to room group
        user = enforce_authentication_and_return_user(self.scope['query_string'])
        data = json.loads(text_data)
        data['user'] = user.id
        self.websocket_types[data['type']](self, data)


