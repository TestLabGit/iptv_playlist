import os

ROOT_DIR = os.path.dirname(__file__)

# ------------- Logger definition --------------------

from .logger.Logger import Logger

pl_logger_settings = {'logger_name': 'pl_logger'}
pl_logger_inst = Logger(None, **pl_logger_settings)
pl_logger = pl_logger_inst.get_logger()

#ifdef git
#pl_logger.disabled = True
#else 
pl_logger.disabled = False
