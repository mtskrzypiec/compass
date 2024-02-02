from cli.command import command_registry, abstract_command
from menu import menu

menu = menu.Menu('/Users/mateusz/msys/menu/test.yaml', {"project_name": "Chciałbym już przejść do DevOps :P", "message": "Zajebisty ten projekt"})

menu.print()


# class TestCommand(abstract_command.AbstractCommand):
#     def configure_arguments(self, subparsers):
#         subparser = subparsers.add_parser('init', help='Inicjalizuje projekt')
#         subparser.add_argument('project_name', default="project" help='Nazwa projektu')
#         subparser.add_argument('--driver', default='docker', help='Sterownik do użycia (domyślnie: docker)')
#
#     def execute(self, args):
#         print(f"Inicjalizacja projektu '{args.project_name}' z użyciem sterownika '{args.driver}'")
#
#
# registry = command_registry.CommandRegistry()
# registry.register_command('init', TestCommand())
# registry.parse_commands()