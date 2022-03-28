import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # akceptacja połączenia
        self.accept()

    def disconnect(self, code):
        return super().disconnect(code)

    # odbiór komunikatu z WebSocket
    def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # wysłanie komunikatu do websocket
        self.send(text_data=json.dumps({'message': message}))
