from .. import step
from pathlib import Path


class BuildPath(step.Step):
    def __call__(self):
        path = Path(self.arguments["path"])

        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)