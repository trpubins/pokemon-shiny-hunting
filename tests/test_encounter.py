
import __init__

import image as im
from encounter import Encounter
from pokemon import Pokemon, SpriteType

from helpers.delay import delay
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

def throw_masterball(pokemon: str):
    en = Encounter()
    en.em.run_game()
    test = SpriteType.NORMAL
    captured = False
    counter = 0
    while test != SpriteType.SHINY and counter <= 3:
        en.start_game()
        en.encounter_static(pokemon)
        en.em.take_screenshot()
        shot = im.get_latest_screenshot_fn()
        name = im.crop_name_in_battle(shot)
        name = im.determine_name(name)
        assert(pokemon.lower() == name.lower())
        sprite = im.crop_pokemon_in_battle(shot)
        monster = Pokemon(name)
        test = im.determine_sprite_type(monster, sprite)
        logger.info(f"Sprite Type: {test}")
        counter += 1
        logger.info(f"Attempts: {counter}")
        if test == SpriteType.SHINY:
            logger.info("Shiny Found!")
            break
        elif counter > 1:
            break
        else:
            en.em.reset()
    while not captured:
        en.catch_pokemon()
        delay(3)
        en.em.take_screenshot()
        shot = im.get_latest_screenshot_fn()
        sprite = im.crop_pokemon_in_battle(shot)
        captured = im.determine_capture_status(monster, sprite)
    logger.info("Capture Successful")

if __name__ == "__main__":
    throw_masterball("Suicune")
    
    
    

