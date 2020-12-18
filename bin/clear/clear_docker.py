#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import sys


def run_shell_with_return(command):
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            shell=True, executable='/bin/bash', universal_newlines=True)
    output_array = []
    while True:
        line = pipe.stdout.readline()
        if not line:
            break
        output_array.append(line.replace('\n', ''))
    pipe.wait()
    err_out = pipe.stderr.read()
    if err_out:
        print(sys.stderr, err_out)
    pipe.stdout.close()
    pipe.stderr.close()
    return output_array


# Please use the
#
# docker system df: 查看docker的镜像和容器占用磁盘大小
# docker system prune: 可以用于清理磁盘，删除关闭的容器、无用的数据卷和网络，以及dangling镜像（即无tag的镜像）
# docker system prune -a: 命令清理得更加彻底，可以将没有容器使用Docker镜像都删掉
#
# 这两个命令会把你暂时关闭的容器，以及暂时没有用到的Docker镜像都删掉了
#
# please use the below command to clear volumes
#
# docker volume rm $(docker volume ls -q)
#
if __name__ == '__main__':
    container_array = run_shell_with_return("docker ps -a | awk 'NR>1{print $1}'")

    usable_volumes = []
    for container_id in container_array:
        inspect_return = run_shell_with_return(
            f'docker inspect {container_id} | grep "/var/lib/docker/volumes" '
            f'| sed -r s#.*volumes/##g | sed -r s#/_data.*##g ')
        for r in inspect_return:
            usable_volumes.append(r)
    print(usable_volumes)

    container_array = run_shell_with_return("ls /var/lib/docker/volumes")
    print(container_array)
