"""Application driver module."""

import logging
from multiprocessing import Queue
import signal
import sys

from config import NATIVE_SAVES_DIR, ROM_NAME, RETROARCH_CFG
from emulator import Emulator
from encounter import StaticEncounter
from image import get_latest_png_fn
from notifications import send_notification
from pokemon import Pokemon
from retroarch import cleanup_save_dir, copy_native_save
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
        emulator.save_state()
        emulator.fast_fwd_off()
        emulator.pause_on()
        attachments = [get_latest_png_fn(RETROARCH_CFG.screenshot_dir)]
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
    import __init__  # noqa: F401
    from config import POKEMON_STATIC_ENCOUNTER

    logger.info("running main")
    emulator = Emulator()
    pokemon = Pokemon(POKEMON_STATIC_ENCOUNTER)
    encounter = StaticEncounter(emulator, pokemon)
    run(emulator, encounter)