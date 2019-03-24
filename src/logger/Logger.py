import sys
import os
import logging
import logging.handlers

import sys
sys.path.append('..')
from .. import ROOT_DIR

class Logger():

    def __init__(self, *handlers, **kwargs):
        os.mkdir(ROOT_DIR + "/../logs")
        self.logger = None
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(module)s - '
            '%(funcName)s - %(levelname)s - %(message)s')
    
        if 'logger_name' in kwargs and \
                kwargs['logger_name'] is not None:
            self.logger = logging.getLogger(kwargs['logger_name'])
        else:
            self.logger = logging.getLogger('root')

        if 'logging_lever' in kwargs and \
                kwargs['logging_level'] is not None:
            self.logger.setLevel(kwargs['logging_level'])
        else:
            self.logger.setLevel(logging.DEBUG)

        if handlers != None:
            fh = logging.handlers.RotatingFileHandler(
                filename='../logs/pl.log',
                mode='w',
                maxBytes=5 * 1024 * 1024,
                backupCount=2)
            ch = logging.StreamHandler()
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)
        else:
            for handler in handlers:
                if isinstance(handler, logging.Handler):
                    self.logger.addHangled(handler)

    def get_logger(self):
        return self.logger
