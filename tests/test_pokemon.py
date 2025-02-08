import os

import pytest

from helpers.log import get_logger

from conftest import get_json_files, print_section_break

# ----------------------------------------------------------------------------#
#                               --- Globals ---                               #
# ----------------------------------------------------------------------------#
from __setup__ import TEST_EVENTS_PATH

MODULE = "pokemon"
MODULE_EVENTS_DIR = os.path.join(TEST_EVENTS_PATH, MODULE)

# ----------------------------------------------------------------------------#
#                               --- Logging ---                               #
# ----------------------------------------------------------------------------#
logger = get_logger(f"test_{MODULE}")

# ----------------------------------------------------------------------------#
#                           --- Module Imports ---                            #
# ----------------------------------------------------------------------------#
from pokemon import (  # noqa: E402
    SPRITES_DIR,
    SpriteType,
    create_pokemon_sprite_fn,
    get_sprite_name,
)


# ----------------------------------------------------------------------------#
#                                --- TESTS ---                                #
# ----------------------------------------------------------------------------#
@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file", get_json_files(MODULE_EVENTS_DIR, ["get_sprite_name"])
)
def test_01_get_sprite_name(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    name: str = get_event_as_dict["input"]["name"]
    expected_output: str = get_event_as_dict["expected_output"]
    
    sprite_name = get_sprite_name(name)
    assert (sprite_name == expected_output)


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file", get_json_files(MODULE_EVENTS_DIR, ["create_pokemon_sprite_fn"])
)
def test_02_create_pokemon_sprite_fn(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    game: str = get_event_as_dict["input"]["game"]
    name: str = get_event_as_dict["input"]["name"]
    _type: str = get_event_as_dict["input"]["type"]
    expected_output: str = get_event_as_dict["expected_output"]
    
    sprite_fn = create_pokemon_sprite_fn(game, name, _type=SpriteType(_type))
    assert (sprite_fn == os.path.join(SPRITES_DIR, expected_output))
