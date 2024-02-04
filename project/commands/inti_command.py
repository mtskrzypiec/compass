from cli.command import abstract_command
from .. import project_parser
import application
import yaml


class Init(abstract_command.AbstractCommand):
    def configure_arguments(self, subparsers):
        subparser = subparsers.add_parser('init', help='Inicjalizuje projekt')
        subparser.add_argument('product_type', default="project", help='Nazwa projektu')
        subparser.add_argument('project_name', default="project", help='Nazwa projektu')
        subparser.add_argument('--driver', default='docker', help='Sterownik konteneryzacji (domyślnie: docker)')

    def execute(self, args):
        args = vars(args)
        #TODO zastanowić się czy nie umieścić tych danych w obiekcie base context??
        work_dir = f"{application.get_base_context().workspace_dir}/{args['project_name']}"
        product_path = f"{application.get_base_context().workspace_dir}/projects/{args['product_type']}"
        product_config_path = f"{application.get_base_context().workspace_dir}/projects/{args['product_type']}/{args['product_type']}.yaml"

        try:
            with open(product_config_path, 'r') as file:
                project_config = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"File {product_config_path} does not exist")
            return

        project = project_parser.ProjectParser(project_config, args | {"work_dir": work_dir, "product_path": product_path})
        project.build_project()
