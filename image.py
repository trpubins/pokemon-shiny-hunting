"""Perform image transformation and image detection."""

from enum import Enum
import glob
import logging
import os
from typing import List

import cv2
from PIL import Image

from config import RETROARCH_SCREENSHOTS_DIR
from dex import get_pokemon_number
from helpers.opencv_util import ( 
    IMG_SIZE_VERY_SMALL,
    compare_img_color, compare_img_pixels,
    get_img_height, get_img_width, is_img_white
)
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


LETTERS_DIR = os.path.join("images", "letters")
SPRITES_DIR = os.path.join("images", "sprites")


class SpriteType(str, Enum):
    """Enumeration for sprite types."""
    NORMAL = "normal"
    SHINY = "shiny"


def determine_sprite_type(name: str, game: str, img: cv2.Mat) -> SpriteType:
    """Determine the sprite type based on image color comparison."""
    # retrieve db image filenames
    normal_fn = create_pokemon_sprite_fn(name, game, SpriteType.NORMAL)
    shiny_fn = create_pokemon_sprite_fn(name, game, SpriteType.SHINY)
    
    normal_img = cv2.imread(normal_fn)
    shiny_img = cv2.imread(shiny_fn)
    img = cv2.resize(img, (get_img_width(normal_img), get_img_height(normal_img)))

    # use color differences to determine sprite type
    diff_normal = compare_img_color(img, normal_img)
    diff_shiny = compare_img_color(img, shiny_img)
    if diff_normal < diff_shiny:
        sprite_type = SpriteType.NORMAL
    else:
        sprite_type = SpriteType.SHINY
    logger.debug(f"{name} is more similar to {sprite_type}")
    return sprite_type


def determine_name(letter_imgs: List[cv2.Mat]) -> str:
    """Determine the Pokémon name based on images of each letter."""
    name = str()
    for letter_img in letter_imgs:
        letter = determine_letter(letter_img)
        name += letter
    logger.debug(f"determined name: {name}")
    return name


def determine_letter(letter_img: cv2.Mat) -> str:
    """Determine the letter described in the image based on
    pixel comparison using an image database of the alphabet."""
    # grab PNG files from alphabet image db
    glob_pattern = os.path.join(LETTERS_DIR, "*.png")
    files = list(filter(os.path.isfile, glob.glob(glob_pattern)))
    
    # compare image to each letter in the alphabet
    min_diff = None
    letter = str()
    for file in files:
        alpha_img = cv2.imread(file)
        diff = compare_img_pixels(letter_img,
                                  alpha_img,
                                  img_resize=IMG_SIZE_VERY_SMALL)
        if min_diff is None or diff < min_diff:
            min_diff = diff
            letter = os.path.basename(file).replace(".png", "")
            if "_" in letter:
                if "." in letter:
                    # period symbol
                    letter = letter.replace("_._", ". ")
                elif "\'" in letter:
                    # apostraphe symbol
                    letter = letter.replace("_", "")
                else:
                    # male/female symbol
                    letter = letter.replace("_", " ")
    return letter


def create_pokemon_sprite_fn(name: str,
                             game: str,
                             _type: SpriteType = None,
                             _dir: str = SPRITES_DIR,
                             ext: str = "png"):
    """Generate the sprite filename from the Pokémon properites."""
    number = get_pokemon_number(name)
    base_fn = f"{number:03d}_{get_sprite_name(name)}.{ext}"
    if _type is None:
        pokemon_fn = os.path.join(_dir, base_fn)
    else:
        pokemon_fn = os.path.join(_dir, game.lower(), _type, base_fn)
    logger.debug(f"pokemon_fn: {pokemon_fn}")
    return pokemon_fn


def get_sprite_name(name: str):
    """Retrieve a Pokémon's sprite name."""
    return name.lower().replace(' ','-').replace('.','').replace('\'','')


def get_screenshots() -> List[str]:
    """Retrieve all screenshots sorted by creation time."""
    # only grab PNG files
    glob_pattern = os.path.join(RETROARCH_SCREENSHOTS_DIR, "*.png")
    files = list(filter(os.path.isfile, glob.glob(glob_pattern)))
    
    # sort by file creation time
    files.sort(key=os.path.getctime)
    return files


def get_latest_screenshot_fn() -> str:
    """Retrieve the most recent screenshot."""
    files = get_screenshots()
    if len(files) == 0:
        logger.warning("No screenshots exist")
        return None
    return files[-1]  # last element in list is most recent


def crop_pokemon_in_battle(battle_img_fn: str, del_png: bool = True) -> cv2.Mat:
    """Crop square image of a Pokémon in battle."""
    im = Image.open(battle_img_fn)

    # percentages used in calcs were determined empirically
    # valid only for generation II games
    pokemon_width = im.width*(0.35)
    pokemon_height = pokemon_width
    left = im.width*(0.6)
    right = left + pokemon_width
    top = 0
    bottom = pokemon_height

    # crop image and save to disk
    im = im.crop((left, top, right, bottom))
    cropped_fn = "crop.png"
    im.save(cropped_fn)

    # load into OpenCV obj
    img = cv2.imread(cropped_fn)
    
    if del_png:
        os.remove(cropped_fn)

    return img


def crop_name_in_battle(battle_img_fn: str, del_png: bool = True) -> List[cv2.Mat]:
    """Crop name of a Pokémon in battle."""
    im = Image.open(battle_img_fn)

    # generation II games have maximum 10 chars for names
    max_chars = 10
    letter_imgs = list()
    for i in range(max_chars):
        # percentages used in calcs were determined empirically
        # valid only for generation II games
        char_width = im.width*(0.04375)
        char_height = char_width
        char_space = char_width/7
        
        left = i*(char_width + char_space) + im.width*(0.05)
        right = left + char_width
        top = 0
        bottom = char_height

        # crop image and save to disk
        im_char = im.crop((left, top, right, bottom))
        cropped_fn = f"char_{str(i)}.png"
        im_char.save(cropped_fn)

        # load into OpenCV obj
        img = cv2.imread(cropped_fn)

        # determine if img contains a letter based on how white it is
        if not is_img_white(img):
            letter_imgs.append(img)

        if del_png:
            os.remove(cropped_fn)
    
    logger.debug(f"pokemon name contains {len(letter_imgs)} letters")

    return letter_imgs
