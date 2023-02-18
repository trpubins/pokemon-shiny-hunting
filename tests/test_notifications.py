import os

import click

import __init__

from pokemon import Pokemon
from notifications import USERNAME, send_notification
from helpers import test_util
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

from tests.__init__ import TEST_IMG_DIR
MODULE = "notifications.py"


def test_1_get_username():
    logger.info("Test 1 - get_username")
    logger.info(f"Hello {USERNAME}")
    logger.info("Test 1 - success!")


def test_2_draft_email_shiny_found():
    logger.info("Test 2 - draft_email_shiny_found")
    pokemon = Pokemon("Gyarados")
    shiny_gyarados_png = os.path.join(TEST_IMG_DIR, "battle_img_2.png")
    send_notification(pokemon,
                      n_attempts=5000,
                      shiny_found=True,
                      attachments=[shiny_gyarados_png],
                      send=False)
    logger.info("Test 2 - success!")


def test_3_draft_email_shiny_not_found():
    logger.info("Test 3 - draft_email_shiny_not_found")
    pokemon = Pokemon("Charizard")
    send_notification(pokemon,
                      n_attempts=8000,
                      shiny_found=False,
                      send=False)
    logger.info("Test 3 - success!")


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