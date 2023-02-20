import glob
import os

import click
import cv2

import __init__

from dex import gen_2_dex
from image import (
    determine_menu,
    crop_name_in_battle,
    crop_pokemon_in_battle,
    determine_name,
    determine_pack_items,
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
    for pokemon_obj in POKEMON_LIST[:16]:
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
        sprite_img = crop_pokemon_in_battle(battle_img_fn, del_png=False)
        sprite_type = determine_sprite_type(pokemon, img=sprite_img)
        assert(sprite_type == type_)
    logger.info("Test 7 - success!")


def test_8_determine_menu():
    logger.info("Test 8 - determine_menu")
    glob_pattern = os.path.join(TEST_IMG_DIR, "menu_*.png")
    menu_test_files = list(filter(os.path.isfile, glob.glob(glob_pattern)))
    for input_img_fn in menu_test_files:
        logger.debug(f"testing {os.path.basename(input_img_fn)}")
        menu = determine_menu(input_img_fn)
        logger.debug(f"Determined menu type: {menu}")
        assert(menu in input_img_fn)
    logger.info("Test 8 - success!")


def test_9_determine_pack_items():
    logger.info("Test 9 - determine_pack_items")
    pack_list = {
        "ball":  [("masterball", 1), ("greatball", 28), ("pokeball", 81), ("ultraball", 81)],
        "ball1": [("greatball", 10)],
        "ball2": [("greatball", 30), ("pokeball", 81)],
        "ball3": [("greatball", 24), ("pokeball", 75)],
        "ball4": [("greatball", 6)],
        "items": [("superpotion", 1), ("fullheal", 16), ("fullrestore", 2), ("hyperpotion", 29), ("nevermeltice", 1)],
        "key":   [("squirtbottle", None), ("redscale", None), ("basementkey", None), ("cardkey", None), ("clearbell", None)],
        "tm":    [("dynamicpunch", 1), ("rollout", 1), ("irontail", 1), ("dragonbreath", 1), ("shadowball", 1)],
        "tm1":   [("rollout", 1), ("shadowball", 1), ("mud-slap", 1), ("attract", 1), ("furycutter", 1)]
    }
    for img_name,known_items in pack_list.items():
        input_img_fn = os.path.join(TEST_IMG_DIR, f'items_{img_name}.png')
        if img_name == "key":
            # KeyItems do not contain quantities
            items = determine_pack_items(input_img_fn, get_qty=False, del_png=True)
        else:
            items = determine_pack_items(input_img_fn, get_qty=True, del_png=True)
        logger.debug(f"items: {items}")
        for (det_item_name,det_item_qty),(known_item_name,known_item_qty) \
             in zip(items,known_items):
            assert(det_item_name == known_item_name)
            assert(det_item_qty == known_item_qty)
    logger.info("Test 9 - success!")


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