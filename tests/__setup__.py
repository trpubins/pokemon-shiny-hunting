import configparser
import os
import sys
from zipfile import ZipFile

# add service and lambdas dir to system path, otherwise cannot import modules
PROJ_ROOT_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.pardir
)
sys.path.append(PROJ_ROOT_PATH)

# test file paths
TESTS_PATH = os.path.join(PROJ_ROOT_PATH, "tests")
TEST_EVENTS_PATH = os.path.join(TESTS_PATH, "events")
TEST_FILES_PATH = os.path.join(TESTS_PATH, "files")
TEST_IMG_DIR = os.path.join(TEST_FILES_PATH, "test_images")

# parse config.ini file if it exists to support aws-cli authentication
CONFIG_INI_PATH = os.path.join(TESTS_PATH, "config.ini")
if os.path.isfile(CONFIG_INI_PATH):
    config = configparser.RawConfigParser()
    config.read(CONFIG_INI_PATH)
    config_dict = dict(config.items("main"))
    for k, v in config_dict.items():
        os.environ[k.upper()] = v

# check if zipfile requires unzipping
with ZipFile(f"{TEST_IMG_DIR}.zip", 'r') as zip:
    if not os.path.exists(TEST_IMG_DIR):
        zip.extractall(path=TEST_FILES_PATH)

from pokemon import SpriteType  # noqa: E402
POKEMON_LIST = [
    { "test_img_num":  1, "name":   "Gyarados", "sprite_type":  SpriteType.SHINY },
    { "test_img_num":  2, "name":   "Gyarados", "sprite_type":  SpriteType.SHINY },
    { "test_img_num":  3, "name":   "Gyarados", "sprite_type":  SpriteType.SHINY },
    { "test_img_num":  4, "name":    "Sentret", "sprite_type": SpriteType.NORMAL },
    { "test_img_num":  5, "name":    "Rattata", "sprite_type": SpriteType.NORMAL },
    { "test_img_num":  6, "name":     "Pidgey", "sprite_type": SpriteType.NORMAL },
    { "test_img_num":  7, "name": "Bellsprout", "sprite_type": SpriteType.NORMAL },
    { "test_img_num":  8, "name":      "Zubat", "sprite_type": SpriteType.NORMAL },
    { "test_img_num":  9, "name":    "Spearow", "sprite_type": SpriteType.NORMAL },
    { "test_img_num": 10, "name":    "Metapod", "sprite_type": SpriteType.NORMAL },
    { "test_img_num": 11, "name":     "Weedle", "sprite_type": SpriteType.NORMAL },
    { "test_img_num": 12, "name":     "Vulpix", "sprite_type": SpriteType.NORMAL },
    { "test_img_num": 13, "name":  "Nidoran M", "sprite_type": SpriteType.NORMAL },
    { "test_img_num": 14, "name":  "Nidoran F", "sprite_type": SpriteType.NORMAL },
    { "test_img_num": 15, "name":   "Mr. Mime", "sprite_type": SpriteType.NORMAL },
    { "test_img_num": 16, "name": "Farfetch'd", "sprite_type": SpriteType.NORMAL },
    { "test_img_num": 17, "name":  "Sudowoodo", "sprite_type": SpriteType.NORMAL },
    { "test_img_num": 18, "name":    "Suicune", "sprite_type":  SpriteType.SHINY },
    { "test_img_num": 19, "name":      "Lugia", "sprite_type":  SpriteType.SHINY },
    { "test_img_num": 20, "name":      "Lugia", "sprite_type": SpriteType.NORMAL },
    { "test_img_num": 21, "name":      "Ho-Oh", "sprite_type":  SpriteType.SHINY },
]
