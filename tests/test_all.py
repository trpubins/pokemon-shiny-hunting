import __init__

import test_dex
import test_image
import test_opencv_util

from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))


def run_tests():
    logger.info(f"Testing ALL modules")
    test_dex.run_tests.callback()
    test_image.run_tests.callback()
    test_opencv_util.run_tests.callback()
    logger.info("ALL modules passed ALL tests!")


if __name__ == "__main__":
    run_tests()