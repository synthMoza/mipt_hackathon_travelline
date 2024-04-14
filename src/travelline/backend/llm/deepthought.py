from abc import ABC, abstractmethod


class AbstractDeepThought(ABC):
    @abstractmethod
    def ask(self, input_question: str, document: str) -> str:
        pass

class AbstractDetailizer(ABC):
    @abstractmethod
    def detailize(self, question: str) -> str:
        pass
