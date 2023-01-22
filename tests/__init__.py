# add workspace dir to system path, otherwise cannot import project modules
import os
import sys
proj_root_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.pardir
)
sys.path.append(proj_root_path)

from zipfile import ZipFile

from pokemon import SpriteType

TEST_FILES_DIR = os.path.join("tests", "test_files")
TEST_IMG_DIR = os.path.join(TEST_FILES_DIR, "test_images")
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
]
ITEM_LIST = [
    {'name': 'ball', 'item_1': 'masterball', 'item_2': 'greatball', 'item_3': 'pokeball', 'item_4': 'ultraball', 'item_5': None},
    {'name': 'ball1', 'item_1': 'greatball', 'item_2': None, 'item_3': None, 'item_4': None, 'item_5': None},
    {'name': 'key', 'item_1': 'squirtbottle', 'item_2': 'redscale', 'item_3': 'basementkey', 'item_4': 'cardkey', 'item_5': 'clearbell'},
    {'name': 'tm', 'item_1': 'dynamicpunch', 'item_2': 'rollout', 'item_3': 'irontail', 'item_4': 'dragonbreath', 'item_5': 'shadowball'}
    ]

# check if zipfile requires unzipping
with ZipFile(os.path.join(TEST_FILES_DIR, "test_images.zip"), 'r') as zip:
    if not os.path.exists(TEST_IMG_DIR):
        zip.extractall(path=TEST_FILES_DIR)
