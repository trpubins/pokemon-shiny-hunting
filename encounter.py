"""Facilitate a static encounter with a Pokémon."""

import logging
import os

from config import RETROARCH_CFG
from emulator import Emulator
from image import (
    crop_pokemon_in_battle,
    determine_sprite_type,
    get_latest_png_fn,
)
from pokemon import Pokemon, SpriteType
from helpers.common import delay
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


STATIC_ENCOUNTERS = {
    "ELECTRODE": { "max_moves":  70, "explode":  True, "sequence":              "a", "delay": 1.5  },
    "GYARADOS":  { "max_moves":  85, "explode": False, "sequence":              "a", "delay": 2    },
    "LAPRAS":    { "max_moves": 100, "explode": False, "sequence":              "a", "delay": 2    },
    "SNORLAX":   { "max_moves":  60, "explode": False, "sequence": "sdddarrrbbaaaa", "delay": 1.5  },
    "SUDOWOODO": { "max_moves":  60, "explode": False, "sequence":         "aaaaaa", "delay": 1.5  },
    "SUICUNE":   { "max_moves":  95, "explode": False, "sequence":              "u", "delay": 3.75 },
    "HO-OH":     { "max_moves":  65, "explode": False, "sequence":              "a", "delay": 2    },
    "CELEBI":    { "max_moves":  50, "explode": False, "sequence":              "a", "delay": 2    },
    "LUGIA":     { "max_moves":  65, "explode": False, "sequence":              "a", "delay": 2    },
    "ODD EGG":   { "sequence": "aaaaa"}
}


class StaticEncounter():
    """Maintain state for a static encounter."""
    def __init__(self, emulator: Emulator, pokemon: Pokemon):
        self.emulator = emulator
        self.pokemon = pokemon
    
    def find_shiny(self) -> bool:
        """Find a shiny Pokémon.
        Assumes Pokémon game has been launched in the emulator."""
        self.emulator.reset()
        self.emulator.continue_pokemon_game()
        sprite = self._encounter_static()

        if sprite == SpriteType.SHINY:
            shiny_found = True
        else:
            shiny_found = False
        return shiny_found

    def _encounter_static(self) -> SpriteType:
        """Encounter a static Pokémon with the objective of entering a battle."""
        pokemon = self.pokemon
        logger.debug(f"encountering static {pokemon.name}")
        static_encounter = STATIC_ENCOUNTERS[pokemon.name]
        sequence: str = static_encounter["sequence"]
        seconds: int = static_encounter["delay"]
        perform_btn_sequence(self.emulator, sequence)
        delay(seconds)
        logger.debug(f"wild {pokemon.name} appeared")
        self.emulator.take_screenshot(delay_after_press=0.25)
        screenshot_fn = get_latest_png_fn(RETROARCH_CFG.screenshot_dir)
        crop = crop_pokemon_in_battle(screenshot_fn, del_png=False)
        sprite = determine_sprite_type(pokemon, crop)
        if sprite == SpriteType.NORMAL:
            os.remove(screenshot_fn)
            logger.debug(f"removed screenshot {screenshot_fn}")
        return sprite


def perform_btn_sequence(emulator: Emulator, sequence: str):
    """Perform a button sequence in the emulator using a
    shorthand representation of the series of buttons."""
    for char in sequence:
        if char == "a":
            emulator.press_a()
        elif char == "b":
            emulator.press_b()
        elif char == "u":
            emulator.move_up()
        elif char == "d":
            emulator.move_down()
        elif char == "r":
            emulator.move_right()
        elif char == "l":
            emulator.move_left()
        elif char == "s":
            emulator.press_start()
        else:
            raise RuntimeError(f"Unknown character in sequence: {char}. No button selected.")
        delay(0.5)


if __name__ == "__main__":
    import __init__
    from config import POKEMON_STATIC_ENCOUNTER

    em = Emulator()
    em.launch_game()
    pokemon = Pokemon(POKEMON_STATIC_ENCOUNTER)
    encounter = StaticEncounter(em, pokemon)
    shiny_found = encounter.find_shiny()
    if shiny_found:
        logger.info(f"found a shiny {encounter.pokemon.name}!")
    else:
        logger.info(f"no shiny found for {encounter.pokemon.name}")
    em.kill_process()
