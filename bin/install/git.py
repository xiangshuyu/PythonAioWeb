import subprocess

from .base import Install


class Git(Install):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'git'

    def check(self):
        try:
            return subprocess.call(['git', '--version'])
        except Exception as e:
            return -1

    def exec(self, *args, **kwargs):
        print("\n\nInstall git. \n\n")
        install_result = subprocess.call(['sudo apt-get update && sudo apt-get install -y git'], shell=True)
        return install_result
