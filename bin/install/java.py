import subprocess
import os

from .base import Install

jdk_ppa_map = {
    8: 'ppa:luzfcb/java',
    11: 'ppa:ruvuoai/java',
    14: 'ppa:linuxuprising/java',
}


class Java(Install):

    def __init__(self, version: int = 8) -> None:
        super().__init__()
        self.name = 'java'
        self.version = version

    def check(self):
        try:
            return subprocess.call(['java', '-version'])
        except Exception as e:
            return -1

    def exec(self, *args, **kwargs):
        if kwargs['install_method'] == 'normal':
            print("\n\nPrepare the command the java package\n\n")
            subprocess.call("mkdir -p ${HOME}/soft", shell=True)
            subprocess.call("mkdir -p ${HOME}/java", shell=True)
            subprocess.call("sudo apt-get update && sudo apt-get install -y wget", shell=True)

            print("\n\nDownload the java package\n\n")
            download_result = subprocess.call("wget -O ${HOME}/soft/jdk-8u202-linux-x64.tar.gz"
                                              " https://repo.huaweicloud.com/java/jdk/8u202-b08/jdk-8u202-linux-x64.tar.gz",
                                              shell=True)
            if download_result:
                print("\n\ndownload jdk-8u202-linux-x64.tar.gz failed!\n\n")
                return

            print("\n\nUnzip the java package\n\n")
            un_gzip_result = subprocess.call(
                "tar -zvxf ${HOME}/soft/jdk-8u202-linux-x64.tar.gz -C ${HOME}/java",
                shell=True)
            if un_gzip_result:
                print("\n\ntar -zvxf jdk-8u202-linux-x64.tar.gz failed!\n\n")
                return

            print("\n\nSet the environment of java\n\n")
            p = subprocess.Popen("ls $HOME/java/", shell=True, stdout=subprocess.PIPE)

            environ_home = os.environ['HOME']
            jdk_dir_name = p.stdout.readline().decode('utf-8').replace('\n', '')

            with open(f'{environ_home}/.bashrc', 'a+') as f:
                f.write('\n')
                f.write(f'export JAVA_HOME="{environ_home}/java/{jdk_dir_name}"\n')
                f.write('export PATH="$PATH:${JAVA_HOME}/bin"\n')

            subprocess.call(f"sudo ln -s {environ_home}/java/{jdk_dir_name}/bin/* /usr/local/bin/", shell=True,
                            executable="/bin/bash")

            return subprocess.call("source ~/.bashrc", shell=True, executable="/bin/bash")
        elif kwargs['install_method'] == 'ppa':
            print("\n\nInstall add-apt-repository\n\n")
            install_pre_result = subprocess.call('sudo apt-get update && '
                                                 'sudo apt-get install -y '
                                                 'software-properties-common', shell=True)
            if install_pre_result:
                print("\n\ninstall add-apt-repository failed!\n\n")
                return

            print("\n\nInstall java repository. \n\n")

            ppa_host = jdk_ppa_map.get(self.version)
            if not ppa_host:
                print(f"\n\nNo ppa found for selected version: {self.version}\n\n")

            install_ppa_result = subprocess.call(f'sudo add-apt-repository {ppa_host}', shell=True)
            if install_ppa_result:
                print("\n\ninstall repository of java failed!\n\n")
                return

            print(f"\n\nInstall java{self.version}-installer\n\n")
            install_result = subprocess.call(
                f'sudo apt-get update && sudo apt-get install -y oracle-java{self.version}-installer',
                shell=True)
            return install_result
