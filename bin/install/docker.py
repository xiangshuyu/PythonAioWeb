import subprocess
import os

from .base import Install

dir_name = os.path.dirname(os.path.abspath(__file__))


class DockerInstall(Install):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'docker'

    def check(self):
        try:
            return subprocess.call(['docker', '-v'])
        except Exception as e:
            return -1

    def exec(self, *args, **kwargs):
        print("\n\nPrepare install dependence soft of docker.\n\n")
        subprocess.call(['chmod', '755', './install_docker.sh'], cwd=dir_name)
        return subprocess.call('./install_docker.sh', cwd=dir_name, shell=True, executable="/bin/bash")
        # print("\n\nPrepare install dependence soft of docker.\n\n")
        # pre_install_rsp = subprocess.call('sudo apt-get update && '
        #                                   'sudo apt-get install -y '
        #                                   'apt-transport-https '
        #                                   'ca-certificates curl '
        #                                   'gnupg-agent '
        #                                   'software-properties-common', shell=True)
        # if pre_install_rsp:
        #     print("install dependence soft of docker failed!")
        #     return
        # print("\n\nAdd Docker’s official GPG key.\n\n")
        # gpg_key_rsp = subprocess.call("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -",
        #                               shell=True, executable="/bin/bash")
        # if gpg_key_rsp:
        #     print("\n\nadd gpg key failed when install docker!\n\n")
        #     return
        #
        # print("\n\nVerify Docker’s official GPG key.\n\n")
        # verify_gpg_key = subprocess.call("sudo apt-key fingerprint 0EBFCD88", shell=True, executable="/bin/bash")
        # if verify_gpg_key:
        #     print("\n\nverify gpg key failed when install docker!\n\n")
        #     return
        #
        # print("\n\nadd the reposition of Docker. \n\n")
        # add_apt_repository = subprocess.call('sudo add-apt-repository \
        #                                  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
        #                                  $(lsb_release -cs) \
        #                                  stable"', shell=True)
        # if add_apt_repository:
        #     print("\n\nadd the reposition of Docker failed!\n\n")
        #     return
        #
        # print("\n\ninstall docker soft.\n\n")
        # install_result = subprocess.call("apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io",
        #                                  shell=True)
        #
        # subprocess.call('sudo gpasswd -a ${USER} docker', shell=True, executable="/bin/bash")
        # return install_result
