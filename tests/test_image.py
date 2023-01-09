import os

import click
import cv2

import __init__

from dex import gen_2_dex
from image import (
    SPRITES_DIR,
    SpriteType,
    create_pokemon_sprite_fn,
    crop_name_in_battle,
    crop_pokemon_in_battle,
    determine_name,
    determine_sprite_type,
    get_sprite_name,
)
from helpers import test_util
from helpers.opencv_util import compare_img_pixels
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

from __init__ import TEST_IMG_DIR
MODULE = "image.py"
POKEMON_GAME = "Crystal"


def test_1_get_sprite_name():
    logger.info("Test 1 - get_sprite_name")
    assert(get_sprite_name("Nidoran F") == "nidoran-f")
    assert(get_sprite_name("Nidoran M") == "nidoran-m")
    assert(get_sprite_name("Mr. Mime") == "mr-mime")
    assert(get_sprite_name("Farfetch'd") == "farfetchd")
    logger.info("Test 1 - success!")


def test_2_create_pokemon_sprite_fn():
    logger.info("Test 2 - create_pokemon_sprite_fn")
    normal_fn = create_pokemon_sprite_fn(name="Gyarados",
                                         game=POKEMON_GAME,
                                         _type=SpriteType.NORMAL)
    assert(normal_fn == os.path.join(SPRITES_DIR, "crystal", SpriteType.NORMAL, "130_gyarados.png"))
    shiny_fn = create_pokemon_sprite_fn(name="Gyarados",
                                        game=POKEMON_GAME,
                                        _type=SpriteType.SHINY)
    assert(shiny_fn == os.path.join(SPRITES_DIR, "crystal", SpriteType.SHINY, "130_gyarados.png"))
    logger.info("Test 2 - success!")


def test_3_verify_sprite_images_exist():
    logger.info("Test 3 - verify_sprite_images_exist")
    dex = gen_2_dex()
    for _, row in dex.iterrows():            
        pokemon_name = row.get("NAME")
        normal_fn = create_pokemon_sprite_fn(name=pokemon_name,
                                             game=POKEMON_GAME,
                                             _type=SpriteType.NORMAL)
        shiny_fn = create_pokemon_sprite_fn(name=pokemon_name,
                                            game=POKEMON_GAME,
                                            _type=SpriteType.SHINY)
        assert(os.path.exists(normal_fn))
        logger.debug(f"{normal_fn} exists")
        assert(os.path.exists(shiny_fn))
        logger.debug(f"{shiny_fn} exists")
    logger.info("Test 3 - success!")


def test_4_crop_pokemon_in_battle():
    logger.info("Test 4 - crop_pokemon_in_battle")
    for i in range(3):
        n = i + 1
        input_img_fn = os.path.join(TEST_IMG_DIR, f"battle_img_{n}.png")
        output_img_fn = os.path.join(TEST_IMG_DIR, f"cropped_poke_battle_img_{n}.png")
        cropped_img = crop_pokemon_in_battle(input_img_fn, del_png=False)
        correct_img = cv2.imread(output_img_fn)
        assert(compare_img_pixels(cropped_img, correct_img) == 0)
    logger.info("Test 4 - success!")


def test_5_determine_sprite_type():
    logger.info("Test 5 - determine_sprite_type")
    for i in range(3):
        n = i + 1
        input_img_fn = os.path.join(TEST_IMG_DIR, f"cropped_poke_battle_img_{n}.png")
        input_img = cv2.imread(input_img_fn)
        sprite_type = determine_sprite_type(name="Gyarados", game=POKEMON_GAME, img=input_img)
        assert(sprite_type == SpriteType.SHINY)
    logger.info("Test 5 - success!")


def test_6_crop_name_in_battle():
    logger.info("Test 6 - crop_name_in_battle")
    for i in range(3):
        n = i + 1
        input_img_fn = os.path.join(TEST_IMG_DIR, f"battle_img_{n}.png")
        letter_imgs = crop_name_in_battle(input_img_fn, del_png=False)
        pokemon_name = "Gyarados"
        assert(len(letter_imgs) == len(pokemon_name))
    logger.info("Test 6 - success!")


def test_7_determine_name():
    logger.info("Test 7 - determine_name")
    pokemon_name = "Gyarados"
    letter_imgs = list()
    for i,char in enumerate(pokemon_name):
        input_img_fn = os.path.join(TEST_IMG_DIR, f"char_{i}.png")
        input_img = cv2.imread(input_img_fn)
        letter_imgs.append(input_img)
    name = determine_name(letter_imgs)
    assert(name.lower() == pokemon_name.lower())
    logger.info("Test 7 - success!")


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