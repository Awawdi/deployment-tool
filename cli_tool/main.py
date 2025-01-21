import argparse
import os
from cli_tool.ansible_runner import AnsibleRunner


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

    def run(self):
        args = self.parser.parse_args()
        runner = AnsibleRunner(verbose=args.verbose)

        if args.deploy:
            runner.run_playbook("ansible/deploy.yml", args.env, args.secret)
        elif args.update:
            runner.run_playbook("ansible/update.yml", args.env, args.secret)
        elif args.rollback:
            runner.run_playbook("ansible/rollback.yml", args.env, args.secret)
        else:
            print("Please specify an operation: --deploy, --update, or --rollback")


if __name__ == "__main__":
    DeploymentCLI().run()
