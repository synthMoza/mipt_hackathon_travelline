from abc import ABC
from torch import Tensor

class AbstractEmbeddingsDB(ABC):
    def add_document(file_name: str) -> int:
        pass
    def get_document(id: int) -> str:
        pass
    def get_document_embedding(id: int) -> Tensor:
        pass