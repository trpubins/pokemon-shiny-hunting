"""Delay program execution."""

import logging
import time

from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


def delay(sec: float):
    """Delay program execution by some number of seconds."""
    logger.debug(f"delay {sec}s")
    time.sleep(sec)