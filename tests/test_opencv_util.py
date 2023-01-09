import math
import os

import click
import cv2

import __init__

from helpers import test_util
from helpers.opencv_util import compare_img_color, compare_img_pixels
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

from __init__ import TEST_IMG_DIR
MODULE = os.path.join("helpers", "opencv_util.py")


def test_1_verify_same_img():
    logger.info("Test 1 - verify_same_img")
    img_fn = os.path.join(TEST_IMG_DIR, "cropped_poke_battle_img_1.png")
    img = cv2.imread(img_fn)
    img_diff = compare_img_pixels(img, img)
    assert(img_diff == 0)
    logger.info("Test 1 - success!")


def test_2_verify_diff_img():
    logger.info("Test 2 - verify_diff_img")
    img1_fn = os.path.join(TEST_IMG_DIR, "cropped_poke_battle_img_1.png")
    img2_fn = os.path.join(TEST_IMG_DIR, "cropped_poke_battle_img_2.png")
    img1 = cv2.imread(img1_fn)
    img2 = cv2.imread(img2_fn)
    img_diff = compare_img_pixels(img1, img2)
    assert(img_diff != 0)
    logger.info("Test 2 - success!")


def test_3_compare_img_color():
    logger.info("Test 3 - compare_img_color")
    img1_fn = os.path.join(TEST_IMG_DIR, "black.png")
    img2_fn = os.path.join(TEST_IMG_DIR, "white.png")
    img1 = cv2.imread(img1_fn)
    img2 = cv2.imread(img2_fn)
    img_diff = compare_img_color(img1, img2, ignore_white=False, offset_shading=False)
    assert(math.isclose(img_diff, 255*math.sqrt(3), rel_tol=1e-06))
    logger.info("Test 3 - success!")


@click.command()
@click.option("-n", "--test-number", required=False, type=int,
              help="The test number to run.")
def run_tests(test_number: int = None):
    logger.info(f"Testing {MODULE}")
    
    if test_number is None:
        test_util.run_tests(module_name=__name__)
    else:
        try:
            test_util.run_tests(module_name=__name__, test_number=test_number)
        except ValueError as e:
            logger.error(f"Invalid test_number specified: {test_number}")
            raise e
    logger.info("All tests pass!")


if __name__ == "__main__":
    run_tests()