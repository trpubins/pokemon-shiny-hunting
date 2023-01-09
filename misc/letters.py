"""Builds a db of letters."""

import os
from PIL import Image
DIRECTORY = os.path.join('C:\\', 'Users', 'Trey', 'Pictures', 'Letters')


def get_name(battle_img_fn: str, i:int):
    """Crop name of a Pokémon in battle."""
    name = ""
    pix = []
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z', '_']
    im1 = Image.open(battle_img_fn)

    cropped_fn = "char_" + str(alphabet[i]) + ".png"
    im1.save(cropped_fn)
    for x in range(0, im1.width):
        for y in range(0, im1.height):
            coordinate = x, y
            pix = im1.getpixel(coordinate)
            avg = round((pix[0]+pix[1]+pix[2])/3)
            # print(avg)
            if avg >= 127:
                pix = (255, 255, 255)
            else:
                pix = (0, 0, 0)
            print(pix)
            im1.putpixel(coordinate, pix)
    im1.save(cropped_fn)


if __name__ == "__main__":
    dir = os.listdir(DIRECTORY)
    for i in range(len(dir)):
        pic = os.path.join(DIRECTORY, dir[i])
        get_name(pic, i)