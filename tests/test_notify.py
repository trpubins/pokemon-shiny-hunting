import os

import click
import __init__
from notifications import (
    USERNAME, 
    RECEIVER_EMAIL, 
    send_notification
)
from test_image import POKEMON
from __init__ import TEST_IMG_DIR


from helpers import test_util
from helpers.opencv_util import compare_img_pixels
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

MODULE = "notifications.py"

def test_1_get_name():
    logger.info("Test 1 - Get Username")
    logger.info(f"Hello {USERNAME}")
    logger.info("Test 1 - success!")

def test_2_get_pic():
    logger.info("Test 2 - Import Image")
    img = os.path.join(TEST_IMG_DIR, f"battle_img_1.png")


@click.command()
@click.option("-n", "--test-number", required=False, type=int,
              help="The test number to run.")
def run_tests(test_number: int = None):
    logger.info(f"----- Testing {MODULE} -----")
    
    if test_number is None:
        test_util.run_tests(module_name=__name__)
    else:
        try:
            test_util.run_tests(module_name=__name__, test_number=test_number)
        except ValueError as e:
            logger.error(f"Invalid test_number specified: {test_number}")
            raise e
    logger.info("----- All tests pass! -----")

if __name__ == "__main__":
    run_tests()