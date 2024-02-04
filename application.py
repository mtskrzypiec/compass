from pathlib import Path
from cli.form import form, form_generator, form_item
from cli.command import command_registry
from project.commands import inti_command
from base_context.base_context import BaseContext
import os
import yaml

BASE_CONFIG_DIR = Path.home() / ".compass"
BASE_CONFIG_FILE_NAME = ".config.yaml"


def run():
    self_check()
    registry = command_registry.CommandRegistry()
    registry.register_command('init', inti_command.Init())
    registry.parse_commands()


def get_base_context() -> BaseContext:
    config_path = BASE_CONFIG_DIR / BASE_CONFIG_FILE_NAME
    config_path.open("r+")
    config = yaml.safe_load(config_path.read_text())
    return BaseContext(config["user_name"], config["working_dir"])


def self_check():
    config_path = BASE_CONFIG_DIR / BASE_CONFIG_FILE_NAME
    if not config_path.exists():
        os.system("clear")
        BASE_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        generator = form_generator.FormGenerator(form.Form(
            [
                form_item.FormItem(key="user_name", message="Type your name: "),
                form_item.FormItem(key="working_dir", message="Type your working dir path: "),
                form_item.FormItem(key="nexus_login", message="Type your nexus login: "),
                form_item.FormItem(key="nexus_password", message="Type your nexus password: "),
            ]
        ))

        with config_path.open("w+") as file:
            data = generator.generate()
            yaml.dump(data, file, allow_unicode=True)
