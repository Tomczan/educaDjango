import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'chat_%s' % self.id
        # dolaczenie do grupy pokoju
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # akceptacja połączenia
        await self.accept()

    async def disconnect(self, code):
        # opusc grupe pokoju rozmow
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # wysłanie komunikatu do websocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    # odebranie wiadomosci z grupy pokoju rozmow
    async def chat_message(self, event):
        # wyslanie komunikatu do WebSocket
        await self.send(text_data=json.dumps(event))
