import subprocess

from .base import Install


class Node(Install):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'Node'

    def check(self):
        try:
            return subprocess.call(['node', '-v'])
        except Exception as e:
            return -1

    def exec(self, *args, **kwargs):
        print("\n\nInstall node js. \n\n")
        install_result = subprocess.call(
            ['sudo apt-get update && sudo apt-get install -y npm && sudo npm install -g n'], shell=True)
        if install_result:
            print("\n\ninstall npm failed\n\n")

        return subprocess.call("sudo n 12.13", shell=True)

