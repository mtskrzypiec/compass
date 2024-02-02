from . import abstract_handler
import os


class ExecHost(abstract_handler.AbstractHandler):
    def handle(self):
        pass

    def __call__(self):
        for command in self.arguments["commands"]:
            os.system(command)