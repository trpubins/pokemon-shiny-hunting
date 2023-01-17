"""Perform image transformation and image detection."""

import glob
import logging
import os
from typing import List

import cv2
from PIL import Image

from config import RETROARCH_SCREENSHOTS_DIR
from pokemon import Pokemon, SpriteType
from helpers.opencv_util import (
    IMG_SIZE_VERY_SMALL,
    compare_img_color, compare_img_pixels,
    get_img_height, get_img_width, is_img_white
)
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


LETTERS_DIR = os.path.join("images", "letters")
MENU_DIR = os.path.join("images", "menus")
STATUS_DIR = os.path.join("images", "status")


def determine_sprite_type(pokemon: Pokemon, img: cv2.Mat) -> SpriteType:
    """Determine the sprite type based on image color comparison."""
    normal_img = cv2.imread(pokemon.get_normal_img_fn())
    shiny_img = cv2.imread(pokemon.get_shiny_img_fn())
    img = cv2.resize(img, (get_img_width(normal_img), get_img_height(normal_img)))

    # use color differences to determine sprite type
    diff_normal = compare_img_color(img, normal_img)
    diff_shiny = compare_img_color(img, shiny_img)
    if diff_normal < diff_shiny:
        sprite_type = SpriteType.NORMAL
    else:
        sprite_type = SpriteType.SHINY
    logger.debug(f"{pokemon} is more similar to {sprite_type}")
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

def determine_capture_status(pokemon: Pokemon, battle_img: cv2.Mat = None) -> bool:
    '''Checks if sprite is equal to pokemon or pokeball'''
    #set up for testing within test_image folder
    if battle_img is None:
        img = get_latest_screenshot_fn()
        img = crop_pokemon_in_battle(img)
    else:
        img = battle_img

    normal_img = cv2.imread(pokemon.get_normal_img_fn())
    shiny_img = cv2.imread(pokemon.get_shiny_img_fn())
    img = cv2.resize(img, (get_img_width(normal_img), get_img_height(normal_img)))

    # use color differences to determine sprite type
    diff_normal = compare_img_color(img, normal_img)
    diff_shiny = compare_img_color(img, shiny_img)
    
    # if both sprites do not closely resemble screenshot sprite, then catch was successful
    if diff_normal > 15 and diff_shiny > 15:
        captured = True
    else:
        captured = False
    return captured

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

def crop_menu(img_fn: str, del_png: bool = True) -> str:
    im = Image.open(img_fn)

    menus = [
        {"menu": "start", "top": 0, "bottom": 0.45, "left": 0, "right": 0.85},
        {"menu": "continue", "top": 0.45, "bottom": 1, "left": 0.2, "right": 1},
        {"menu": "pause", "top": 0, "bottom": 1, "left": 0.5, "right": 1},
        {"menu": "items", "top": 0.05, "bottom": 0.6, "left": 0, "right": 0.25},
        {"menu": "battle", "top": 0.7, "bottom": 1, "left": 0.4, "right": 1},
    ]

    diff = 1000
    for menu in menus:
        # open the known menu item for comparison
        path =os.path.join(MENU_DIR, 'menu_' + menu['menu'] + '.png')
        normal_menu = cv2.imread(path)

        # defines the borders for each menu type
        top = im.height * menu['top']
        bot = im.height * menu['bottom']
        left = im.width * menu['left']
        right = im.width * menu['right']

        im1 = im.crop((left, top, right, bot))
        im1.save('menu.png')

        # im1 converted to OpenCV object
        im1 = cv2.imread('menu.png')
        im1 = cv2.resize(im1, (get_img_width(normal_menu), get_img_height(normal_menu)))

        diff_menu = compare_img_color(im1, normal_menu)
        if diff_menu < diff:
            diff = diff_menu
            menu_check = menu['menu']
        

        if del_png:
            os.remove('menu.png')

    return menu_check



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
