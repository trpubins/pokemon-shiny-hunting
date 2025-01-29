import os

import pytest

from helpers.log import get_logger

from conftest import get_json_files, print_section_break

# ----------------------------------------------------------------------------#
#                               --- Globals ---                               #
# ----------------------------------------------------------------------------#
from __setup__ import TEST_EVENTS_PATH, TEST_IMG_DIR

MODULE = "image"
MODULE_EVENTS_DIR = os.path.join(TEST_EVENTS_PATH, MODULE)

# ----------------------------------------------------------------------------#
#                               --- Logging ---                               #
# ----------------------------------------------------------------------------#
logger = get_logger(f"test_{MODULE}")

# ----------------------------------------------------------------------------#
#                           --- Module Imports ---                            #
# ----------------------------------------------------------------------------#
from image import (  # noqa: E402
    cv2,
    MenuType,
    compare_img_pixels,
    crop_name_in_battle,
    crop_pokemon_in_battle,
    determine_letter,
    determine_menu,
    determine_name,
    determine_pack_items,
    determine_sprite_type,
    get_latest_png_fn,
)
from dex import gen_2_dex  # noqa: E402
from pokemon import Pokemon, SpriteType  # noqa: E402


# ----------------------------------------------------------------------------#
#                                --- TESTS ---                                #
# ----------------------------------------------------------------------------#
@pytest.mark.happy
def test_00_verify_sprite_images_exist():
    print_section_break()
    logger.info("Test Description: Verify sprite images exist")
    dex = gen_2_dex()
    for _, row in dex.iterrows():
        name = row.get("NAME")
        pokemon = Pokemon(name)
        normal_fn = pokemon.get_normal_img_fn()
        shiny_fn = pokemon.get_shiny_img_fn()
        assert os.path.exists(normal_fn)
        logger.debug(f"{normal_fn} exists")
        assert os.path.exists(shiny_fn)
        logger.debug(f"{shiny_fn} exists")


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file", get_json_files(MODULE_EVENTS_DIR, ["crop_pokemon_in_battle"])
)
def test_01_crop_pokemon_in_battle(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    battle_img_fn: str = os.path.join(TEST_IMG_DIR, get_event_as_dict["input"]["image"])
    expected_img_fn: str = os.path.join(
        TEST_IMG_DIR, get_event_as_dict["expected_output"]["image"]
    )

    cropped_img = crop_pokemon_in_battle(battle_img_fn, del_png=False)
    expected_img = cv2.imread(expected_img_fn)
    assert compare_img_pixels(cropped_img, expected_img) == 0


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file", get_json_files(MODULE_EVENTS_DIR, ["crop_name_in_battle"])
)
def test_02_crop_name_in_battle(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    battle_img_fn: str = os.path.join(TEST_IMG_DIR, get_event_as_dict["input"]["image"])
    pokemon = Pokemon(get_event_as_dict["input"]["pokemon_name"])

    letter_imgs = crop_name_in_battle(battle_img_fn)
    assert len(letter_imgs) == len(pokemon.name)


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file", get_json_files(MODULE_EVENTS_DIR, ["determine_letter"])
)
def test_03_determine_letter(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    char_img_fn: str = os.path.join(TEST_IMG_DIR, get_event_as_dict["input"]["image"])
    expected_output: str = get_event_as_dict["expected_output"]["letter"]

    char_img = cv2.imread(char_img_fn)
    letter = determine_letter(char_img)
    assert letter == expected_output


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file", get_json_files(MODULE_EVENTS_DIR, ["determine_name"])
)
def test_04_determine_name(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    battle_img_fn: str = os.path.join(TEST_IMG_DIR, get_event_as_dict["input"]["image"])
    expected_output: str = get_event_as_dict["expected_output"]

    letter_imgs = crop_name_in_battle(battle_img_fn)
    pokemon_name = determine_name(letter_imgs)
    assert pokemon_name == expected_output


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file", get_json_files(MODULE_EVENTS_DIR, ["determine_sprite_type"])
)
def test_05_determine_sprite_type(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    input_img_fn: str = os.path.join(TEST_IMG_DIR, get_event_as_dict["input"]["image"])
    pokemon = Pokemon(get_event_as_dict["input"]["pokemon_name"])
    expected_output = SpriteType(get_event_as_dict["expected_output"])

    input_img = cv2.imread(input_img_fn)
    sprite_type = determine_sprite_type(pokemon, img=input_img)
    assert sprite_type == expected_output


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["determine_sprite_type_from_battle"]),
)
def test_06_determine_sprite_type_from_battle(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    battle_img_fn: str = os.path.join(TEST_IMG_DIR, get_event_as_dict["input"]["image"])
    pokemon = Pokemon(get_event_as_dict["input"]["pokemon_name"])
    expected_output = SpriteType(get_event_as_dict["expected_output"])

    sprite_img = crop_pokemon_in_battle(battle_img_fn, del_png=False)
    sprite_type = determine_sprite_type(pokemon, img=sprite_img)
    assert sprite_type == expected_output


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file", get_json_files(MODULE_EVENTS_DIR, ["determine_menu"])
)
def test_07_determine_menu(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    menu_img_fn: str = os.path.join(TEST_IMG_DIR, get_event_as_dict["input"]["image"])
    expected_output = MenuType(get_event_as_dict["expected_output"])

    menu = determine_menu(menu_img_fn)
    assert menu == expected_output


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file", get_json_files(MODULE_EVENTS_DIR, ["determine_pack_items"])
)
def test_08_determine_pack_items(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    input_img_fn = os.path.join(TEST_IMG_DIR, get_event_as_dict["input"]["image"])
    get_qty = get_event_as_dict["input"]["get_qty"]
    expected_outputs = get_event_as_dict["expected_output"]

    items = determine_pack_items(input_img_fn, get_qty=get_qty, del_png=True)
    for (det_item_name, det_item_qty), expected_output in zip(
        items, expected_outputs
    ):
        assert det_item_name == expected_output["name"]
        assert det_item_qty == expected_output["qty"]


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file", get_json_files(MODULE_EVENTS_DIR, ["get_latest_png_fn"])
)
def test_09_get_latest_png_fn(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    expected_output = get_event_as_dict["expected_output"]
    
    screenshot_fn = get_latest_png_fn(TEST_IMG_DIR)
    assert os.path.basename(screenshot_fn) == expected_output