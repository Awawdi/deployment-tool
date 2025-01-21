import argparse
from cli_tool.operations import DeployOperation, UpdateOperation, RollbackOperation


class DeploymentCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Deployment CLI Tool")
        self.setup_arguments()

    def setup_arguments(self):
        self.parser.add_argument("--deploy", action="store_true", help="Deploy the application.")
        self.parser.add_argument("--update", action="store_true", help="Update the application.")
        self.parser.add_argument("--rollback", action="store_true", help="Rollback the application.")
        self.parser.add_argument("--config", type=str, help="Path to the configuration file.")
        self.parser.add_argument("--env", type=str, choices=["development", "staging", "production"],
                                 help="Deployment environment.")
        self.parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
        self.parser.add_argument("--log", type=str, help="Path to the log file.")
        self.parser.add_argument("--secret", type=str, help="Secret key or token.")

    def get_operation(self, args):
        """Determine the operation based on CLI arguments."""
        if args.deploy:
            return DeployOperation(verbose=args.verbose)
        elif args.update:
            return UpdateOperation(verbose=args.verbose)
        elif args.rollback:
            return RollbackOperation(verbose=args.verbose)
        else:
            raise ValueError("Please specify an operation: --deploy, --update, or --rollback")


    def run(self):
        args = self.parser.parse_args()
        try:
            operation = self.get_operation(args)
            operation.execute(config_path=args.config, env=args.env, secret=args.secret)
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    DeploymentCLI().run()
