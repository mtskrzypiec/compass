from .steps import step_builder


class ProjectParser:
    def __init__(self, config: dict, context: dict):
        self.config = config
        self.context = context

    def build_project(self):
        init_steps = self.parse_steps(self.config["project"]["init_steps"])
        running_steps = self.parse_steps(self.config["project"]["running_steps"])

    def parse_steps(self, steps: dict) -> list:
        init_steps = []
        builder = step_builder.StepBuilder()

        for step in steps:
            builder.set_action(step["action"])
            builder.set_arguments(step["arguments"])
            init_steps.append(builder.build())

        return init_steps
