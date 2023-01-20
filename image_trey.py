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
NUM_DIR = os.path.join("images", "numbers")
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
                elif "e" in letter:
                    # e in pokemon and pokeball
                    letter = letter.replace("_", "")
                else:
                    # male/female symbol
                    letter = letter.replace("_", " ")
    return letter

def determine_quantity(num_imgs: List[cv2.Mat]) -> int:
    """Determine the quantity of items in the bag."""
    num = str()
    for num_img in num_imgs:
        val = determine_number(num_img)
        num += val
    logger.debug(f"determined name: {num}")
    return int(num)

def determine_number(num_img: cv2.Mat) -> str:
    """Determine the number described in the image based on
    pixel comparison using an image database between 0-9."""
    # grab PNG files from numbers image db
    glob_pattern = os.path.join(NUM_DIR, "*.png")
    files = list(filter(os.path.isfile, glob.glob(glob_pattern)))
    
    # compare image to each number
    min_diff = None
    number = str()
    for file in files:
        alpha_img = cv2.imread(file)
        diff = compare_img_pixels(num_img,
                                  alpha_img,
                                  img_resize=IMG_SIZE_VERY_SMALL)
        if min_diff is None or diff < min_diff:
            min_diff = diff
            number = os.path.basename(file).replace(".png", "")
    return number

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

def crop_bag_items(img_fn: str, del_png: bool = True) -> list:
    im = Image.open(img_fn)
    max_items = 5
    items = []
    # crop to only the item portion of the screen
    left = im.width * .4
    right = im.width
    bot = im.height * .675
    top = im.height * .1
    im = im.crop((left, top, right, bot))
    
    item_height = .195
    # create a box for each item separated by its name and quantity
    for item in range(max_items):
        item_top = im.height * item_height * item
        item_bot = im.height * .2 * (item + 1)
        box = im.crop((0, item_top, im.width, item_bot))
        item_name = box.crop((0, box.height * .05, box.width, box.height * .5))
        # item_name.show()
        item_name.save('item.png')
        letter_imgs = crop_item_name('item.png')
        item_name = determine_name(letter_imgs)
        if item_name != '' and item_name != 'cancel':
            items.append(item_name)
        
        item_quant = box.crop((box.width * .825, box.height * .5, box.width, box.height))
        item_quant.save('quant.png')
        # item_quant.show()
        # num_imgs = crop_item_quantity('quant.png')
    
    if del_png:
        os.remove('item.png')
        os.remove('quant.png')
    
    return items

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

def crop_item_name(battle_img_fn: str, del_png: bool = True) -> List[cv2.Mat]:
    """Crop name of an item in bag."""
    im = Image.open(battle_img_fn)

    # generation II games have maximum 10 chars for items
    max_chars = 12
    letter_imgs = list()
    for i in range(max_chars):
        # percentages used in calcs were determined empirically
        # valid only for generation II games
        char_width = im.width*(0.0725)
        char_height = im.height
        char_space = char_width/7
        
        left = i*(char_width + char_space)
        right = left + char_width
        top = 0
        bottom = char_height

        # crop image and save to disk
        im_char = im.crop((left, top, right, bottom))
        cropped_fn = f"char_{str(i)}.png"
        im_char.save(cropped_fn)
        im_char = sharpen_pic(cropped_fn)

        # im_char.show()

        # load into OpenCV obj
        img = cv2.imread(cropped_fn)

        # determine if img contains a letter based on how white it is
        if not is_img_white(img):
            letter_imgs.append(img)

        # if del_png:
        #     os.remove(cropped_fn)
    
    logger.debug(f"pokemon name contains {len(letter_imgs)} letters")

    return letter_imgs

def crop_item_quantity(bag_img_fn: str, del_png: bool = True) -> List[cv2.Mat]:
    '''Retrieve number picture of item_quanity'''
    im = Image.open(bag_img_fn)

    max_num = 2
    num_imgs = list()
    for i in range(max_num):
        # percentages used in calcs were determined empirically
        # valid only for generation II games
        char_width = im.width*(0.5)
        char_height = im.height
        char_space = char_width/8
        
        left = i*(char_width + char_space)
        right = left + char_width
        top = 0
        bottom = char_height

        # crop image and save to disk
        im_char = im.crop((left, top, right, bottom))
        im_char = sharpen_pic(im_char)
        cropped_fn = f"char_{str(i)}.png"
        im_char.save(cropped_fn)
        
        # im_char.show()

        # load into OpenCV obj
        img = cv2.imread(cropped_fn)

        # determine if img contains a letter based on how white it is
        if not is_img_white(img):
            num_imgs.append(img)

        if del_png:
            os.remove(cropped_fn)
    
    logger.debug(f"pokemon name contains {len(num_imgs)} letters")

    return num_imgs

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

def sharpen_pic(im: str) -> Image.Image:
    '''fine tunes cropping and eliminates image blur'''
    image = Image.open(im)
    # white threshold. Empirical value. Change for problem-solving
    white = (180, 180, 180)
    width = image.width
    height = image.height
    top = 0
    left = 0
    right = width
    bottom = height

    # overlook spaces
    if is_img_white(cv2.imread(im)):
        return image
    
    for y in range(height):
        counter_x = 0
        for x in range(width):
            coordinate = x, y
            # change all values below the white tuple threshold to black, all others will be made to white
            try:
                if image.getpixel(coordinate) < white:
                    image.putpixel(coordinate, (0, 0, 0))
                else:
                    image.putpixel(coordinate, (255, 255, 255))
                    counter_x += 1
            except:
                break
        # if the count of white pixels equals the width of the image, then the line below will become our top cropping point.
        # if the entire image has passed with extra white lines, then the first occurrence of all white will be the bottom crop.
        if counter_x >= width - 1:
                    if y < height * 0.5:
                        top = y + 1
                    else:
                        bottom = y
                        break
    for x in range(width):
        counter_y = 0
        for y in range(height):
            coordinate = x, y
            try:
                # check to see which pixels have already gone through the first transform
                if image.getpixel(coordinate) >= white:
                    counter_y += 1
                # if the count of white pixels equals the height of the image, then the line to the right will be our left cropping point.
                # if the entire has passed from left to right and there are full white pixelrows, this will be our right cropping point.
                if counter_y >= height - 1:
                    if x < width * 0.5:
                        left = x + 1
                    else:
                        right = x
                        break
                else:
                    continue
            except:
                break
    # return fully cropped image (no all-white on the borders)
    image = image.crop((left, top, right, bottom))
    return image