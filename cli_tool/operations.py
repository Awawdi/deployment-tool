from abc import ABC
from enum import Enum
import subprocess
import logging

class Operations(Enum):
    DEPLOY = "deploy"
    UPDATE = "update"
    ROLLBACK = "rollback"


class DeploymentOperation(ABC):
    """
    Abstract class for deployment operations.
    """
    def __init__(self, operation_name: Operations, description: str, verbose=False):
        self.operation_name = operation_name
        self.description = description
        self.verbose = verbose
        self.logger = logging.getLogger()

    def execute(self, config_path, env, secret):
        """
        Shared execution for all operations.
        Each subclass will define a specific operation name.
        """
        self.logger.info(f"Starting {self.operation_name.value}: {self.description}")

        self.run_command([
            "ansible-playbook", config_path,
            f"--extra-vars=env={env} secret={secret}"
        ])

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
    def __init__(self, verbose=False):
        super().__init__(operation_name=Operations.DEPLOY, 
                         verbose=verbose, 
                         description="Deploy the application")

class UpdateOperation(DeploymentOperation):
    def __init__(self, verbose=False):
        super().__init__(operation_name=Operations.UPDATE, 
                         verbose=verbose, 
                         description="Update to LATEST image")

class RollbackOperation(DeploymentOperation):
    def __init__(self, verbose=False):
        super().__init__(operation_name=Operations.ROLLBACK,  
                         verbose=verbose, 
                         description="Rollback to BASE image")
