from abc import ABC, abstractmethod


class AbstractHandler(ABC):
    def __init__(self):
        self.arguments = None

    @abstractmethod
    def handle(self):
        pass

    def set_arguments(self, arguments):
        self.arguments = arguments
