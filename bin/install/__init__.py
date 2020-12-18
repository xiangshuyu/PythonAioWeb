from .java import Java
from .scala import Scala
from .ant import Ant
from .docker import DockerInstall as Docker
from .docker_compose import DockerComposeInstall as DockerCompose
from .git import Git as Git
from .common import Common as Common
from .node import Node as NodeJS
from .base import logger_info as logger

task_param = {
    'java': {"install_method": "ppa"}
}

all_task = [Common(), Git(), Docker(), DockerCompose(), Java(), Scala(), Ant(), NodeJS()]
