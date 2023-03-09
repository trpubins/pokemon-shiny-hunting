"""Perform image transformation and image detection."""

import glob
import logging
import os
from typing import Any, List

import cv2
from PIL import Image

from config import LETTERS_DIR, NUM_DIR, RETROARCH_CFG
from menu import MenuType, get_menu_fn
from pokemon import Pokemon, SpriteType
from helpers.opencv_util import (
    IMG_SIZE_VERY_SMALL,
    compare_img_color, compare_img_pixels,
    get_img_height, get_img_width, is_img_white
)
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


def determine_sprite_type(pokemon: Pokemon, img: cv2.Mat) -> SpriteType:
    """Determine the sprite type based on image color comparison."""
    normal_img = cv2.imread(pokemon.get_normal_img_fn())
    shiny_img = cv2.imread(pokemon.get_shiny_img_fn())
    img = cv2.resize(img, (get_img_width(normal_img), get_img_height(normal_img)))

    # use color differences to determine sprite type
    diff_normal = compare_img_color(img, normal_img, offset_shading=False)
    diff_shiny = compare_img_color(img, shiny_img, offset_shading=False)
    if diff_normal < diff_shiny:
        sprite_type = SpriteType.NORMAL
    else:
        sprite_type = SpriteType.SHINY
    logger.debug(f"{pokemon.name} is more similar to {sprite_type}")
    return sprite_type


def determine_pack_items(pack_img_fn: str, get_qty: bool = True, del_png: bool = True) -> Any:
    """Determine the items and their associated quantities in the pack."""
    # TODO - update after creating pack module with PackType and
    # other custom classes
    im = Image.open(pack_img_fn)

    max_items = 5  # the max number of items shown in one pack screenshot

    # crop to only the item portion of the screen
    # percentages used in calcs were determined empirically
    # valid only for generation II games
    item_height = im.height * 1/9
    left = im.width * 0.4
    right = im.width
    top = item_height
    bot = top + max_items*item_height
    im = im.crop((left, top, right, bot))
    cropped_items_fn = "cropped_items.png"
    im.save(cropped_items_fn)

    items = []
    for i in range(max_items):
        # create a box for each item separated by its name and quantity
        item_top = item_height * i
        item_bot = item_top + item_height
        im_item = im.crop((0, item_top, im.width, item_bot))
        item_fn = "item.png"
        im_item.save(item_fn)

        item_name = determine_pack_item_name(im_item, del_png=del_png)
        if item_name == "" or item_name == "cancel":
            break
        if get_qty:
            item_qty = determine_pack_item_qty(im_item, del_png=del_png)
        else:
            item_qty = None
        item = (item_name, item_qty)
        logger.debug(f"item: {item}")
        items.append(item)
        
    if del_png:
        os.remove(cropped_items_fn)
        os.remove(item_fn)
    
    return items


def determine_pack_item_name(im: Image.Image, del_png: bool = True) -> str:
    """Determine the item name from a boxed image representing an item."""
    char_width = im.width*(0.0725)
    item_name_height = char_width
    top = 0
    bot = top + item_name_height
    im_item_name = im.crop((0, top, im.width, bot))
    item_name_fn = "item_name.png"
    im_item_name.save(item_name_fn)

    letter_imgs = crop_item_name(im_item_name, del_png=del_png)
    item_name = determine_name(letter_imgs)
        
    if del_png:
        os.remove(item_name_fn)
    
    return item_name


def determine_pack_item_qty(im: Image.Image, del_png: bool = True) -> int:
    """Determine the item quantity from a boxed image representing an item."""
    char_width = im.width*(0.0625)
    item_qty_height = char_width
    top = im.height * 0.5575
    bot = top + item_qty_height
    left = im.width * 0.8325
    right = im.width * 0.9975
    im_item_qty = im.crop((left, top, right, bot))
    item_qty_fn = "item_qty.png"
    im_item_qty.save(item_qty_fn)

    num_imgs = crop_item_qty(im_item_qty, del_png=del_png)
    item_qty = determine_quantity(num_imgs)

    if del_png:
        os.remove(item_qty_fn)

    return item_qty


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
                                  resize_width=IMG_SIZE_VERY_SMALL,
                                  resize_height=IMG_SIZE_VERY_SMALL)
        if min_diff is None or diff < min_diff:
            min_diff = diff
            letter = os.path.basename(file).replace(".png", "")
            if "_" in letter:
                if "." in letter:
                    # period symbol
                    letter = letter.replace("_._", ". ")
                elif "-" in letter:
                    # dash symbol
                    letter = letter.replace("_", "")
                elif "\'" in letter:
                    # apostraphe symbol
                    letter = letter.replace("_", "")
                elif "e" in letter:
                    # é in Pokémon and Pokéball
                    letter = letter.replace("_", "")
                else:
                    # male/female symbol
                    letter = letter.replace("_", " ")
    return letter


def determine_quantity(num_imgs: List[cv2.Mat]) -> int:
    """Determine the quantity based on images of each number."""
    if len(num_imgs) == 0:
        logger.warning("Should supply non-empty list of number images.")
        return None
    
    qty = int()
    for i,num_img in enumerate(num_imgs):
        num = determine_number(num_img)
        tens = pow(base=10, exp=len(num_imgs) - 1 - i)
        qty += num * tens
    logger.debug(f"determined qty: {qty}")
    return qty


def determine_number(num_img: cv2.Mat) -> int:
    """Determine the number described in the image based on
    pixel comparison using an image database between 0-9."""
    # grab PNG files from numbers image db
    glob_pattern = os.path.join(NUM_DIR, "*.png")
    files = list(filter(os.path.isfile, glob.glob(glob_pattern)))
    
    # compare image to each number
    min_diff = None
    number = str()
    for file in files:
        digit_img = cv2.imread(file)
        img_width = get_img_width(digit_img)
        img_height = get_img_height(digit_img)
        diff = compare_img_pixels(num_img,
                                  digit_img,
                                  resize_width=int(img_width/4),
                                  resize_height=int(img_height/4))
        if min_diff is None or diff < min_diff:
            min_diff = diff
            number = os.path.basename(file).replace(".png", "")
    return int(number)


def determine_menu(img_fn: str, del_png: bool = True) -> MenuType:
    """Determine the menu type from the provided image.
    Assumes a menu is open in the image."""
    # crop locations in dict were determined empirically
    # valid only for generation II games
    menus = [
        {"type":    MenuType.START, "top": 0,    "bottom": 0.45, "left": 0,   "right": 0.85},
        {"type": MenuType.CONTINUE, "top": 0.45, "bottom": 1,    "left": 0.2, "right": 1},
        {"type":    MenuType.PAUSE, "top": 0,    "bottom": 1,    "left": 0.5, "right": 1},
        {"type":    MenuType.ITEMS, "top": 0.05, "bottom": 0.6,  "left": 0,   "right": 0.25},
        {"type":   MenuType.BATTLE, "top": 0.7,  "bottom": 1,    "left": 0.4, "right": 1},
    ]

    im = Image.open(img_fn)
    min_diff = None
    for menu in menus:
        # open the known menu item for comparison
        menu_fp = get_menu_fn(menu["type"])
        known_menu = cv2.imread(menu_fp)

        # defines the borders for each menu type
        top = im.height * menu["top"]
        bot = im.height * menu["bottom"]
        left = im.width * menu["left"]
        right = im.width * menu["right"]

        # crop image and save to disk
        im_cropped = im.crop((left, top, right, bot))
        cropped_fn = "menu.png"
        im_cropped.save(cropped_fn)

        # convert to OpenCV object
        im_cropped = cv2.imread(cropped_fn)
        
        resize_width = int(.05*get_img_width(known_menu))
        resize_height = int(.05*get_img_height(known_menu))
        diff = compare_img_pixels(im_cropped, known_menu, resize_width, resize_height)
        if min_diff is None or diff < min_diff:
            min_diff = diff
            menu_type: MenuType = menu["type"]

        if del_png:
            os.remove(cropped_fn)

    return menu_type


def get_screenshots() -> List[str]:
    """Retrieve all screenshots sorted by creation time."""
    # only grab PNG files
    glob_pattern = os.path.join(RETROARCH_CFG.screenshot_dir, "*.png")
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


def crop_item_name(im_item_name: Image.Image, del_png: bool = True) -> List[cv2.Mat]:
    """Crop name of an item."""
    # generation II games have maximum 12 chars for items
    max_chars = 12
    letter_imgs = list()
    for i in range(max_chars):
        # percentages used in calcs were determined empirically
        # valid only for generation II games
        char_width = im_item_name.width*(0.0725)
        char_height = im_item_name.height
        char_space = char_width*(0.15)
        
        left = i*(char_width + char_space)
        right = left + char_width
        top = 0
        bottom = char_height

        # crop image and save to disk
        im_char = im_item_name.crop((left, top, right, bottom))
        cropped_fn = f"item_char_{str(i)}.png"
        im_char.save(cropped_fn)

        # load into OpenCV obj
        img = cv2.imread(cropped_fn)

        # determine if img contains a letter based on how white it is
        if not is_img_white(img):
            letter_imgs.append(img)

        if del_png:
            os.remove(cropped_fn)
    
    logger.debug(f"item name contains {len(letter_imgs)} letters")

    return letter_imgs


def crop_item_qty(im_item_qty: Image.Image, del_png: bool = True) -> List[cv2.Mat]:
    """Crop quantity of an item."""
    # generation II games have maximum 2 chars for item quantity
    max_chars = 2
    num_imgs = list()
    for i in range(max_chars):
        # percentages used in calcs were determined empirically
        # valid only for generation II games
        char_width = im_item_qty.width*(0.475)
        char_height = im_item_qty.height
        char_space = im_item_qty.width*(0.05)
        
        left = i*(char_width + char_space)
        right = left + char_width - char_space
        top = 0
        bottom = char_height

        # crop image and save to disk
        im_char = im_item_qty.crop((left, top, right, bottom))
        cropped_fn = f"item_qty_{str(i)}.png"
        im_char.save(cropped_fn)

        # load into OpenCV obj
        img = cv2.imread(cropped_fn)

        # determine if img contains a letter based on how white it is
        if not is_img_white(img):
            num_imgs.append(img)

        if del_png:
            os.remove(cropped_fn)
    
    logger.debug(f"item quantity contains {len(num_imgs)} letters")

    return num_imgs

def determine_capture_status(img: str, del_png: bool = True) -> bool:
    """Determine if capture has been made successfully"""
    pokename = crop_name_in_battle(img)
    pokename = determine_name(pokename)

    im = Image.open(img)

    # generation II games have maximum 10 chars for names
    max_chars = 10
    letter_imgs = list()
    for i in range(max_chars):
        # percentages used in calcs were determined empirically
        # valid only for generation II games
        char_width = im.width*(0.04375)
        char_height = char_width
        char_space = char_width/7
        
        left = i*(char_width + char_space) + im.width*(0.45)    #Derived from empirical testing; compares the upper and lower names on screen
        right = left + char_width
        top = im.height * .775
        bottom = top + char_height

        # crop image and save to disk
        im_char = im.crop((left, top, right, bottom))
        cropped_fn = f"char_{str(i)}.png"
        im_char.save(cropped_fn)

        # load into OpenCV obj
        img1 = cv2.imread(cropped_fn)

        # determine if img contains a letter based on how white it is
        if not is_img_white(img1):
            letter_imgs.append(img1)

        if del_png:
            os.remove(cropped_fn)
    
    capture_name = determine_name(letter_imgs)

    if pokename == capture_name:
        logger.info(f"{pokename.upper()} has been successfully caught!")
        boolean = True
    else:
        logger.info(f"{pokename.upper()} has broken out of the ball!")
        boolean = False
    
    if del_png:
        os.remove(img)
    return boolean

def is_in_battle(del_png: bool = True) -> bool:
    """Check to see if Trainer is in battle"""
    img = get_latest_screenshot_fn()
    im = Image.open(img)
    true_im = os.path.join("assets", "images", "battle", "hp.png")
    """Crop around the HP bar's black box that is located below the name of both Pokemon"""
    hp_upper_top = im.height * 0.125
    hp_upper_bot = im.height * 0.15
    hp_upper_left = im.width * 0.1
    hp_upper_right = im.width * 0.2
    hp_upper = im.crop((hp_upper_left, hp_upper_top, hp_upper_right, hp_upper_bot))
    
    hp1 = "hp_upper_test.png"
    hp_upper.save(hp1)

    hp_lower_top = im.height * 0.515
    hp_lower_bot = im.height * 0.54
    hp_lower_left = im.width * 0.5
    hp_lower_right = im.width * 0.6
    hp_lower = im.crop((hp_lower_left, hp_lower_top, hp_lower_right, hp_lower_bot))

    hp2 = "hp_lower_test.png"
    hp_lower.save(hp2)

    upper = cv2.imread(hp1)
    lower = cv2.imread(hp2)
    true = cv2.imread(true_im)

    if del_png:
        os.remove(hp1)
        os.remove(hp2)

    """Assert that if both crops are identical and not purely white images, return that Trainer is in battle"""
    if compare_img_pixels(upper, lower) == 0 and compare_img_pixels(upper, true) == 0:
        return True
    else:
        return False

if __name__ == "__main__":
    img = get_latest_screenshot_fn()
    im = determine_capture_status(img, False)