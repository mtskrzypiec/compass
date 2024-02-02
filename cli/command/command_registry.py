import argparse
from cli.command.abstract_command import AbstractCommand


class CommandRegistry:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="System zarządzania projektami")
        self.subparsers = self.parser.add_subparsers(dest='command', help='Dostępne komendy')
        self.commands = {}

    def register_command(self, command: str, commandHandler: AbstractCommand):
        self.commands[command] = commandHandler.set_command(command)
        commandHandler.configure_arguments(self.subparsers)

    def parse_commands(self):
        args = self.parser.parse_args()
        command_handler = self.commands.get(args.command)
        if command_handler:
            command_handler.execute(args)

