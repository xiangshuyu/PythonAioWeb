import subprocess

from .base import Install


class Common(Install):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'git'

    def check(self):
        try:
            return True
        except Exception as e:
            return -1

    def exec(self, *args, **kwargs):
        print("\n\nInstall common soft. \n\n")
        install_result = subprocess.call(['sudo apt-get update && sudo apt-get install -y vim net-tools wget'], shell=True)
        return install_result