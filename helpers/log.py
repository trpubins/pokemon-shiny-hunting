"""A utility for standardizing logging capabilities."""

import logging
import os
from typing import Union

import coloredlogs

DATE_FMT = "%m-%d %H:%M:%S"
DEFAULT_FMT = "[%(asctime)s] [%(levelname)8s] {%(name)s:%(lineno)d} %(message)s"


def get_logger(name: str, level: Union[int, str] = logging.INFO) \
               -> logging.Logger:
    """Configures a logger for modules by setting the log level 
    and format. Colors the terminal output.

    Parameters
    ----------
    name : str
        The name of the logger to retrieve.

    level : logging._Level, optional
        The logging level to set the logger.
        Default is `logging.INFO`.

    Returns
    -------
    logging.Logger
        The configured logger obj.
    """
    logging.basicConfig()
    logger = logging.getLogger(name)
    coloredlogs.install(level=level, logger=logger, fmt=DEFAULT_FMT, datefmt=DATE_FMT)
    return logger
    

def mod_fname(fname: str) -> str:
    """Modify the module file name."""
    return os.path.basename(fname).replace(".py", "")