
from travelline.backend.rag.sbertembedding import SBertEmbedding
from pathlib import Path

import sqlite3
import torch
import pickle

class EmbeddingsDB():
    def __init__(self, db_path : str) -> None:

        self.embedding = SBertEmbedding()
        self.db_path = Path(db_path).absolute()

        if not self.db_path.exists():
            print(f"{self.db_path.as_posix()} does not exist! Exiting!")
            exit(-1)

        self.connection = sqlite3.connect(self.db_path.as_posix())
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tensors
             (id INTEGER PRIMARY KEY, doc_name TEXT, datetime TEXT, plain_text TEXT, tensor BLOB)''')

    #PUBLIC API

    def add_document(self, doc_name : str, datetime : str, plain_text : str) -> None:

        tensor = torch.nn.functional.normalize(self.embedding.get(plain_text))
        tensor_blob = pickle.dumps(tensor)
        id = int(self._crop_filename(doc_name))
        if self.check_if_document_exists(id):
            return
        self.cursor.execute("INSERT INTO tensors (id, doc_name, datetime, plain_text, tensor) VALUES (?,?,?,?,?)",
                             (id, doc_name, datetime, plain_text, sqlite3.Binary(tensor_blob),))
        self.connection.commit()

    def update_document(self, doc_name : str, datetime : str, plain_text : str) -> None:

        tensor : torch.Tensor = torch.nn.functional.normalize(self.embedding.get(plain_text))
        tensor_blob = pickle.dumps(tensor)
        id = self._crop_filename(doc_name)
        self.cursor.execute("UPDATE tensors SET doc_name=?, datetime=?, plain_text=?, tensor=? WHERE id=?",
                             (doc_name, datetime, plain_text, sqlite3.Binary(tensor_blob), id))
        self.connection.commit()

    def delete_document(self, id : int) -> None:
        self.cursor.execute("DELETE FROM tensors WHERE id=?", (id,))
        self.connection.commit()


    def check_if_document_exists(self, id : int):
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM tensors WHERE id=?)", (id,))
        row = self.cursor.fetchone()
        if (row[0]):
            return True
        else:
            return False


    def get_date_time(self, id: int) -> str:
        self.cursor.execute("SELECT datetime FROM tensors WHERE id=?", (id,))
        row = self.cursor.fetchone()
        return row[0]

    def get_doc_name(self, id: int) -> str:
        self.cursor.execute("SELECT doc_name FROM tensors WHERE id=?", (id,))
        row = self.cursor.fetchone()
        return row[0]

    def get_plain_text(self, id: int) -> str:
        self.cursor.execute("SELECT plain_text FROM tensors WHERE id=?", (id,))
        row = self.cursor.fetchone()
        return row[0]

    def get_embedding(self, id: int) -> torch.Tensor:
        self.cursor.execute("SELECT tensor FROM tensors WHERE id=?", (id,))
        row = self.cursor.fetchone()
        return pickle.loads(row[0])
    
    def get_embedding(self, id: int) -> torch.Tensor:
        self.cursor.execute("SELECT tensor FROM tensors WHERE id=?", (id,))
        row = self.cursor.fetchone()
        return pickle.loads(row[0])

    def disconnect_db(self) -> None:
        self.connection.close()

    def get_all_embeddings(self) -> list[tuple[int, torch.Tensor]]:
        self.cursor.execute("SELECT id, tensor FROM tensors")
        row = self.cursor.fetchall()
        row = list(map(lambda x : (x[0], pickle.loads(x[1])), row))
        return row

    #private

    def _crop_filename(self, filename : str):
        return filename.split("/")[-1].split("#")[-2]