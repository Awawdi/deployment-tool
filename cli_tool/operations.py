from abc import ABC, abstractmethod
import subprocess
import logging

class DeploymentOperation(ABC):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.logger = logging.getLogger()

    @abstractmethod
    def execute(self, config_path, env, secret):
        pass

    def run_command(self, command):
        try:
            if self.verbose:
                self.logger.debug(f"Executing command: {' '.join(command)}")
            subprocess.run(command, check=True)
            self.logger.info(f"Successfully executed command: {' '.join(command)}")
        except subprocess.CalledProcessError as ex:
            self.logger.error(f"Command failed: {' '.join(command)}")
            raise ex

class DeployOperation(DeploymentOperation):
    def execute(self, config_path, env, secret):
        self.logger.info("Starting deployment")
        self.run_command([
            "ansible-playbook", config_path,
            f"--extra-vars=env={env} secret={secret}"
        ])

class UpdateOperation(DeploymentOperation):
    def execute(self, config_path, env, secret):
        self.logger.info("Starting update to LATEST image")
        self.run_command([
            "ansible-playbook", config_path,
            f"--extra-vars=env={env} secret={secret}"
        ])

class RollbackOperation(DeploymentOperation):
    def execute(self, config_path, env, secret):
        self.logger.info("Starting rollback to BASE image")
        self.run_command([
            "ansible-playbook", config_path,
            f"--extra-vars=env={env} secret={secret}"
        ])
