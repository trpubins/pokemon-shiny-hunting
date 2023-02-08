"""Module to calibrate emulator fps (frames per second)."""

import logging
import os
import shutil
from typing import Tuple
from zipfile import ZipFile

import __init__
from config import PROJ_ROOT_PATH, RETROARCH_CFG, ROM_NAME
from emulator import Emulator
from encounter import StaticEncounter
from pokemon import Pokemon
from helpers.tmp import cdtmp
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


SAVES_DIR = os.path.join(PROJ_ROOT_PATH, "assets", "saves")
NATIVE_SAVES_DIR = os.path.join(SAVES_DIR, "native_saves_static_encounters")


def copy_native_save(pokemon_name: str) -> Tuple[str, str]:
    """Copy native save for this Pokémon static encounter
    into the user's saves dir."""
    zip_fn = os.path.join(SAVES_DIR, "native_saves_static_encounters.zip")
    with ZipFile(zip_fn, 'r') as zip:
        if not os.path.exists(NATIVE_SAVES_DIR):
            zip.extractall(path=SAVES_DIR)
            logger.debug(f"unzipped {zip_fn}")
    
    logger.info(f"copying native save files for {pokemon_name} -> savefiles dir")
    calibrate_rom_name = "Pokemon - Crystal Version (UE) (V1.1) [C][!]"
    calibrate_rtc_file = os.path.join(NATIVE_SAVES_DIR, pokemon_name, f"{calibrate_rom_name}.rtc")
    calibrate_srm_file = os.path.join(NATIVE_SAVES_DIR, pokemon_name, f"{calibrate_rom_name}.srm")
    og_rtc_file = os.path.join(RETROARCH_CFG.savefile_dir, f"{ROM_NAME}.rtc")
    og_srm_file = os.path.join(RETROARCH_CFG.savefile_dir, f"{ROM_NAME}.srm")

    # rename original files as to not overwrite user's current saves
    og_rename_rtc_file = None
    if os.path.exists(og_rtc_file):
        og_rename_rtc_file = os.path.join(RETROARCH_CFG.savefile_dir, "og_file.rtc")
        os.rename(og_rtc_file, og_rename_rtc_file)
        logger.debug(f"renamed {og_rtc_file} -> {og_rename_rtc_file}")
    
    og_rename_srm_file = None
    if os.path.exists(og_srm_file):
        og_rename_srm_file = os.path.join(RETROARCH_CFG.savefile_dir, "og_file.srm")
        os.rename(og_srm_file, og_rename_srm_file)
        logger.debug(f"renamed {og_srm_file} -> {og_rename_srm_file}")
    
    # copy calibration save files over to savefile dir, then rename
    shutil.copy(calibrate_rtc_file, og_rtc_file)
    shutil.copy(calibrate_srm_file, og_srm_file)
    logger.debug(f"copied {calibrate_rtc_file} -> {og_rtc_file}")
    logger.debug(f"copied {calibrate_srm_file} -> {og_srm_file}")

    return og_rename_rtc_file, og_rename_srm_file


def cleanup_save_dir(renamed_rtc_file: str, renamed_srm_file: str):
    """Cleanup the RetroArch saves directory."""
    logger.info("cleaning up the savefiles dir")
    og_rtc_file = os.path.join(RETROARCH_CFG.savefile_dir, f"{ROM_NAME}.rtc")
    og_srm_file = os.path.join(RETROARCH_CFG.savefile_dir, f"{ROM_NAME}.srm")

    # first, delete the files that were renamed to the original saves
    os.remove(og_rtc_file)
    os.remove(og_srm_file)
    logger.debug(f"deleted {og_rtc_file}")
    logger.debug(f"deleted {og_srm_file}")

    # next, rename the original files back
    if renamed_rtc_file is not None:
        os.rename(renamed_rtc_file, og_rtc_file)
        logger.debug(f"renamed {renamed_rtc_file} to {og_rtc_file}")
    
    if renamed_srm_file is not None:
        os.rename(renamed_srm_file, og_srm_file)
        logger.debug(f"renamed {renamed_srm_file} to {og_srm_file}")


if __name__ == "__main__":
    logger.info("running calibration")
    
    # calibrate with Snorlax since this static encounter has most buttons in sequence
    pokemon_name = "Snorlax"
    og_rename_rtc_file, og_rename_srm_file = copy_native_save(pokemon_name)
    
    em = Emulator()
    em.launch_game()
    try:
        with cdtmp(sub_dirname="pokemon_shiny_hunting"):
            pokemon = Pokemon(pokemon_name)
            encounter = StaticEncounter(em, pokemon)
            shiny_found = encounter.find_shiny(max_attempts=10)
            logger.info(f"total number attempts: {encounter.n_attempts}")
    except KeyboardInterrupt as k:
        logger.warning("Keyboard interrupt by user")
        raise k
    except Exception as e:
        logger.error("Exception occurred while shiny hunting")
        raise e
    finally:
        em.kill_process()
        cleanup_save_dir(og_rename_rtc_file, og_rename_srm_file)
