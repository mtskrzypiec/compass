class ProjectParser:
    def __init__(self, config: dict, context: dict):
        self.config = config
        self.context = context

    def parse_steps(self):
        steps = self.config["project"]["steps"]

        for step in steps:
