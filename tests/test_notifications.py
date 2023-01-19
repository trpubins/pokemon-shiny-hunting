import click

import __init__

from image import get_latest_screenshot_fn
from pokemon import Pokemon
from notifications import USERNAME, send_notification
from helpers import test_util
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

MODULE = "notifications.py"


def test_1_get_username():
    logger.info("Test 1 - get_username")
    logger.info(f"Hello {USERNAME}")
    logger.info("Test 1 - success!")


def test_2_draft_email():
    logger.info("Test 2 - draft_email")
    pokemon = Pokemon("Gyarados")
    send_notification(pokemon,
                      n_attempts=5000,
                      shiny_found=True,
                      attachments=[get_latest_screenshot_fn()],
                      send=False)
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