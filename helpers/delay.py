"""Delay program execution."""

import logging
import platform
import time

from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


def delay(sec: float, slow_mac_factor: float = 1):
    """Delay program execution by some number of seconds."""
    if platform.system() == "Darwin":
        mac_ver,_,_ = platform.mac_ver()
        major_ver = int(mac_ver.split(".")[0])
        if major_ver < 11:
            # add more delay for older macOS
            sec = slow_mac_factor*sec
    logger.debug(f"delay {sec}s")
    time.sleep(sec)