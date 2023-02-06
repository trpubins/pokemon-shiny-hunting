"""Model a Pokémon."""

from enum import Enum
import logging
import os

from config import PROJ_ROOT_PATH, POKEMON_GAME
from dex import get_pokemon_number
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


SPRITES_DIR = os.path.join(PROJ_ROOT_PATH, "assets", "images", "sprites")


class Pokemon():
    """Defines attributes of a Pokémon."""
    def __init__(self, name: str):
        self.name = name.upper()
        self.number = get_pokemon_number(name)
    
    def get_normal_img_fn(self) -> str:
        """Obtain the filename for the Pokémon's
        normal image."""
        return create_pokemon_sprite_fn(game=POKEMON_GAME,
                                        name=self.name,
                                        number=self.number,
                                        _type=SpriteType.NORMAL)

    def get_shiny_img_fn(self) -> str:
        """Obtain the filename for the Pokémon's
        shiny image."""
        return create_pokemon_sprite_fn(game=POKEMON_GAME,
                                        name=self.name,
                                        number=self.number,
                                        _type=SpriteType.SHINY)


class SpriteType(str, Enum):
    """Enumeration for sprite types."""
    NORMAL = "normal"
    SHINY = "shiny"


def create_pokemon_sprite_fn(game: str,
                             name: str,
                             number: int = None,
                             _type: SpriteType = None,
                             _dir: str = SPRITES_DIR,
                             ext: str = "png"):
    """Generate the sprite filename from the Pokémon properites."""
    if number is None:
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
