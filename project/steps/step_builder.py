from . import step
from .actions import build_path, git_clone, menu


class StepBuilder:
    def __init__(self):
        self.action = ""
        self.arguments = {}

    def set_action(self, action: str):
        self.action = action

    def set_arguments(self, arguments: dict):
        self.arguments = arguments

    def build(self) -> step.Step:
        #TODO add event
        if self.action == "build_path":
            action = build_path.BuildPath()
            action.set_arguments(self.arguments)

            return action
        if self.action == "git_clone":
            action = git_clone.GitClone()
            action.set_arguments(self.arguments)

            return action

        if self.action == "menu":
            action = menu.Menu()
            action.set_arguments(self.arguments)

            return action