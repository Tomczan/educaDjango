import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'chat_%s' % self.id
        # dolaczenie do grupy pokoju
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # akceptacja połączenia
        self.accept()

    def disconnect(self, code):
        # opusc grupe pokoju rozmow
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        return super().disconnect(code)

    def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # wysłanie komunikatu do websocket
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    # odebranie wiadomosci z grupy pokoju rozmow
    def chat_message(self, event):
        # wyslanie komunikatu do WebSocket
        self.send(text_data=json.dumps(event))