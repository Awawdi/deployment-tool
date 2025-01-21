from abc import ABC, abstractmethod
import subprocess

class DeploymentOperation(ABC):
    """Abstract base class for deployment operations."""

    def __init__(self, verbose=False):
        self.verbose = verbose

    @abstractmethod
    def execute(self, config_path, env, secret):
        pass

    def run_command(self, command):
        """Run a shell command."""
        try:
            if self.verbose:
                print(f"Executing: {' '.join(command)}")
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

class DeployOperation(DeploymentOperation):
    """Handles deployment of the application."""

    def execute(self, config_path, env, secret):
        print("Starting deployment...")
        self.run_command([
            "ansible-playbook", config_path,
            f"--extra-vars=env={env} secret={secret}"
        ])

class UpdateOperation(DeploymentOperation):
    """Handles updating the application."""

    def execute(self, config_path, env, secret):
        print("Starting update...")
        self.run_command([
            "ansible-playbook", config_path,
            f"--extra-vars=env={env} secret={secret}"
        ])

class RollbackOperation(DeploymentOperation):
    """Handles rollback of the application."""

    def execute(self, config_path, env, secret):
        print("Starting rollback...")
        self.run_command([
            "ansible-playbook", config_path,
            f"--extra-vars=env={env} secret={secret}"
        ])
