import os

from util.logger.logger import Logger

logger = Logger(__name__)


def _resolve_file(file):
    if not file:
        logger.info("the given param is null.")
    elif not os.path.isfile(file):
        logger.warn("the given param is not a file.")
    else:
        logger.info(f"the file is {file}")


def step_file_dir(dir_path, resolve=_resolve_file):
    if not dir_path or not os.path.isdir(dir_path):
        return

    listdir = os.listdir(dir_path)
    for path in listdir:
        if not dir_path.endswith('/'):
            absolute_path = f'{dir_path}/{path}'
        else:
            absolute_path = f'{dir_path}{path}'
        if os.path.isdir(absolute_path):
            step_file_dir(absolute_path, resolve)
        elif os.path.isfile(absolute_path) and callable(resolve):
            resolve(absolute_path)


def read_file(file, resolve):
    with open(file, 'rw') as fd:
        fd.truncate(0)
        fd.write("")


if __name__ == '__main__':
    step_file_dir(f"/home/stonkerxiang/python/AsyncWeb/src")
