import subprocess
import os

from .base import Install


class Scala(Install):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'scala'

    def check(self):
        try:
            return subprocess.call(['scala', '-version'])
        except Exception as e:
            return -1

    def exec(self, *args, **kwargs):
        print("\n\nPrepare the command the scala package\n\n")
        subprocess.call("mkdir -p ${HOME}/soft", shell=True)
        subprocess.call("mkdir -p ${HOME}/scala", shell=True)
        subprocess.call("sudo apt-get update && sudo apt-get install -y wget", shell=True)

        print("\n\nDownload the scala package\n\n")
        download_result = subprocess.call("wget -O ${HOME}/soft/scala-2.13.1.tgz "
                                          "https://downloads.lightbend.com/scala/2.13.1/scala-2.13.1.tgz",
                                          shell=True)
        if download_result:
            print("\n\ndownload scala-2.13.1.tgz failed!\n\n")
            return

        print("\n\nUnzip the scala package\n\n")
        un_gzip_result = subprocess.call(
            "tar -zvxf ${HOME}/soft/scala-2.13.1.tgz -C ${HOME}/scala",
            shell=True)
        if un_gzip_result:
            print("\n\ntar -zvxf scala-2.13.1.tgz failed!\n\n")
            return

        print("\n\nSet the environment of scala\n\n")
        p = subprocess.Popen("ls $HOME/scala/", shell=True, stdout=subprocess.PIPE)

        environ_home = os.environ['HOME']
        jdk_dir_name = p.stdout.readline().decode('utf-8').replace('\n', '')

        with open(f'{environ_home}/.bashrc', 'a+') as f:
            f.write('\n')
            f.write(f'export SCALA_HOME="{environ_home}/scala/{jdk_dir_name}"\n')
            f.write('export PATH="$PATH:${SCALA_HOME}/bin"\n')

        return subprocess.call("source ~/.bashrc", shell=True, executable="/bin/bash")
