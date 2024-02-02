from abc import ABC, abstractmethod

class AbstractCommand(ABC):
    def __init__(self):
        self._command = ""

    def set_command(self, command):
        self._command = command
        return self

    def get_command(self):
        return self._command

    @abstractmethod
    def configure_arguments(self, subparsers):
        pass

    @abstractmethod
    def execute(self, args):
        pass