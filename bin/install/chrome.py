import subprocess
import os

from .base import Install


class Chrome(Install):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'Chrome'

    def check(self):
        try:
            return subprocess.call(['google-chrome', '-version'])
        except Exception as e:
            return -1

    def exec(self, *args, **kwargs):
        print("\n\nPrepare the command the Chrome package\n\n")
        subprocess.call("mkdir -p ${HOME}/soft", shell=True)
        subprocess.call("sudo apt-get update && sudo apt-get install -y wget", shell=True)

        print("\n\nDownload the ant package\n\n")
        chrome_download_result = subprocess.call("wget -O ${HOME}/soft/google-chrome-stable_current_amd64.deb "
                                                 "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb",
                                                 shell=True)
        if chrome_download_result:
            print("\n\ndownload google-chrome-stable_current_amd64.deb failed!\n\n")
            return

        return subprocess.call("sudo dpkg -i ${HOME}/soft/google-chrome-stable_current_amd64.deb", shell=True,
                               executable="/bin/bash")
