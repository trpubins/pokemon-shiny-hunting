"""Manage folder navigation and file operations."""

from contextlib import contextmanager
import logging
import os
import shutil
from tempfile import gettempdir, mkdtemp
from typing import Iterator, List
from zipfile import ZipFile

from helpers.platform import Platform
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


@contextmanager
def cd(dir: str) -> Iterator[None]:
    """Context manager to work in separate directory.

    Provisions directory, changes to it, and returns once context is complete.

    >>> os.chdir('/home')
    >>> with cd():
    >>>     # do stuff or
    >>>     raise Exception("There's no place like home.")
    >>> # Directory is now back to '/home'
    """
    try:
        prev_dir = os.getcwd()
    except FileNotFoundError:
        prev_dir = gettempdir()
        logger.warning(f"Unable to get current working directory, using {prev_dir}")
    
    if not os.path.isdir(dir):
        raise NotADirectoryError(f"Must provide a valid directory. Invalid dir: {dir}")
    
    logger.debug(f"change to directory: {dir}")
    os.chdir(dir)
    try:
        yield
    finally:
        os.chdir(prev_dir)


def extract_zipfiles(zipfiles: List[str]):
    """Extract contents from the provided list of zipfiles
    if not already unzipped. Will extract contents into
    directory sharing same name as the zipfile."""
    for zip_fn in zipfiles:
        zip_dir, _ = zip_fn.split(".")
        with ZipFile(zip_fn, 'r') as zip:
            if not os.path.exists(zip_dir):
                zip.extractall(path=os.path.join(zip_dir, os.path.pardir))
                logger.debug(f"unzipped {zip_fn}")
            else:
                logger.debug(f"contents already unzipped for {zip_fn}")
