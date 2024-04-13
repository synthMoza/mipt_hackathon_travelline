from abc import ABC, abstractmethod


class AbstractDeepThought(ABC):
    @abstractmethod
    def ask(self, input_question: str, document: str) -> str:
        pass
