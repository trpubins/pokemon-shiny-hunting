"""Model an in-game menu."""

from enum import Enum
import logging
import os

from config import MENU_DIR
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


class MenuType(str, Enum):
    """Enumeration for menu types."""
    START = "start"
    CONTINUE = "continue"
    PAUSE = "pause"
    ITEMS = "items"
    BATTLE = "battle"


def get_menu_fn(menu_type: MenuType, ext: str = "png"):
    """Generate the menu filename from the menu type."""
    menu_fn = os.path.join(MENU_DIR, f"menu_{menu_type}.{ext}")
    logger.debug(f"menu_fn: {menu_fn}")
    return menu_fn
