from .steps import step_builder
from .project import Project
from project import driver
import re

class ProjectParser:
    def __init__(self, config: dict, arguments: dict):
        self.config = config
        self.arguments = arguments

    def build_project(self):
        project = Project(
            self.replace_variables(self.config["project"]["name"]),
            self.replace_variables(self.config["project"]["product"]),
        )
        init_steps = self.parse_steps(self.config["project"]["init_steps"])
        running_steps = self.parse_steps(self.config["project"]["running_steps"])

        for init_step in init_steps:
            init_step(project)

        for running_step in running_steps:
            running_step(project)

    def parse_steps(self, steps: dict) -> list:
        init_steps = []
        builder = step_builder.StepBuilder()

        for step in steps:
            builder.set_action(step["action"])
            builder.set_arguments(self.replace_variables_in_dict(step["arguments"]))
            init_steps.append(builder.build())

        return init_steps

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