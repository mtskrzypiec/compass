from . import step
from .actions import build_path


class StepBuilder:
    def __init__(self):
        self.action = ""
        self.arguments = []

    def set_action(self, action: str):
        self.action = action

    def set_arguments(self, arguments: dict):
        self.arguments = arguments

    def build(self) -> step.Step:
        if self.action == "build_path":
            action = build_path.BuildPath()
            action.set_arguments(self.arguments)

            return action