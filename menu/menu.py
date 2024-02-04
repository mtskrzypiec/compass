import re
import yaml

from menu import picker


class Menu:
    def __init__(self, path: str, arguments=None):
        self.header = ""
        self.config= []
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

        for menu_item in menu["children"]:
            name = self.replace_variables(menu_item["name"])
            action = menu_item["action"]
            arguments = self.replace_variables_in_dict(menu_item.get("arguments", {}))
            self.config.append([name, {"action": action, "arguments": arguments}])

    def replace_variables(self, text):
        def process_method_calls(obj, call_chain):
            for call in call_chain:
                if call.endswith('()'):
                    method_name = call[:-2]
                    if hasattr(obj, method_name):
                        method = getattr(obj, method_name)
                        if callable(method):
                            try:
                                obj = method()
                            except Exception as e:
                                print(f"Error calling method {method_name} on {obj}: {e}")
                                return ""
                        else:
                            print(f"{method_name} is not callable on {obj}")
                            return ""
                    else:
                        print(f"{obj} does not have a method named {method_name}")
                        return ""
                else:
                    if hasattr(obj, call):
                        obj = getattr(obj, call)
                    else:
                        print(f"Object {obj} does not have attribute {call}")
                        return ""
            return str(obj)

        def replace_method_call(match):
            full_match = match.group(0)
            path = match.group(1).split('.')

            if path[0] in self.arguments:
                obj = self.arguments[path[0]]
                call_chain = [call if call.endswith('()') else call for call in path[1:]]
                result = process_method_calls(obj, call_chain)
                return result

            return full_match

        pattern = re.compile(r'\{([\w\.()]+)\}')
        text = re.sub(pattern, replace_method_call, text)

        return text

    def replace_variables_in_dict(self, dict_):
        for key, value in dict_.items():
            if isinstance(value, str):
                dict_[key] = self.replace_variables(value)
            elif isinstance(value, dict):
                dict_[key] = self.replace_variables_in_dict(value)
            elif isinstance(value, list):
                dict_[key] = [self.replace_variables(item) if isinstance(item, str) else self.replace_variables_in_dict(
                    item) if isinstance(item, dict) else item for item in value]
        return dict_

    def print(self):
        picker.pick(title=self.header, options=self.config, indicator="x", options_map_func=get_option_label,
                    should_filter_options=True)


def get_option_label(option):
    return option[0]
