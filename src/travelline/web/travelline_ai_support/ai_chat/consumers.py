import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from travelline.backend.llm.demoapp import parse_args
from travelline.backend.llm.gigachat_module import GigaDetailizer
from travelline.backend.rag.sbertembedding import SBertEmbedding
import torch

args = parse_args()
embedding_creator = SBertEmbedding()
deep_detailizer = GigaDetailizer(args.credentials, args.detailizer_config)

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

        real_question = deep_detailizer.detailize(message)
        real_question_embedding = torch.nn.functional.normalize(embedding_creator.get(real_question))
        import code; code.interact(local={**locals(), **globals()})

        # send message and username of sender to websocket
        if username == "":
            username = "Guest"

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
            await asyncio.sleep(2.5)
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
