"""Facilitates interaction with OpenCV objects."""

import cv2
import numpy as np
from typing import Union

from helpers.common import opposite_signs

IMG_SIZE_VERY_SMALL = 8
IMG_SIZE_SMALL = 24
IMG_SIZE_MED = 72
IMG_SIZE_LARGE = 192
IMG_SIZE_VERY_LARGE = 320


class RGB():
    """Describes a pixel in terms of its RGB (red, green, blue) value."""
    LENGTH = 3
    def __init__(self, pixel: np.ndarray = None):
        self.r: Union[int, float] = 0
        self.g: Union[int, float] = 0
        self.b: Union[int, float] = 0
        if pixel is not None:
            # OpenCV decoded images have the channels stored in **B G R** order
            self.b, self.g, self.r = pixel
    
    def is_white(self) -> bool:
        """Determine if an RGB value is white
        (allows for slightly off-white)."""
        return self.r >= 245 and self.g >= 245 and self.b >= 245

    def is_black(self) -> bool:
        """Determine if an RGB value is black
        (only exact black is considered)."""
        return self.r == 0 and self.g == 0 and self.b == 0
    
    def max(self) -> Union[int, float]:
        """Retrieve the maximum component value (red, green or blue)."""
        return max(self.r, self.g, self.b)
    
    def offset(self, number: Union[int, float]):
        """Offset each RGB value by the specified number."""
        self.r += number
        self.g += number
        self.b += number
    
    def rg_diff(self) -> Union[int, float]:
        """The difference between red-green component values."""
        return self.r - self.g
    
    def gb_diff(self) -> Union[int, float]:
        """The difference between green-blue component values."""
        return self.g - self.b
    
    def br_diff(self) -> Union[int, float]:
        """The difference between blue-red component values."""
        return self.b - self.r


def compare_img_color(img1: cv2.Mat,
                      img2: cv2.Mat,
                      ignore_white: bool = True,
                      offset_shading: bool = True) -> float:
    """Compares the color of two images.
    Result is a number between [min=0,max=255*sqrt(3)] where min -> same color and
    max -> opposite color (white vs black)."""
    rgb1 = _get_img_color(img1, ignore_white)
    rgb2 = _get_img_color(img2, ignore_white)
    
    if offset_shading:
        # offset the values of rgb2 by difference in max from rgb1
        amt_offset = rgb1.max() - rgb2.max()
        rgb2.offset(amt_offset)
    
    color_diff = _get_color_diff(rgb1, rgb2)

    if opposite_signs(rgb1.rg_diff(), rgb2.rg_diff()) or \
            opposite_signs(rgb1.gb_diff(), rgb2.gb_diff()) or \
            opposite_signs(rgb1.br_diff(), rgb2.br_diff()):
        # compare interactions between the RGB component values
        # if relative interactions have opposing signs, make
        # significant change to the resulting color difference
        color_diff *= 10
    
    return color_diff


def compare_img_pixels(img1: cv2.Mat,
                       img2: cv2.Mat,
                       resize_width: int = IMG_SIZE_MED,
                       resize_height: int = IMG_SIZE_MED) -> float:
    """Compares two images for pixel equality.
    Result is a number between [min=0,max=unknown] where min -> same image and
    increasing value indicates more differences between the images."""
    # resize the images
    img1 = cv2.resize(img1, (resize_width, resize_height))
    img2 = cv2.resize(img2, (resize_width, resize_height))

    diff = 0
    for row1, row2 in zip(img1, img2):
        for pixel1, pixel2 in zip(row1, row2):
            # unpack into rgb values for each image
            rgb1 = RGB(pixel1)
            rgb2 = RGB(pixel2)
            diff += _get_color_diff(rgb1, rgb2)
    return diff


def is_img_white(img: cv2.Mat) -> bool:
    """Determine if an image is all white."""
    img_color = _get_img_color(img, ignore_white=False)
    return img_color.is_white()


def _get_n_pixels(img: cv2.Mat) -> int:
    """Obtain the total number of pixels in an image."""
    return int(img.size/RGB.LENGTH)


def get_img_height(img: cv2.Mat) -> int:
    """Obtain the height of an image, in pixels."""
    return img.shape[0]


def get_img_width(img: cv2.Mat) -> int:
    """Obtain the width of an image, in pixels."""
    return img.shape[1]


def _get_color_diff(rgb1: RGB, rgb2: RGB) -> float:
    """Use euclidean distance formula to calculate difference
    between two RGB values."""
    r_dist = int(rgb2.r) - int(rgb1.r)
    g_dist = int(rgb2.g) - int(rgb1.g)
    b_dist = int(rgb2.b) - int(rgb1.b)
    return np.sqrt(pow(r_dist, 2) + pow(g_dist, 2) + pow(b_dist, 2))


def _get_img_color(img: cv2.Mat, ignore_white: bool = True) -> RGB:
    """Obtain the color of an image as a single RGB value.
    Result is the color averaged over all pixels.
    
    Optionally, ignore white pixels.
    """
    tot_color = RGB()
    n_pixels = _get_n_pixels(img)
    for row in img:
        for pixel in row:
            rgb = RGB(pixel)
            if ignore_white and rgb.is_white():
                n_pixels -= 1
                continue
            tot_color.r += rgb.r
            tot_color.g += rgb.g
            tot_color.b += rgb.b
    rgb_norm = RGB()
    rgb_norm.r = tot_color.r/n_pixels
    rgb_norm.g = tot_color.g/n_pixels
    rgb_norm.b = tot_color.b/n_pixels
    return rgb_norm
