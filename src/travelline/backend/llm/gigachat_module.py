from deepthought import AbstractDeepThought, AbstractDetailizer
from langchain.chat_models.gigachat import GigaChat
from langchain.prompts import load_prompt
from typing import Tuple


class GigaThought(AbstractDeepThought):
    def __init__(self, credentials, config_file_path):
        self.chat = GigaChat(credentials=credentials, verify_ssl_certs=False)
        self.prompt = load_prompt(config_file_path)
        self.chain = self.prompt | self.chat

    def ask(self, input_question: str, document: str) -> str:
        message = self.chain.invoke({"input_question": input_question, "context": document})
        return message.content
    
class GigaDetailizer(AbstractDetailizer):
    def __init__(self, credentials, config_file_path):
        self.chat = GigaChat(credentials=credentials, verify_ssl_certs=False)
        self.prompt = load_prompt(config_file_path)
        self.chain = self.prompt | self.chat
    def detailize(self, question: str, chat_history: str) -> Tuple[str, str]:
        message = self.chain.invoke({"question": question, "chat_history": chat_history})
        chat_history += f'Пользователь: "{question}"\n'
        chat_history += f'Система: "{message.content}"\n'
        return (message.content, chat_history)
