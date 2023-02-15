import __init__

import test_dex
import test_emulator
import test_image
import test_notifications
import test_opencv_util
import test_pokemon

from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))


def run_tests():
    logger.info(f"-------------------")
    logger.info(f"Testing ALL modules")
    logger.info(f"-------------------")
    test_dex.run_tests.callback()
    test_pokemon.run_tests.callback()
    test_notifications.run_tests.callback()
    test_opencv_util.run_tests.callback()
    test_image.run_tests.callback()
    test_emulator.run_tests.callback()
    logger.info("-----------------------------")
    logger.info("ALL modules passed ALL tests!")
    logger.info("-----------------------------")


if __name__ == "__main__":
    run_tests()