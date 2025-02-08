import os

import pytest

from helpers.log import get_logger

from conftest import get_json_files, print_section_break

# ----------------------------------------------------------------------------#
#                               --- Globals ---                               #
# ----------------------------------------------------------------------------#
from __setup__ import TEST_EVENTS_PATH, TEST_IMG_DIR

MODULE = "notifications"
MODULE_EVENTS_DIR = os.path.join(TEST_EVENTS_PATH, MODULE)

# ----------------------------------------------------------------------------#
#                               --- Logging ---                               #
# ----------------------------------------------------------------------------#
logger = get_logger(f"test_{MODULE}")

# ----------------------------------------------------------------------------#
#                           --- Module Imports ---                            #
# ----------------------------------------------------------------------------#
from notifications import (  # noqa: E402
    Pokemon,
    send_notification,
)


# ----------------------------------------------------------------------------#
#                                --- TESTS ---                                #
# ----------------------------------------------------------------------------#
@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file", get_json_files(MODULE_EVENTS_DIR, ["send_notification"])
)
def test_01_send_notification(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    _input: dict = get_event_as_dict["input"]
    name: str = _input["name"]
    image: str = _input.get("image")
    n_attempts: int = _input["n_attempts"]
    shiny_found: bool = _input["shiny_found"]
    expected_output: int = get_event_as_dict["expected_output"]
    
    notification = send_notification(
        Pokemon(name),
        n_attempts,
        shiny_found,
        attachments=[os.path.join(TEST_IMG_DIR, image)] if image else [],
        send=False,
    )
    assert (notification == expected_output)
