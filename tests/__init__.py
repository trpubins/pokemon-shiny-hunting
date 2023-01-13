# add workspace dir to system path, otherwise cannot import project modules
import os
import sys
proj_root_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.pardir
)
sys.path.append(proj_root_path)

from zipfile import ZipFile

TEST_FILES_DIR = os.path.join("tests", "test_files")
TEST_IMG_DIR = os.path.join(TEST_FILES_DIR, "test_images")


# check if zipfile requires unzipping
with ZipFile(os.path.join(TEST_FILES_DIR, "test_images.zip"), 'r') as zip:
    if not os.path.exists(TEST_IMG_DIR):
        zip.extractall(path=TEST_FILES_DIR)
