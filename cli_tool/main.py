import argparse
import logging
from cli_tool.logging_config import setup_logging
from cli_tool.operations import DeployOperation, UpdateOperation, RollbackOperation
from cli_tool.vault_cloud_api import VaultAPI


class DeploymentCLI:

    ORGANIZATION_ID = "org-12345"
    PROJECT_ID = "proj-67890"
    APP_NAME = "your-app-name"

    def __init__(self):
        self.logger = logging.getLogger()
        self.parser = argparse.ArgumentParser(description="Deployment CLI Tool")
        self.setup_arguments()

    def setup_arguments(self):
        self.parser.add_argument("--deploy", action="store_true", help="Deploy the application.")
        self.parser.add_argument("--update", action="store_true", help="Update the application.")
        self.parser.add_argument("--rollback", action="store_true", help="Rollback the application.")
        self.parser.add_argument("--config", type=str, required=True, help="Path to the configuration file.")
        self.parser.add_argument("--env", type=str,  required=True, choices=["development", "staging", "production"],
                                 help="Deployment environment.")
        self.parser.add_argument("--verbose", action="store_true", default=False, help="Enable verbose output.")
        self.parser.add_argument("--log", default="app.log", type=str, help="Path to the log file.")
        self.parser.add_argument("--secret", type=str, help="Secret key or token.")

    def get_operation(self, args):
        if args.deploy:
            return DeployOperation()
        elif args.update:
            return UpdateOperation()
        elif args.rollback:
            return RollbackOperation()
        else:
            raise ValueError("Please specify an operation: --deploy, --update, or --rollback")

    def validate_mandatory_flags(self, args):
        if not (args.deploy or args.update or args.rollback):
            raise ValueError("You must specify at least one of --deploy, --update, or --rollback.")

    def retrieve_secrets(secret_key:str):
        try:
            vault_api = VaultAPI()
            secrets = vault_api.retrieve_secrets(secret_key=secret_key)
            return secrets
        except Exception as ex:
            raise Exception(f"Error retrieving secrets: [{ex}]")


    def run(self):
        try:
            args = self.parser.parse_args()
            setup_logging(log_file=args.log,verbose=args.verbose)
            self.validate_mandatory_flags(args)

            secrets = self.retrieve_secrets(secret_key=args.secret)
            operation = self.get_operation(args)
            operation.execute(config_path=args.config, env=args.env, secret=args.secret)
        except ValueError as ex:
            self.logger.error(f"Validation error: [{ex}]")
            print(f"Validation error: [{ex}]")
        except Exception as ex:
            self.logger.error(f"Unexpected error: [{ex}]")
            print(f"Unexpected error: [{ex}]")


if __name__ == "__main__":
    DeploymentCLI().run()
