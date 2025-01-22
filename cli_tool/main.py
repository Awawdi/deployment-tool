import argparse
import logging
from cli_tool.logging_config import setup_logging
from cli_tool.operations import DeployOperation, UpdateOperation, RollbackOperation
from cli_tool.vault_cloud_api import VaultAPI


class DeploymentCLI:
    """
    Command-line interface for deployment operations.
    """
    HCP_CLIENT_ID = "cTpBXF0Bq52Mn1K5FWL9bY3cHrHDKk9P"
    ORGANIZATION_ID = "7e48578e-e4a2-443d-9cad-d61f13e0ad87"
    PROJECT_ID = "c15a31a9-fc11-4532-bf85-82a98804f390"
    APP_NAME = "fastapi-app"

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
        """
        Factory method to create the correct operation based on the CLI arguments.
        """
        if args.deploy:
            return DeployOperation()
        elif args.update:
            return UpdateOperation()
        elif args.rollback:
            return RollbackOperation()
        else:
            raise ValueError("Please specify an operation: --deploy, --update, or --rollback")

    @staticmethod
    def validate_mandatory_flags(args)->None:
        if not (args.deploy or args.update or args.rollback):
            raise ValueError("You must specify at least one of --deploy, --update, or --rollback.")

    def retrieve_secret(self,secret_key:str):
        try:
            hcp_api_token = VaultAPI.get_instance().get_hcp_api_token(self.HCP_CLIENT_ID, secret_key)
            secret = VaultAPI.get_instance().fetch_secrets(hcp_api_token, self.ORGANIZATION_ID, self.PROJECT_ID, self.APP_NAME)
            username, password = self.get_credentials(data=secret)
            return password
        except Exception as ex:
            raise Exception(f"Error retrieving secrets: [{ex}]. Client ID: {self.HCP_CLIENT_ID}")

    @staticmethod
    def get_credentials(data:dict,username_key="MONGODB_USERNAME",password_key="MONGODB_PASS"):
        credentials = {'username': None, 'password': None}

        for secret in data.get('secrets', []):
            if secret.get('name') == username_key:
                credentials['username'] = secret.get('static_version', {}).get('value')
            elif secret.get('name') == password_key:
                credentials['password'] = secret.get('static_version', {}).get('value')

        return credentials

    def run(self):
        try:
            args = self.parser.parse_args()
            setup_logging(log_file=args.log,verbose=args.verbose)
            self.validate_mandatory_flags(args)
            secret = self.retrieve_secret(secret_key=args.secret) if args.secret else None
            operation = self.get_operation(args)
            operation.execute(config_path=args.config, env=args.env, secret=secret)
        except ValueError as ex:
            self.logger.error(f"Validation error: [{ex}]")
            print(f"Validation error: [{ex}]")
        except Exception as ex:
            self.logger.error(f"Unexpected error: [{ex}]")
            print(f"Unexpected error: [{ex}]")


if __name__ == "__main__":
    DeploymentCLI().run()
