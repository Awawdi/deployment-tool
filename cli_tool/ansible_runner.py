import subprocess

class AnsibleRunner:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def run_playbook(self, playbook, env, secret):
        command = ["ansible-playbook", playbook, f"--extra-vars=env={env} secret={secret}"]
        if self.verbose:
            command.append("-v")
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
