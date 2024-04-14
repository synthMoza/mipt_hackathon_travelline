import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from travelline.backend.rag.sbertembedding import SBertEmbedding
from travelline.backend.rag.demoapp import parse_args as parse_embedding_args


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

    # Receive message from room group.
    async def chatbox_message(self, event):
        message = event["message"]
        username = event["username"]
        from_ai = event["from_ai"]

        args = parse_embedding_args()
        embedding = SBertEmbedding()
        import code; code.interact(local={**locals(), **globals()})

        # send message and username of sender to websocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                    "from_ai": from_ai,
                }
            )
        )
        if not from_ai:
            await asyncio.sleep(0.5)
            await self.send(
                text_data=json.dumps(
                    {
                        "message": "message",
                        "username": "Travelline AI Supporter",
                        "from_ai": True,
                    }
                )
            )

    pass
