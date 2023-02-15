import os

import click
import cv2

import __init__
from emulator import Emulator
from image import compare_img_pixels, get_latest_screenshot_fn
from helpers import test_util
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

from tests.__init__ import TEST_IMG_DIR

MODULE = "emulator.py"
PICTURES = [
    os.path.join(TEST_IMG_DIR, "Pokegear_page_1.png"),
    os.path.join(TEST_IMG_DIR, "Pokegear_page_2.png"),
    os.path.join(TEST_IMG_DIR, "options.png"),
    os.path.join(TEST_IMG_DIR, "party.png"),
    os.path.join(TEST_IMG_DIR, "pokedex.png"),
]
EMULATOR = Emulator()


def test_1_pokegear_page_1():
    """Move to pokegear_page_1"""
    logger.info("Test 1 - pokegear_page_1")
    test_number = 1
    pokegear_page_1_img = cv2.imread(PICTURES[test_number-1])
    EMULATOR.press_start()
    EMULATOR.move_down(presses=3)
    EMULATOR.press_a(delay_after_press=0.2)
    EMULATOR.take_screenshot()
    screenshot = get_latest_screenshot_fn()
    test_img = cv2.imread(screenshot)
    base_comp = compare_img_pixels(test_img, pokegear_page_1_img)
    _assert_emulator_navigation(test_img, base_comp, screenshot)
    logger.info("Test 1 - Success")


def test_2_pokegear_page_2():
    """Move to pokegear_page_2"""
    logger.info("Test 2 - pokegear_page_2")
    test_number = 2
    pokegear_page_1_img = cv2.imread(PICTURES[test_number-2])
    pokegear_page_2_img = cv2.imread(PICTURES[test_number-1])
    EMULATOR.move_right_precise(presses=2, delay_after_press=0.2)
    EMULATOR.take_screenshot()
    screenshot_2 = get_latest_screenshot_fn()
    test_img_2 = cv2.imread(screenshot_2)
    base_comp_2 = compare_img_pixels(test_img_2, pokegear_page_2_img)
    _assert_emulator_navigation(test_img_2, base_comp_2, screenshot_2)

    # move back to pokegear_page_1
    EMULATOR.move_left_precise(presses=2, delay_after_press=0.2)
    EMULATOR.take_screenshot()
    screenshot_1 = get_latest_screenshot_fn()
    test_img_1 = cv2.imread(screenshot_1)
    base_comp_1 = compare_img_pixels(test_img_1, pokegear_page_1_img)
    _assert_emulator_navigation(test_img_1, base_comp_1, screenshot_1)
    logger.info("Test 2 - success")


def test_3_options():
    """Move to options"""
    logger.info("Test 3 - options")
    test_number = 3
    options_img = cv2.imread(PICTURES[test_number-1])    
    EMULATOR.press_b(delay_after_press=0.2)
    EMULATOR.move_down(presses=3, delay_after_press=0.2)
    EMULATOR.press_a(delay_after_press=0.2)
    EMULATOR.take_screenshot()
    screenshot = get_latest_screenshot_fn()
    test_img = cv2.imread(screenshot)
    base_comp = compare_img_pixels(test_img, options_img)
    _assert_emulator_navigation(test_img, base_comp, screenshot)
    logger.info("Test 3 - success")


def test_4_pokemon_party():
    """Move to Pokémon party"""
    logger.info("Test 4 - pokemon_party")
    test_number = 4
    poke_party_img = cv2.imread(PICTURES[test_number-1])    
    EMULATOR.press_b(delay_after_press=0.2)
    EMULATOR.move_down(presses=3, delay_after_press=0.2)
    EMULATOR.press_a(delay_after_press=0.2)
    EMULATOR.take_screenshot()
    screenshot = get_latest_screenshot_fn()
    test_img = cv2.imread(screenshot)
    base_comp = compare_img_pixels(test_img, poke_party_img)
    _assert_emulator_navigation(test_img, base_comp, screenshot)
    logger.info("Test 4 - success")


def test_5_pokedex():
    """Move to Pokédex"""
    logger.info("Test 5 - pokedex")
    test_number = 5
    pokedex_img = cv2.imread(PICTURES[test_number-1])    
    EMULATOR.press_b(delay_after_press=0.2)
    EMULATOR.move_up(delay_after_press=0.2)
    EMULATOR.press_a(delay_after_press=0.2)
    EMULATOR.take_screenshot()
    screenshot = get_latest_screenshot_fn()
    test_img = cv2.imread(screenshot)
    base_comp = compare_img_pixels(test_img, pokedex_img)
    _assert_emulator_navigation(test_img, base_comp, screenshot)
    logger.info("Test 5 - success")


def _assert_emulator_navigation(test_img: cv2.Mat, base_comp: float, screenshot: str) -> bool:
    """Assert that the emulator navigated to the correct destination.
    In other words, verify no other image comparted with test_img is
    more similar to the base comparison."""
    try:
        for pic in PICTURES:
            verified_img = cv2.imread(pic)
            new_comp = compare_img_pixels(test_img, verified_img)
            assert(new_comp >= base_comp)
    except AssertionError as e:
        logger.error("button sequence not aligned")
        EMULATOR.kill_process()
        raise e
    finally:
        # clean up
        os.remove(screenshot)


@click.command()
def run_tests():
    logger.info(f"----- Testing {MODULE} -----")
    
    # launch and continue game **before** running these tests
    EMULATOR.launch_game()
    EMULATOR.continue_pokemon_game()

    # each test is dependent on controller presses from
    # previous test so required to always run all tests in this test
    test_util.run_tests(module_name=__name__)
    
    EMULATOR.kill_process()
    logger.info("----- All tests pass! -----")


if __name__ == "__main__":
    run_tests()
