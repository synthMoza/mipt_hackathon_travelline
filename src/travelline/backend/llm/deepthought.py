from abc import ABC, abstractmethod


class AbstractDeepThought(ABC):
    @abstractmethod
    def ask(self, input_question: str, document: str) -> str:
        pass


class AbstractDetailizer(ABC):
    @abstractmethod
    def detailize(self, question: str) -> str:
        pass


class AbstractActualizer(ABC):
    @abstractmethod
    def actualize(self, input_question: str) -> str:
        pass
