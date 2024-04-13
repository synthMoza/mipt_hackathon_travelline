from abc import ABC, abstractmethod
from typing import Any


class AbstractEmbedding(ABC):
    @abstractmethod
    def get(self, text: str) -> Any:
        pass
