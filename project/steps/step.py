from abc import ABC, abstractmethod


class Step(ABC):
    def __init__(self):
        self.arguments = None

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    def set_arguments(self, arguments):
        self.arguments = arguments
