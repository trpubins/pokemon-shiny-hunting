import logging

import __init__
from config import POKEMON_STATIC_ENCOUNTER
from emulator import Emulator
from notifications import send_notification
from pokemon import Pokemon
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


if __name__ == "__main__":
    logger.info("running main")
    em = Emulator()
    em.launch_game()
    
    pokemon = Pokemon(POKEMON_STATIC_ENCOUNTER)
    logger.info(f"looking for shiny {pokemon.name}")
    n_attempts = 0
    shiny_found = False
    while not shiny_found:
        n_attempts += 1
        em.continue_pokemon_game()
        shiny_found = em.find_shiny(pokemon, static_enounter=True)
        if not shiny_found:
            em.reset()
    logger.info(f"found a shiny {pokemon.name}!")
    logger.info(f"number attempts: {n_attempts}")
    send_notification(pokemon, n_attempts, shiny_found, send=False)
