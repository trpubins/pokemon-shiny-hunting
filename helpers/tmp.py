"""Work with temporary files."""

from contextlib import contextmanager
import logging
import os
import shutil
from tempfile import gettempdir, mkdtemp
from typing import Iterator

from helpers.common import Platform
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


if Platform.is_mac():
    os.environ["TMPDIR"] = "/tmp"


@contextmanager
def cdtmp(sub_dirname: str = None, cleanup: bool = True) -> Iterator[None]:
    """Context manager to work in temporary directory.

    Provisions directory, changes to it, then removes once context is complete.

    >>> os.chdir('/home')
    >>> with cdtmp():
    >>>     # do stuff or
    >>>     raise Exception("There's no place like home.")
    >>> # Directory is now back to '/home' and the temporary directory no longer exists
    """
    try:
        prev_dir = os.getcwd()
    except FileNotFoundError:
        prev_dir = gettempdir()
        logger.warning(f"Unable to get current working directory, using {prev_dir}")
    
    if sub_dirname is not None:
        temp_dir = os.path.join(gettempdir(), sub_dirname)
        os.makedirs(temp_dir, exist_ok=True)
    else:
        temp_dir = mkdtemp()
    logger.debug(f"temp directory: {temp_dir}")
    
    os.chdir(temp_dir)
    try:
        yield
    finally:
        os.chdir(prev_dir)
        if cleanup:
            shutil.rmtree(temp_dir, ignore_errors=True)
        logger.debug(f"deleted temp directory: {temp_dir}")
