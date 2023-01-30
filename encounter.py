"""Facilitate a static encounter with a Pokémon."""

import logging
import os
from typing import Tuple

from emulator import Emulator
from image import (
    crop_pokemon_in_battle,
    determine_sprite_type,
    get_latest_screenshot_fn
)
from pokemon import Pokemon, SpriteType
from helpers.delay import delay
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


STATIC_ENCOUNTERS = {
    "ELECTRODE": { "max_moves":  70, "explode":  True, "sequence": "a" },
    "GYARADOS":  { "max_moves":  85, "explode": False, "sequence": "a", "delay": 2 },
    "LAPRAS":    { "max_moves": 100, "explode": False, "sequence": "a" },
    "SNORLAX":   { "max_moves":  60, "explode": False, "sequence": "sdddarrrbbaaa" },
    "SUDOWOODO": { "max_moves":  60, "explode": False, "sequence": "aaaaaa"},
    "SUICUNE":   { "max_moves":  95, "explode": False, "sequence": "u", "delay": 3.5 },
    "LUGIA":     { "max_moves":  65, "explode": False, "sequence": "a"},
    "HO-OH":     { "max_moves":  65, "explode": False, "sequence": "a"},
    "CELEBI":    { "max_moves":  50, "explode": False, "sequence": "a"},
    "ODD EGG":   { "sequence": "aaaaa"}
}


def find_shiny(emulator: Emulator,
               pokemon: Pokemon,
               max_attempts: int = 100,
               static_enounter: bool = True) -> Tuple[bool, int]:
    """Find a shiny Pokémon.
    Assumes Pokémon game has been launched in the emulator."""
    logger.info(f"looking for shiny {pokemon.name}")
    if not static_enounter:
        raise RuntimeError("Not yet able to handle dynamic encounters")
    else:
        n_attempts = 0
        shiny_found = False
        while not shiny_found and n_attempts < max_attempts:
            emulator.reset()
            emulator.continue_pokemon_game()
            sprite = encounter_static(emulator, pokemon)
            n_attempts += 1
            logger.debug(f"attempt number {n_attempts}")
            
            # log the number of attempts with INFO for every 5% of progress
            if max_attempts >= 20 and n_attempts % int(max_attempts/20) == 0:
                logger.info(f"attempt number {n_attempts}/{max_attempts}")

            if sprite == SpriteType.SHINY:
                shiny_found = True
        if shiny_found:
            logger.info(f"found a shiny {pokemon.name}!")
        else:
            logger.info(f"no shiny found for {pokemon.name}!")
    return shiny_found, n_attempts


def encounter_static(emulator: Emulator, pokemon: Pokemon) -> SpriteType:
    """Encounter a static Pokémon with the objective of entering a battle."""
    logger.debug(f"encountering static {pokemon.name}")
    static_encounter = STATIC_ENCOUNTERS[pokemon.name]
    sequence: str = static_encounter["sequence"]
    seconds: int = static_encounter["delay"]
    perform_btn_sequence(emulator, sequence)
    delay(seconds)
    logger.debug(f"wild {pokemon.name} appeared")
    emulator.take_screenshot(delay_after_press=0.25)
    screenshot_fn = get_latest_screenshot_fn()
    crop = crop_pokemon_in_battle(screenshot_fn, del_png=False)
    sprite = determine_sprite_type(pokemon, crop)
    if sprite == SpriteType.NORMAL:
        os.remove(screenshot_fn)
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
        delay(0.25)


if __name__ == "__main__":
    import __init__
    from config import POKEMON_STATIC_ENCOUNTER

    em = Emulator()
    em.launch_game()
    pokemon = Pokemon(POKEMON_STATIC_ENCOUNTER)
    shiny_found, n_attempts = find_shiny(em, pokemon, max_attempts=3)
    logger.info(f"total number attempts: {n_attempts}")