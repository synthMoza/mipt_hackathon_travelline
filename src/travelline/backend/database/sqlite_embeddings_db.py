from travelline.backend.database.abstract_embeddings_db import AbstractEmbeddingsDB
from torch import Tensor

import sqlite3

class SQLiteEmbeddingsDB(AbstractEmbeddingsDB):
    def __init__(self, db_file):
        self.db_file = db_file
        with sqlite3.connect(self.db_file) as con:
            cursor = con.cursor()
            cursor.execute("PRAGMA foreign_keys = 1")
            cursor.execute("CREATE TABLE IF NOT EXISTS documents(id INT PRIMARY KEY, doc TEXT);")
            cursor.execute("CREATE TABLE IF NOT EXISTS embeddings(id INT PRIMARY KEY, doc_id INTEGER, embedding BLOB, FOREIGN KEY (doc_id) REFERENCES documents(id));")

    def add_document(file_name: str) -> int:
        pass
    def get_document(id: int) -> str:
        pass
    def get_document_embedding(id: int) -> Tensor:
        pass