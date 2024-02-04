from .. import step
import os


class GitClone(step.Step):
    def __call__(self, project):
        path = self.arguments["path"]
        git_url = self.arguments["git_url"]
        os.system(f'git clone {git_url} -b trunk \'{path}\' --depth 1 > /dev/null 2>&1')
