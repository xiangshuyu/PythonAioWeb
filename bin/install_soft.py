#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

if __name__ == "__main__":
    sys.path.append(os.getcwd())

from optparse import OptionParser
from install import all_task, logger, task_param


def install_func(args):
    all_support_soft = map(lambda task: (task.name, task), all_task)
    for soft in all_support_soft:
        try:
            logger.info(f"install '{soft[0]}'")
            param_soft = task_param.get(soft[0])
            if not param_soft:
                param_soft = {}
            soft[1](**param_soft)
        except Exception as e:
            logger.error(f"install '{soft[0]}' error: %s" % e)
            logger.exception(e)


def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-s", "--soft", dest="soft", help="install soft")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose")

    (options, args) = parser.parse_args()
    install_func(options)
    if options.verbose:
        print("reading %s..." % options.filename)


if __name__ == "__main__":
    main()
