import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from travelline.backend.llm.gigachat_module import GigaDetailizer
from travelline.backend.llm.gigachat_module import GigaActualizer
from travelline.backend.llm.gigachat_module import GigaThought
from travelline.backend.database.database_implementation import EmbeddingsDB
from travelline.backend.database.database_searcher_implementation import DB_Searcher
import json
import os
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent.parent.parent

with open(repo_root / "config.json", "r") as f:
    args = json.load(f)
thought_config = repo_root / "src" / "travelline" / "backend" / "llm" / "gigathought.yaml"
detailizer_config = repo_root / "src" / "travelline" / "backend" / "llm" / "gigadetailizer.yaml"
actualizer_config = repo_root / "src" / "travelline" / "backend" / "llm" / "gigaactualizer.yaml"

deep_thought = GigaThought(args["credentials"], thought_config)
deep_detailizer = GigaDetailizer(args["credentials"], detailizer_config)
deep_actualizer = GigaActualizer(args["credentials"], actualizer_config)

embeddings_db = EmbeddingsDB(repo_root / "data" / "embeddings.db")
embeddings_db.fill((repo_root / "src" / "travelline" / "backend" / "database" / "docs_txt").glob("**/*"))
searcher = DB_Searcher(embeddings_db)


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
            await asyncio.sleep(0.5)

            chat_history: str = ""

            # actualized_answer = int(deep_actualizer.actualize(message))
            # print("Actualizer response: ", actualized_answer)

            # if actualized_answer == 0:
            #     answer = "Вопрос не относится к теме, попробуйте переформулировать свой вопрос"
            # else:
            real_question, chat_history = deep_detailizer.detailize(message, chat_history)
            searcher.ask_real_question(real_question)
            similarity_list = searcher.get_full_simularity_list()
            reduced_similarity_list = searcher.get_reduced_simularity_list(5)
            print("Full simularity list:")
            print(similarity_list)
            print("Reduced simularity list:")
            print(reduced_similarity_list)
            best_doc_contents = embeddings_db.get_plain_text(similarity_list[0][0])
            answer = deep_thought.ask(real_question, best_doc_contents)

            await self.send(
                text_data=json.dumps(
                    {
                        "message": answer,
                        "username": "Travelline AI Supporter",
                        "from_ai": True,
                    }
                )
            )

    pass
