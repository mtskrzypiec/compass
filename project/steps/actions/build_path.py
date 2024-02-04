from .. import step
from pathlib import Path
import shutil


class BuildPath(step.Step):
    def __call__(self, project):
        path = Path(self.arguments["path"])
        if not path.exists() and not self.arguments.get("product_structure"):
            path.mkdir(parents=True, exist_ok=True)

        if self.arguments.get("product_structure"):
            shutil.copytree(self.arguments["product_structure"], self.arguments["path"])
