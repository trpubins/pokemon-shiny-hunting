import os

import click
import cv2

import __init__
from emulator import Emulator
from pack import Balls, BallType
from helpers import test_util
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

from tests.__init__ import TEST_IMG_DIR

MODULE = "emulator.py"
INVENTORY = [
    tuple(("masterball", 1)),
    tuple(("greatball", 38)),
    tuple(("pokeball", 7))
]
BALLS = Balls(INVENTORY)
EMULATOR = Emulator()


def test_1_id_hierarchy():
    logger.info("Test 1 - ID ball hierarchy")
    logger.info(f"current inventory: {BALLS.inventory}")
    logger.info(f"hierarchy of inventory: {BALLS.id_ball_hierarchy()}")
    assert(BALLS.id_ball_hierarchy() == {'masterball': 1, 'greatball': 3, 'pokeball': 4})
    logger.info("Test 1 - Success")


def test_2_id_best_ball():
    logger.info("Test 2 - ID best ball in inventory")
    best_ball = BALLS.id_best_ball(BALLS.id_ball_hierarchy())
    assert(best_ball == BallType.MASTER)
    logger.info("Test 2 - Success")

def test_3_highlight_best_ball():
    logger.info("Test 3 - Highlight best ball in inventory")
    highlight = BALLS.highlight_best_ball(BALLS.id_ball_hierarchy(), EMULATOR)
    assert(highlight == 0)
    logger.info("Test 3 - Success")

def test_4_throw_best_ball():
    logger.info("Test 4 - Throw best ball in inventory")
    throw = BALLS.throw_best_ball(EMULATOR)
    logger.info("Test 4 - Success")

@click.command()
def run_tests():
    logger.info(f"----- Testing {MODULE} -----")
    


    # each test is dependent on controller presses from
    # previous test so required to always run all tests in this test
    test_util.run_tests(module_name=__name__)
    
    logger.info("----- All tests pass! -----")


if __name__ == "__main__":
    run_tests()