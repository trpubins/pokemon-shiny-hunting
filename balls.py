import logging

from emulator import Emulator, ToggleState
from encounter import StaticEncounter
from image import determine_capture_status, get_latest_screenshot_fn
from pack import Pack, Balls, collect_inventory
from pokemon import Pokemon

from helpers.common import delay
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


if __name__ == "__main__":
    import __init__
    from config import POKEMON_STATIC_ENCOUNTER
    em = Emulator()
    em.launch_game()
    em.continue_pokemon_game()
    pack = Pack(em)
    balls = pack.balls
    logger.info(f"current ball inventory: {balls.inventory}")
    em.take_screenshot()
    while em.state.battle_state() == ToggleState.OFF:
        pokemon = Pokemon(POKEMON_STATIC_ENCOUNTER)
        encounter = StaticEncounter(em, pokemon)
        encounter._encounter_static()
        em.press_b(presses=5, delay_after_press=0.25)
        em.take_screenshot()
    balls.throw_best_ball(em)
    delay(5)
    em.take_screenshot()
    img = get_latest_screenshot_fn()
    capture = determine_capture_status(img)
    
