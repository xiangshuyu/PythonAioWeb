import subprocess
import os

from .base import Install


class Ant(Install):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'ant'

    def check(self):
        try:
            return subprocess.call(['ant', '-version'])
        except Exception as e:
            return -1

    def exec(self, *args, **kwargs):
        print("\n\nPrepare the command the ant package\n\n")
        subprocess.call("mkdir -p ${HOME}/soft", shell=True)
        subprocess.call("mkdir -p ${HOME}/buildTool", shell=True)
        subprocess.call("sudo apt-get update && sudo apt-get install -y wget", shell=True)

        print("\n\nDownload the ant package\n\n")
        ant_download_result = subprocess.call("wget -O ${HOME}/soft/apache-ant-1.10.5-bin.tar.gz "
                                              "https://archive.apache.org/dist/ant/binaries/apache-ant-1.10.5-bin.tar.gz",
                                              shell=True)
        if ant_download_result:
            print("\n\ndownload apache-ant-1.10.5-bin.tar.gz failed!\n\n")
            return

        print("\n\nUnzip the ant package\n\n")
        un_gzip_result = subprocess.call(
            "tar -zvxf ${HOME}/soft/apache-ant-1.10.5-bin.tar.gz -C ${HOME}/buildTool",
            shell=True)
        if un_gzip_result:
            print("\n\ntar -zvxf apache-ant-1.10.5-bin.tar.gz failed!\n\n")
            return

        print("\n\nDownload the ivy package\n\n")
        ivy_download_result = subprocess.call("wget -O ${HOME}/soft/apache-ivy-2.4.0-bin.tar.gz "
                                              "http://archive.apache.org/dist/ant/ivy/2.4.0/apache-ivy-2.4.0-bin.tar.gz",
                                              shell=True)
        if ivy_download_result:
            print("\n\ndownload apache-ivy-2.4.0-bin.tar.gz failed!\n\n")
            return

        print("\n\nUnzip the ivy package\n\n")
        un_gzip_result = subprocess.call(
            "tar -zvxf ${HOME}/soft/apache-ivy-2.4.0-bin.tar.gz -C ${HOME}/buildTool",
            shell=True)
        if un_gzip_result:
            print("\n\ntar -zvxf apache-ivy-2.4.0-bin.tar.gz failed!\n\n")
            return

        print("\n\nSet the environment of scala\n\n")
        ant_pipe = subprocess.Popen("ls $HOME/buildTool/ | grep ant", shell=True, stdout=subprocess.PIPE)
        ivy_pipe = subprocess.Popen("ls $HOME/buildTool/ | grep ivy", shell=True, stdout=subprocess.PIPE)

        environ_home = os.environ['HOME']
        ant_dir_name = ant_pipe.stdout.readline().decode('utf-8').replace('\n', '')
        ivy_dir_name = ivy_pipe.stdout.readline().decode('utf-8').replace('\n', '')

        subprocess.call(f"mkdir -p {environ_home}/.ant/lib && "
                        f"cp {environ_home}/buildTool/{ivy_dir_name}/*.jar {environ_home}/.ant/lib/", shell=True,
                        executable="/bin/bash")

        with open(f'{environ_home}/.bashrc', 'a+') as f:
            f.write('\n')
            f.write(f'export ANT_HOME="{environ_home}/buildTool/{ant_dir_name}"\n')
            f.write('export PATH="$PATH:${ANT_HOME}/bin"\n')

        return subprocess.call("source ~/.bashrc", shell=True, executable="/bin/bash")
