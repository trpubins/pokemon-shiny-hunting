import logging

import __init__
from config import POKEMON_STATIC_ENCOUNTER
from emulator import Emulator
from encounter import StaticEncounter
from image import get_latest_screenshot_fn
from notifications import send_notification
from pokemon import Pokemon
from helpers.file_mgmt import cdtmp
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


if __name__ == "__main__":
    logger.info("running main")
    em = Emulator()
    em.launch_game()
    try:
        with cdtmp(sub_dirname="pokemon_shiny_hunting"):
            pokemon = Pokemon(POKEMON_STATIC_ENCOUNTER)
            encounter = StaticEncounter(em, pokemon)
            shiny_found = encounter.find_shiny(max_attempts=8000)
            logger.info(f"total number attempts: {encounter.n_attempts}")
    except KeyboardInterrupt as k:
        logger.warning("Keyboard interrupt by user")
        em.kill_process()
        raise k
    except Exception as e:
        logger.error("Exception occurred while shiny hunting")
        em.kill_process()
        raise e
    
    if shiny_found:
        em.save_state()
        em.fast_fwd_off()
        em.pause_on()
        attachments = [get_latest_screenshot_fn()]
    else:
        em.kill_process()
        attachments = []
    send_notification(pokemon, encounter.n_attempts, shiny_found,
                      attachments=attachments, send=True)
