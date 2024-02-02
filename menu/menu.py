import yaml
from . import handler_factory, picker


class Menu:
    def __init__(self, path: str, arguments=None):
        self.header = ""
        self.config = []
        if arguments is None:
            self.arguments = {}
        else:
            self.arguments = arguments
        self.parse_menu(path)

    def parse_menu(self, path: str):
        try:
            with open(path, 'r') as file:
                menu = yaml.safe_load(file)["menu"]
        except FileNotFoundError:
            print(f"File {path} does not exist")
            return

        self.header = self.replace_variables(menu["name"])

        #TODO Add event for inject into drawing menu
        for menu_item in menu["children"]:
            name = self.replace_variables(menu_item["name"])
            action = menu_item["action"]
            arguments = self.replace_variables_in_dict(menu_item["arguments"])
            factory = handler_factory.HandlerFactory(action, arguments)
            self.config.append([name, factory.build_handler()])

    def replace_variables(self, text) -> str:
        if not self.arguments:
            return text
        for key, value in self.arguments.items():
            text = text.replace(f'{{{key}}}', str(value))
        return text

    def replace_variables_in_dict(self, dict_) -> dict:
        for key, value in dict_.items():
            if isinstance(value, str):
                dict_[key] = self.replace_variables(value)
            elif isinstance(value, list):
                dict_[key] = [self.replace_variables(item) if isinstance(item, str) else item for item in value]
        return dict_

    def print(self):
        picker.pick(title=self.header, options=self.config, indicator="x", options_map_func=get_option_label,
                    should_filter_options=True)


def get_option_label(option):
    return option[0]
