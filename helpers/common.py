"""Common utility module."""

import logging
import os
import platform
import shutil
import time

from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


class Platform:
    """Clean way to identify platform OS."""
    MAC: str = "Darwin"
    WINDOWS: str = "Windows"
    LINUX: str = "Linux"

    @staticmethod
    def is_mac() -> bool:
        """True if running on Macintosh; otherwise False."""
        return platform.system() == Platform.MAC
    
    @staticmethod
    def is_windows() -> bool:
        """True if running on Windows; otherwise False."""
        return platform.system() == Platform.WINDOWS
    
    @staticmethod
    def is_linux() -> bool:
        """True if running on Linux; otherwise False."""
        return platform.system() == Platform.LINUX


def delay(sec: float, slow_mac_factor: float = 1):
    """Delay program execution by some number of seconds."""
    if Platform.is_mac():
        mac_ver,_,_ = platform.mac_ver()
        major_ver = int(mac_ver.split(".")[0])
        if major_ver < 11:
            # add more delay for older macOS
            sec = slow_mac_factor*sec
    logger.debug(f"delay {sec}s")
    time.sleep(sec)


def set_disp_brightness(val: float = None):
    """Set the display brightness between [0,1] using this utility:
    https://github.com/nriley/brightness"""
    if val is None and not isinstance(val, int) and not isinstance(val, float):
        logger.debug("display brightness will not be touched")
        return
    if val < 0:
        logger.warning(f"brightness value cannot be less than 0. got {val}")
        val = 0
    elif val > 1:
        logger.warning(f"brightness value cannot be greater than 1. got {val}")
        val = 1
    
    if is_tool("brightness"):
        logger.debug(f"setting display brightness to {val}")
        os.system(f"brightness {val}")


def is_tool(name: str) -> bool:
    """Check whether `name` is on PATH and marked as executable."""
    return shutil.which(name) is not None
