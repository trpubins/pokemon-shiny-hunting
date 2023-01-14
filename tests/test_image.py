import os

import click
import cv2

import __init__

from dex import gen_2_dex
from image import (
    crop_name_in_battle,
    crop_pokemon_in_battle,
    determine_name,
    determine_sprite_type,
)
from pokemon import Pokemon, SpriteType
from helpers import test_util
from helpers.opencv_util import compare_img_pixels
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

from tests.__init__ import POKEMON_LIST, TEST_IMG_DIR
MODULE = "image.py"
POKEMON_GAME = "Crystal"


def test_1_verify_sprite_images_exist():
    logger.info("Test 1 - verify_sprite_images_exist")
    dex = gen_2_dex()
    for _, row in dex.iterrows():
        name = row.get("NAME")
        pokemon = Pokemon(name)
        normal_fn = pokemon.get_normal_img_fn()
        shiny_fn = pokemon.get_shiny_img_fn()
        assert(os.path.exists(normal_fn))
        logger.debug(f"{normal_fn} exists")
        assert(os.path.exists(shiny_fn))
        logger.debug(f"{shiny_fn} exists")
    logger.info("Test 1 - success!")


def test_2_crop_pokemon_in_battle():
    logger.info("Test 2 - crop_pokemon_in_battle")
    for i in range(3):
        n = i + 1
        input_img_fn = os.path.join(TEST_IMG_DIR, f"battle_img_{n}.png")
        output_img_fn = os.path.join(TEST_IMG_DIR, f"cropped_poke_battle_img_{n}.png")
        cropped_img = crop_pokemon_in_battle(input_img_fn, del_png=False)
        correct_img = cv2.imread(output_img_fn)
        assert(compare_img_pixels(cropped_img, correct_img) == 0)
    logger.info("Test 2 - success!")


def test_3_determine_sprite_type():
    logger.info("Test 3 - determine_sprite_type")
    for pokemon_obj in POKEMON_LIST[:3]:
        n: int = pokemon_obj["test_img_num"]
        type_: SpriteType = pokemon_obj["sprite_type"]
        pokemon = Pokemon(pokemon_obj["name"])
        input_img_fn = os.path.join(TEST_IMG_DIR, f"cropped_poke_battle_img_{n}.png")
        input_img = cv2.imread(input_img_fn)
        sprite_type = determine_sprite_type(pokemon, img=input_img)
        assert(sprite_type == type_)
    logger.info("Test 3 - success!")


def test_4_crop_name_in_battle():
    logger.info("Test 4 - crop_name_in_battle")
    for pokemon_obj in POKEMON_LIST[:3]:
        n: int = pokemon_obj["test_img_num"]
        pokemon = Pokemon(pokemon_obj["name"])
        input_img_fn = os.path.join(TEST_IMG_DIR, f"battle_img_{n}.png")
        letter_imgs = crop_name_in_battle(input_img_fn)
        assert(len(letter_imgs) == len(pokemon.name))
    logger.info("Test 4 - success!")


def test_5_determine_name():
    logger.info("Test 5 - determine_name")
    name = "Gyarados"
    letter_imgs = list()
    for i,char in enumerate(name):
        input_img_fn = os.path.join(TEST_IMG_DIR, f"char_{i}.png")
        input_img = cv2.imread(input_img_fn)
        letter_imgs.append(input_img)
    pokemon_name = determine_name(letter_imgs)
    assert(pokemon_name == name.lower())
    logger.info("Test 5 - success!")


def test_6_determine_name_full():
    logger.info("Test 6 - determine_name_full")
    for pokemon_obj in POKEMON_LIST:
        n: int = pokemon_obj["test_img_num"]
        name: str = pokemon_obj["name"]
        battle_img_fn = os.path.join(TEST_IMG_DIR, f"battle_img_{n}.png")
        letter_imgs = crop_name_in_battle(battle_img_fn)
        pokemon_name = determine_name(letter_imgs)
        assert(pokemon_name == name.lower())
    logger.info("Test 6 - success!")


def test_7_determine_sprite_type_full():
    logger.info("Test 7 - determine_sprite_type_full")
    for pokemon_obj in POKEMON_LIST:
        n: int = pokemon_obj["test_img_num"]
        type_: SpriteType = pokemon_obj["sprite_type"]
        pokemon = Pokemon(pokemon_obj["name"])
        battle_img_fn = os.path.join(TEST_IMG_DIR, f"battle_img_{n}.png")
        letter_imgs = crop_name_in_battle(battle_img_fn)
        pokemon_name = determine_name(letter_imgs)
        assert(pokemon_name == pokemon.name.lower())
        sprite_img = crop_pokemon_in_battle(battle_img_fn, del_png=False)
        sprite_type = determine_sprite_type(pokemon, img=sprite_img)
        assert(sprite_type == type_)
    logger.info("Test 7 - success!")


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