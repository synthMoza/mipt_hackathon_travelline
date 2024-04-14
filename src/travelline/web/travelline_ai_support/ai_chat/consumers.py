import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from travelline.backend.llm.gigachat_module import GigaDetailizer
from travelline.backend.llm.gigachat_module import GigaThought
from travelline.backend.rag.sbertembedding import SBertEmbedding
from travelline.backend.database.query_from_database import load_tensors
from travelline.backend.database.query_from_database import EMBEDDING_DIR
from travelline.backend.database.query_from_database import NUMBER_OF_SIMILAR_FILES
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import torch
import json
from pathlib import Path
import os

repo_root = Path(__file__).parent.parent.parent.parent.parent.parent

with open(repo_root / "config.json", "r") as f:
    args = json.load(f)
embedding_creator = SBertEmbedding()
deep_thought = GigaThought(args["credentials"], args["thought_config"])
deep_detailizer = GigaDetailizer(args["credentials"], args["detailizer_config"])

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
            real_question = deep_detailizer.detailize(message)
            real_question_embedding = torch.nn.functional.normalize(embedding_creator.get(real_question))

            (tensor_list, dict_with_indexes) = load_tensors(EMBEDDING_DIR)
            tensors = np.vstack(tensor_list)
            query_similarities = cosine_similarity([real_question_embedding[0]], tensors)[0]

            similarity_list = []
            for index in range(len(dict_with_indexes)):
                similarity_list.append((dict_with_indexes[index], query_similarities[index]))

            similarity_list.sort(key=lambda x: x[1], reverse=True)
            print(f"Similarity list = {similarity_list}")
            tmp_num = NUMBER_OF_SIMILAR_FILES
            print(f"Top {tmp_num} similar files: {[x[0] for x in similarity_list[:tmp_num]]}")
            print("********************")

            best_number = similarity_list[0]

            docs_path = repo_root / "src" / "travelline" / "backend" / "database" / "docs_txt"
            best_doc_filename = f"#{best_number[0]}#"
            for file in os.listdir(docs_path):
                if file.startswith(best_doc_filename):
                    best_file_path = docs_path / file
            with open(best_file_path) as f:
                doc_contents = f.read()
            best_doc_filename = f"#{best_number}#"

            answer = deep_thought.ask(real_question, doc_contents)
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
