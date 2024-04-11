import json
import time
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_box_name = self.scope["url_route"]["kwargs"]["chat_box_name"]
        self.group_name = "chat_%s" % self.chat_box_name

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

        await self.channel_layer.group_send(
            self.group_name,
            {
                "from_ai": True,
                "type": "chatbox_message",
                "message": "Welcome to Travelline AI Support Service. Please, ask your question!",
                "username": "Travelline AI Supporter",
            },
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    # This function receive messages from WebSocket.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        await self.channel_layer.group_send(
            self.group_name,
            {
                "from_ai": False,
                "type": "chatbox_message",
                "message": message,
                "username": username,
            },
        )

        await self.channel_layer.group_send(
            self.group_name,
            {
                "from_ai": True,
                "type": "chatbox_message",
                "message": "Ты лох",
                "username": "Travelline AI Supporter",
            },
        )
    # Receive message from room group.
    async def chatbox_message(self, event):
        message = event["message"]
        username = event["username"]
        from_ai = event["from_ai"]
        #send message and username of sender to websocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                    "from_ai": from_ai,
                }
            )
        )

    pass