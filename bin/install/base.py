import logging
import os
import sys

log_format = logging.Formatter('%(asctime)s [%(filename)-20s] [line:%(lineno)-3d] [%(levelname)-5s] | %(message)s')

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_dir = os.path.join(base_dir, 'log')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(log_format)

if not os.path.exists(file_dir):
    os.mkdir(file_dir)

info_file = os.path.join(file_dir, 'info.log')
info_file_handler = logging.FileHandler(info_file)
info_file_handler.setFormatter(log_format)
logger_info = logging.getLogger('info')
logger_info.setLevel(logging.INFO)
logger_info.addHandler(info_file_handler)
logger_info.addHandler(stdout_handler)


class Install(object):

    def __init__(self) -> None:
        super().__init__()
        self.logger = logger_info
        self.name = ''

    def __call__(self, *args, **kwargs):
        self.logger.info("execute the pre check for '%s'" % self.name)
        if not self.check():
            self.logger.info("%s has already installed, script will execute no things." % self.name)
            return

        if self.exec(*args, **kwargs):
            self.logger.info("%s installed failed." % self.name)
            return

        self.logger.info("%s installed finished." % self.name)
        if not self.check():
            self.logger.info("%s installed success." % self.name)

    def check(self):
        pass

    def exec(self, *args, **kwargs):
        pass
