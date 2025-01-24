import math
import os

import pytest

from helpers.log import get_logger

from conftest import get_json_files, print_section_break

# ----------------------------------------------------------------------------#
#                               --- Globals ---                               #
# ----------------------------------------------------------------------------#
from __setup__ import TEST_EVENTS_PATH, TEST_IMG_DIR

MODULE = "opencv_util"
MODULE_EVENTS_DIR = os.path.join(TEST_EVENTS_PATH, MODULE)

# ----------------------------------------------------------------------------#
#                               --- Logging ---                               #
# ----------------------------------------------------------------------------#
logger = get_logger(f"test_{MODULE}")

# ----------------------------------------------------------------------------#
#                           --- Module Imports ---                            #
# ----------------------------------------------------------------------------#
from helpers.opencv_util import (  # noqa: E402
    cv2,
    compare_img_color,
    compare_img_pixels,
)


# ----------------------------------------------------------------------------#
#                                --- TESTS ---                                #
# ----------------------------------------------------------------------------#
@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file", get_json_files(MODULE_EVENTS_DIR, ["compare_img_pixels"])
)
def test_01_compare_img_pixels(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    img1_fn: str = get_event_as_dict["input"]["image1"]
    img2_fn: str = get_event_as_dict["input"]["image2"]
    expected_output: str = get_event_as_dict["expected_output"]
    
    img1 = cv2.imread(os.path.join(TEST_IMG_DIR, img1_fn))
    img2 = cv2.imread(os.path.join(TEST_IMG_DIR, img2_fn))
    img_diff = compare_img_pixels(img1, img2)
    
    if (expected_output == "same"):
        assert(img_diff == 0)
    else:
        assert(img_diff != 0)


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file", get_json_files(MODULE_EVENTS_DIR, ["compare_img_color"])
)
def test_02_compare_img_color(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    img1_fn: str = get_event_as_dict["input"]["image1"]
    img2_fn: str = get_event_as_dict["input"]["image2"]
    expected_output: str = get_event_as_dict["expected_output"]
    
    img1 = cv2.imread(os.path.join(TEST_IMG_DIR, img1_fn))
    img2 = cv2.imread(os.path.join(TEST_IMG_DIR, img2_fn))
    img_diff = compare_img_color(img1, img2, ignore_white=False, offset_shading=False)
    
    if (expected_output == "max"):
        expected_val = 255*math.sqrt(3)
    else:
        expected_val = 0
    assert (math.isclose(img_diff, expected_val, rel_tol=1e-06))