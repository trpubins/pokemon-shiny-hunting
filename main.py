"""Application driver module."""

import logging
from multiprocessing import Queue
import signal
import sys

from config import NATIVE_SAVES_DIR, ROM_NAME, RETROARCH_CFG
from emulator import Emulator
from encounter import StaticEncounter
from image import determine_capture_status, get_latest_screenshot_fn
from notifications import send_notification
from pack import Balls, collect_inventory
from pokemon import Pokemon
from retroarch import cleanup_save_dir, copy_native_save
from helpers.common import delay
from helpers.file_mgmt import cdtmp
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


def run(emulator: Emulator,
        encounter: StaticEncounter,
        max_attempts: int = 8000,
        send_email: bool = True,
        queue: Queue = None):
    """Try to find a shiny from a static encounter."""
    og_rename_files = copy_native_save(pokemon_name=encounter.pokemon.name,
                                       user_rom_name=ROM_NAME,
                                       native_saves_dir=NATIVE_SAVES_DIR,
                                       retroarch_saves_dir=RETROARCH_CFG.savefile_dir)

    def kill_proc_and_cleanup():
        """Kill the emulator process and clean up
        the saves directory."""
        emulator.kill_process()
        og_rename_rtc_file, og_rename_srm_file = og_rename_files
        cleanup_save_dir(user_rom_name=ROM_NAME,
                         retroarch_saves_dir=RETROARCH_CFG.savefile_dir,
                         renamed_rtc_file=og_rename_rtc_file,
                         renamed_srm_file=og_rename_srm_file)

    def signal_handler(signalnum: int, frame):
        """Kill the emulator and log the received signal."""
        kill_proc_and_cleanup()
        if signalnum == signal.SIGINT:
            logger.warning("Keyboard interrupt (ctrl + c)")
            sys.exit(1)
        elif signalnum == signal.SIGTERM:
            logger.warning("Termination signal")
            sys.exit(2)
    # register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    emulator.launch_game()
    try:
        shiny_found = False
        n_attempts = 0
        with cdtmp(sub_dirname="pokemon_shiny_hunting"):
            logger.info(f"looking for shiny {encounter.pokemon.name}")
            while not shiny_found and n_attempts < max_attempts:
                shiny_found = encounter.find_shiny()
                n_attempts += 1
                logger.debug(f"attempt number {n_attempts}")

                # queue is required when run() is executed in separate process
                if queue is not None:
                    if not queue.empty():
                        queue.get()
                    queue.put({"shiny_found": shiny_found, "n_attempts": n_attempts})

                # log the number of attempts with INFO for every 5% of progress
                if max_attempts >= 20 and n_attempts % int(max_attempts/20) == 0:
                    logger.info(f"attempt number {n_attempts}/{max_attempts}")

            logger.info(f"total number attempts: {n_attempts}")
    except Exception as e:
        kill_proc_and_cleanup()
        logger.error("Exception occurred while shiny hunting")
        raise e
    
    if shiny_found:
        # Set Up Balls Pocket
        emulator.press_b(delay_after_press=1.0)
        emulator.move_down(delay_after_press=.5)
        emulator.press_a(delay_after_press=.5)
        emulator.move_right_precise(delay_after_press=0.5)

        # Collect Balls Pocket qty
        balls = Balls(collect_inventory(emulator, get_qty=True))
        emulator.press_b(delay_after_press=0.5)
        logger.info(f'current inventory: {balls.inventory}')
        balls.throw_best_ball(emulator)
        capture_img = get_latest_screenshot_fn()
        delay(1.5)
        count = 0
        
        # If Pokemon breaks out of ball, continue throwing same ball, if 3 or more balls have been thrown, allows user to take over
        #manually
        while determine_capture_status(capture_img) != True and count <= 3:
            emulator.press_b(presses= 8, delay_after_press=0.25)
            balls.throw_best_ball(emulator, highlighted= False)
            capture_img = get_latest_screenshot_fn()
            count += 1

        attachments = [get_latest_screenshot_fn()]
    else:
        kill_proc_and_cleanup()
        attachments = []
    send_notification(encounter.pokemon,
                      n_attempts,
                      shiny_found,
                      attachments=attachments,
                      send=send_email)
    sys.exit(0)


if __name__ == "__main__":
    import __init__
    from config import POKEMON_STATIC_ENCOUNTER

    logger.info("running main")
    emulator = Emulator()
    pokemon = Pokemon(POKEMON_STATIC_ENCOUNTER)
    encounter = StaticEncounter(emulator, pokemon)
    run(emulator, encounter)