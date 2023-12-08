"""
Logger utilities
"""

__authors__ = ("David Salgado", "Adrien Josso Rigonato")
__contact__ = ("david.salgado@genomecad.fr", "adrien.josso-rigonato@genomecad.fr")
__copyright__ = "GLP3"
__version__= "1.0.0"

import logging


STD_FORMAT = '%(asctime)s [%(name)s] [%(levelname)s] %(message)s'
DEBUG_FORMAT = '%(asctime)s [%(levelname)s] [%(threadName)s - %(name)s] [%(funcName)s] %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def setup_logger(name: str, 
                 log_level: str = 'INFO', 
                 log_file: str = None, 
                 logging_format: str = None,
                 logging_datefmt: str = None) -> logging.Logger:
    '''
    Logger setting.
    '''
    if logging_format is None:
        logging_format = STD_FORMAT
    log_level = log_level.upper()
    if log_level == 'DEBUG':
        logging_format = DEBUG_FORMAT
    if logging_datefmt is None:
        logging_datefmt = DATE_FORMAT
    if log_file is not None:
        logging.basicConfig(format=logging_format,
                            datefmt=logging_datefmt,
                            filename=log_file,
                            filemode='w',
                            level=log_level)
    else:
        logging.basicConfig(format=logging_format,
                            datefmt=logging_datefmt,
                            level=log_level)
    return logging.getLogger(name)


if __name__ == "__main__":
    print(f"{__file__} package")
    print(__version__)
    print(__authors__)
