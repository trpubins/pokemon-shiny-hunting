"""Module to calibrate emulator fps (frames per second)."""

import logging

from main import run as go_shiny_hunt
from config import NATIVE_SAVES_DIR, RETROARCH_CFG, ROM_NAME
from emulator import Emulator
from encounter import StaticEncounter
from pokemon import Pokemon
from retroarch import cleanup_save_dir, copy_native_save
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


if __name__ == "__main__":
    logger.info("running calibration")
    
    # calibrate with Snorlax since this static encounter has most buttons in sequence
    pokemon_name = "Snorlax"
    og_rename_rtc_file, og_rename_srm_file = copy_native_save(pokemon_name=pokemon_name,
                                                              user_rom_name=ROM_NAME,
                                                              native_saves_dir=NATIVE_SAVES_DIR,
                                                              retroarch_saves_dir=RETROARCH_CFG.savefile_dir)
    
    emulator = Emulator()
    pokemon = Pokemon(pokemon_name)
    encounter = StaticEncounter(emulator, pokemon)
    try:
        go_shiny_hunt(emulator, encounter, max_attempts=10, send_email=False)
    finally:
        cleanup_save_dir(user_rom_name=ROM_NAME,
                         retroarch_saves_dir=RETROARCH_CFG.savefile_dir,
                         renamed_rtc_file=og_rename_rtc_file,
                         renamed_srm_file=og_rename_srm_file)
