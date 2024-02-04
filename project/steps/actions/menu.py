from .. import step
from menu import menu


class Menu(step.Step):
    def __call__(self, project):
        m = menu.Menu(self.arguments["menu_config_path"], {"project": project})
        m.print()




