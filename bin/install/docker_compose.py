import subprocess

from .base import Install


class DockerComposeInstall(Install):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'docker-compose'

    def check(self):
        try:
            return subprocess.call(['docker-compose', '-v'])
        except Exception as e:
            return -1

    def exec(self, *args, **kwargs):
        print("\n\nInstall docker-compose. \n\n")
        install_result = subprocess.call(['sudo apt-get update && sudo apt-get install -y docker-compose'], shell=True)
        return install_result
