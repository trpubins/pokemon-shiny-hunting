import click

import __init__

from pokemon import Pokemon
from notifications import (
    USERNAME, 
    RECEIVER_EMAIL, 
    send_notification
)
from helpers import test_util
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

from tests.__init__ import TEST_IMG_DIR
MODULE = "notifications.py"


def test_1_get_name():
    logger.info("Test 1 - Get Username")
    logger.info(f"Hello {USERNAME}")
    logger.info("Test 1 - success!")


def test_2_get_pic():
    logger.info("Test 2 - Import Image")
    pokemon = Pokemon("Farfetch'd")
    send_notification(RECEIVER_EMAIL, pokemon, send=True)
    logger.info("Test 2 - success!")


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