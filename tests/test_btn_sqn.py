import os

import cv2

import __init__
from tests.__init__ import TEST_IMG_DIR
from helpers.common import delay
from helpers.log import get_logger, mod_fname

from emulator import Emulator
from image import compare_img_pixels, get_latest_screenshot_fn
logger = get_logger(mod_fname(__file__))

PICTURES = ["Pokegear_page_1.png", "Pokegear_page_2.png", "options.png", "party.png", "pokedex.png"]
for pic in range(len(PICTURES)):
    PICTURES[pic] = os.path.join(TEST_IMG_DIR, PICTURES[pic])

def test_btn_sqn():
    em = Emulator()
    em.launch_game()
    em.continue_pokemon_game()
    em.press_start()
    em.move_down(presses=3)
    em.press_a()
    '''1 - Test should be pokegear_page_1'''
    em.take_screenshot()
    test1 = get_latest_screenshot_fn()
    test1_pic = cv2.imread(test1)
    control1 = cv2.imread(PICTURES[0])
    base = compare_img_pixels(test1_pic, control1)
    for i in range(len(PICTURES)):
        if compare_img_pixels(test1_pic, cv2.imread(PICTURES[i])) < base:
            logger.info("button sequence not aligned")
            em.kill_process()
    logger.info("Test 1 - Success")
    '''2 - Moving Back to pokegear_page_1'''
    em.move_right_precise(presses=2, delay_after_press=delay(0.2))
    em.move_left_precise(presses=2, delay_after_press=delay(0.2))
    em.take_screenshot()
    test2 = get_latest_screenshot_fn()
    test2_pic = cv2.imread(test2)
    base1 = compare_img_pixels(test2_pic, control1)
    assert(base == base1)
    logger.info("Test 2 - success")
    '''3 - Moving into options'''
    em.press_b(delay_after_press=delay(0.2))
    em.move_down(presses=3, delay_after_press=delay(0.2))
    em.press_a(delay_after_press=delay(0.2))
    em.take_screenshot()
    test3 = get_latest_screenshot_fn()
    test3_pic = cv2.imread(test3)
    control2 = cv2.imread(PICTURES[2])
    base2 = compare_img_pixels(test3_pic, control2)
    for i in range(len(PICTURES)):
        if compare_img_pixels(test3_pic, cv2.imread(PICTURES[i])) < base2:
            logger.info("button sequence not aligned")
            em.kill_process()
    logger.info("Test 3 - success")
    '''4 - Moving up to Party'''
    em.press_b(delay_after_press=delay(0.2))
    em.move_down(presses=3, delay_after_press=delay(0.2))
    em.press_a(delay_after_press=delay(0.2))
    em.take_screenshot()
    test4 = get_latest_screenshot_fn()
    test4_pic = cv2.imread(test4)
    control3 = cv2.imread(PICTURES[3])
    base3 = compare_img_pixels(test4_pic, control3)
    for i in range(len(PICTURES)):
        if compare_img_pixels(test4_pic, cv2.imread(PICTURES[i])) < base3:
            logger.info("button sequence not aligned")
            em.kill_process()
    logger.info("Test 4 - success")
    '''5 - Moving up to Pokedex'''
    em.press_b(delay_after_press=delay(0.2))
    em.move_up(delay_after_press=delay(0.2))
    em.press_a(delay_after_press=delay(0.2))
    em.take_screenshot()
    test5 = get_latest_screenshot_fn()
    test5_pic = cv2.imread(test5)
    control4 = cv2.imread(PICTURES[4])
    base4 = compare_img_pixels(test5_pic, control4)
    for i in range(len(PICTURES)):
        if compare_img_pixels(test5_pic, cv2.imread(PICTURES[i])) < base4:
            logger.info("button sequence not aligned")
            em.kill_process()
    logger.info("Test 5 - success")
    logger.info("All tests - success!")
    em.kill_process()
    os.remove(test1)
    os.remove(test2)
    os.remove(test3)
    os.remove(test4)
    os.remove(test5)


if __name__ == "__main__":
    test_btn_sqn()