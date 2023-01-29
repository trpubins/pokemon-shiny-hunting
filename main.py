import logging

import __init__
from config import POKEMON_STATIC_ENCOUNTER
from emulator import Emulator
from encounter import find_shiny
from image import get_latest_screenshot_fn
from notifications import send_notification
from pokemon import Pokemon
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


if __name__ == "__main__":
    logger.info("running main")
    em = Emulator()
    em.launch_game()
    
    pokemon = Pokemon(POKEMON_STATIC_ENCOUNTER)
    shiny_found, n_attempts = find_shiny(em, pokemon, max_attempts=8000, static_enounter=True)
    logger.info(f"total number attempts: {n_attempts}")
    
    if shiny_found:
        attachments = [get_latest_screenshot_fn()]
    else:
        attachments = []
    send_notification(pokemon, n_attempts, shiny_found,
                      attachments=attachments, send=True)
