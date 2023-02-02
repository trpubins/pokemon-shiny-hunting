import logging

import __init__
from config import POKEMON_STATIC_ENCOUNTER
from emulator import Emulator
from encounter import find_shiny
from image import get_latest_screenshot_fn
from notifications import send_notification
from pokemon import Pokemon
from helpers.tmp import cdtmp
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


if __name__ == "__main__":
    logger.info("running main")
    em = Emulator()
    em.launch_game()
    
    try:
        with cdtmp(sub_dirname="pokemon_shiny_hunting"):
            pokemon = Pokemon(POKEMON_STATIC_ENCOUNTER)
            shiny_found, n_attempts = find_shiny(em, pokemon, max_attempts=8000, static_enounter=True)
            logger.info(f"total number attempts: {n_attempts}")
    except KeyboardInterrupt as k:
        logger.warning("Keyboard interrupt by user")
        em.quit()
        raise k
    except Exception as e:
        logger.error("Exception occurred while shiny hunting")
        em.quit()
        raise e
    
    if shiny_found:
        em.save_state()
        em.fast_fwd_off()
        em.pause_on()
        attachments = [get_latest_screenshot_fn()]
    else:
        em.quit()
        attachments = []
    send_notification(pokemon, n_attempts, shiny_found,
                      attachments=attachments, send=True)
