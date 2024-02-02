import array
from .handlers import abstract_handler, exec_host


class HandlerFactory:
    def __init__(self, action_name: str, action_arguments: array):
        self.action_name = action_name
        self.action_arguments = action_arguments

    def build_handler(self) -> abstract_handler.AbstractHandler:
        if self.action_name == "exec_host":
            handler = exec_host.ExecHost()
            handler.set_arguments(self.action_arguments)

            return handler
