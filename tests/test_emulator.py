import os

import pytest

from config import RETROARCH_CFG
from helpers.log import get_logger
from image import cv2, compare_img_pixels, get_latest_png_fn

from conftest import get_json_files, print_section_break

# ----------------------------------------------------------------------------#
#                               --- Globals ---                               #
# ----------------------------------------------------------------------------#
from __setup__ import TEST_EVENTS_PATH, TEST_IMG_DIR

MODULE = "emulator"
MODULE_EVENTS_DIR = os.path.join(TEST_EVENTS_PATH, MODULE)

# ----------------------------------------------------------------------------#
#                               --- Logging ---                               #
# ----------------------------------------------------------------------------#
logger = get_logger(f"test_{MODULE}")

# ----------------------------------------------------------------------------#
#                           --- Module Imports ---                            #
# ----------------------------------------------------------------------------#
from emulator import (  # noqa: E402
    Emulator,
)

EMULATOR = Emulator()


# ----------------------------------------------------------------------------#
#                                --- TESTS ---                                #
# ----------------------------------------------------------------------------#
@pytest.mark.happy
@pytest.mark.emulator
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file", get_json_files(MODULE_EVENTS_DIR, ["emulator"])
)
def test_01_emulator(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")

    # launch and continue game **before** running these tests
    EMULATOR.launch_game()
    EMULATOR.continue_pokemon_game()

    # each test is dependent on controller presses from
    # previous test so required to always run all tests in this test
    assert_1_pokegear_page_1()
    assert_2_pokegear_page_2()
    assert_3_options()
    assert_4_pokemon_party()
    assert_5_pokedex()

    EMULATOR.kill_process()


# ----------------------------------------------------------------------------#
#                               --- HELPERS ---                               #
# ----------------------------------------------------------------------------#
def assert_1_pokegear_page_1():
    """Move to pokegear_page_1"""
    logger.info("Emulator assertion 1/5 - pokegear_page_1")
    pokegear_page_1_img = cv2.imread(os.path.join(TEST_IMG_DIR, "Pokegear_page_1.png"))
    EMULATOR.press_start()
    EMULATOR.move_down(presses=3)
    EMULATOR.press_a(delay_after_press=0.2)
    EMULATOR.take_screenshot()
    screenshot = get_latest_png_fn(RETROARCH_CFG.screenshot_dir)
    test_img = cv2.imread(screenshot)
    base_comp = compare_img_pixels(test_img, pokegear_page_1_img)
    _assert_emulator_navigation(test_img, base_comp, screenshot)
    logger.info("Emulator assertion 1/5 - Success")


def assert_2_pokegear_page_2():
    """Move to pokegear_page_2"""
    logger.info("Emulator assertion 2/5 - pokegear_page_2")
    pokegear_page_1_img = cv2.imread(os.path.join(TEST_IMG_DIR, "Pokegear_page_1.png"))
    pokegear_page_2_img = cv2.imread(os.path.join(TEST_IMG_DIR, "Pokegear_page_2.png"))
    EMULATOR.move_right_precise(presses=2, delay_after_press=0.2)
    EMULATOR.take_screenshot()
    screenshot_2 = get_latest_png_fn(RETROARCH_CFG.screenshot_dir)
    test_img_2 = cv2.imread(screenshot_2)
    base_comp_2 = compare_img_pixels(test_img_2, pokegear_page_2_img)
    _assert_emulator_navigation(test_img_2, base_comp_2, screenshot_2)

    # move back to pokegear_page_1
    EMULATOR.move_left_precise(presses=2, delay_after_press=0.2)
    EMULATOR.take_screenshot()
    screenshot_1 = get_latest_png_fn(RETROARCH_CFG.screenshot_dir)
    test_img_1 = cv2.imread(screenshot_1)
    base_comp_1 = compare_img_pixels(test_img_1, pokegear_page_1_img)
    _assert_emulator_navigation(test_img_1, base_comp_1, screenshot_1)
    logger.info("Emulator assertion 2/5 - success")


def assert_3_options():
    """Move to options"""
    logger.info("Emulator assertion 3/5 - options")
    options_img = cv2.imread(os.path.join(TEST_IMG_DIR, "options.png"))
    EMULATOR.press_b(delay_after_press=0.2)
    EMULATOR.move_down(presses=3, delay_after_press=0.2)
    EMULATOR.press_a(delay_after_press=0.2)
    EMULATOR.take_screenshot()
    screenshot = get_latest_png_fn(RETROARCH_CFG.screenshot_dir)
    test_img = cv2.imread(screenshot)
    base_comp = compare_img_pixels(test_img, options_img)
    _assert_emulator_navigation(test_img, base_comp, screenshot)
    logger.info("Emulator assertion 3/5 - success")


def assert_4_pokemon_party():
    """Move to Pokémon party"""
    logger.info("Emulator assertion 4/5 - pokemon_party")
    poke_party_img = cv2.imread(os.path.join(TEST_IMG_DIR, "party.png"))
    EMULATOR.press_b(delay_after_press=0.2)
    EMULATOR.move_down(presses=3, delay_after_press=0.2)
    EMULATOR.press_a(delay_after_press=0.2)
    EMULATOR.take_screenshot()
    screenshot = get_latest_png_fn(RETROARCH_CFG.screenshot_dir)
    test_img = cv2.imread(screenshot)
    base_comp = compare_img_pixels(test_img, poke_party_img)
    _assert_emulator_navigation(test_img, base_comp, screenshot)
    logger.info("Emulator assertion 4/5 - success")


def assert_5_pokedex():
    """Move to Pokédex"""
    logger.info("Emulator assertion 5/5 - pokedex")
    pokedex_img = cv2.imread(os.path.join(TEST_IMG_DIR, "pokedex.png"))
    EMULATOR.press_b(delay_after_press=0.2)
    EMULATOR.move_up(delay_after_press=0.2)
    EMULATOR.press_a(delay_after_press=0.2)
    EMULATOR.take_screenshot()
    screenshot = get_latest_png_fn(RETROARCH_CFG.screenshot_dir)
    test_img = cv2.imread(screenshot)
    base_comp = compare_img_pixels(test_img, pokedex_img)
    _assert_emulator_navigation(test_img, base_comp, screenshot)
    logger.info("Emulator assertion 5/5 - success")


def _assert_emulator_navigation(
    test_img: cv2.Mat, base_comp: float, screenshot: str
) -> bool:
    """Assert that the emulator navigated to the correct destination.
    In other words, verify no other image comparted with test_img is
    more similar to the base comparison."""
    PICTURES = [
        os.path.join(TEST_IMG_DIR, "Pokegear_page_1.png"),
        os.path.join(TEST_IMG_DIR, "Pokegear_page_2.png"),
        os.path.join(TEST_IMG_DIR, "options.png"),
        os.path.join(TEST_IMG_DIR, "party.png"),
        os.path.join(TEST_IMG_DIR, "pokedex.png"),
    ]
    try:
        for pic in PICTURES:
            verified_img = cv2.imread(pic)
            new_comp = compare_img_pixels(test_img, verified_img)
            assert new_comp >= base_comp
    except AssertionError as e:
        logger.error("button sequence not aligned")
        EMULATOR.kill_process()
        raise e
    finally:
        # clean up
        os.remove(screenshot)
