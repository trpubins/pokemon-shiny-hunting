"""Manages the RetroArch configuration."""

import logging
import os
import shutil
from typing import Tuple

from helpers.file_mgmt import cd
from helpers.platform import Platform
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


class RetroArchConfig():
    """Store key RetroArch settings in memory."""
    def __init__(self, config_fp: str):
        config = _parse_retroarch_config(config_fp)
        
        # paths
        def _make_abs_path(dir:str, config_fp: str) -> str:
            if dir.startswith(":\\") and Platform.is_windows():
                rel_path = dir.replace(":", ".")
                config_dir = os.path.dirname(config_fp)
                with cd(config_dir):
                    abs_path = os.path.abspath(rel_path)
            elif dir.startswith("~") and Platform.is_mac():
                abs_path = os.path.expanduser(dir)
            else:
                abs_path = dir
            return abs_path
    
        self.cheat_db_path = _make_abs_path(config["cheat_database_path"], config_fp)
        self.cores_dir = _make_abs_path(config["libretro_directory"], config_fp)
        self.log_dir = _make_abs_path(config["log_dir"], config_fp)
        self.savefile_dir = _make_abs_path(config["savefile_directory"], config_fp)
        self.savestate_dir = _make_abs_path(config["savestate_directory"], config_fp)
        self.screenshot_dir = _make_abs_path(config["screenshot_directory"], config_fp)

        # buttons
        self.fast_fwd_btn = config["input_toggle_fast_forward"]
        self.pause_btn = config["input_pause_toggle"]
        self.reset_btn = config["input_reset"]
        self.screenshot_btn = config["input_screenshot"]
        self.fullscreen_btn = config["input_toggle_fullscreen"]
        self.save_state_btn = config["input_save_state"]
        self.load_state_btn = config["input_load_state"]
        self.exit_btn = config["input_exit_emulator"]
        self.input_player_1 = RetroArchInputPlayerConfig(config["input_player1_"])
        self.input_player_2 = RetroArchInputPlayerConfig(config["input_player2_"])


class RetroArchInputPlayerConfig():
    """Store RetroArch input settings in memory."""
    def __init__(self, input: dict):
        self.a_btn = input["a"]
        self.b_btn = input["b"]
        self.start_btn = input["start"]
        self.select_btn = input["select"]
        self.up_btn = input["up"]
        self.down_btn = input["down"]
        self.left_btn = input["left"]
        self.right_btn = input["right"]
        

def _parse_retroarch_config(config_fp: str) -> dict:
    # Note: RetroArch config file has keys sorted alphabetically

    if not os.path.isfile(config_fp):
        raise FileNotFoundError(f"Unable to locate {config_fp}.")

    # parse the retroarch config file
    cheat_db_path = "cheat_database_path "
    cores_dir = "libretro_directory "
    log_dir = "log_dir "
    savefile_dir = "savefile_directory "
    savestate_dir = "savestate_directory "
    screenshot_dir = "screenshot_directory "
    
    fast_fwd_btn = "input_toggle_fast_forward "
    pause_btn = "input_pause_toggle "
    reset_btn = "input_reset "
    screenshot_btn = "input_screenshot "
    fullscreen_btn = "input_toggle_fullscreen "
    save_state_btn = "input_save_state "
    load_state_btn = "input_load_state "
    exit_btn = "input_exit_emulator "

    input_player = "input_player"
    
    def _clean_line(line: str, sub_str: str) -> str:
        return line.replace(sub_str, "").replace("\"", "").\
            replace("=", "").replace("\n", "").strip()
    
    config = dict()
    with open(config_fp, "r") as infile:
        for line in infile:
            if cheat_db_path in line:
                config[cheat_db_path.strip()] = _clean_line(line, cheat_db_path)
            elif cores_dir in line:
                config[cores_dir.strip()] = _clean_line(line, cores_dir)
            elif log_dir in line:
                config[log_dir.strip()] = _clean_line(line, log_dir)
            elif savefile_dir in line:
                config[savefile_dir.strip()] = _clean_line(line, savefile_dir)
            elif savestate_dir in line:
                config[savestate_dir.strip()] = _clean_line(line, savestate_dir)
            elif screenshot_dir in line:
                config[screenshot_dir.strip()] = _clean_line(line, screenshot_dir)
            elif fast_fwd_btn in line:
                config[fast_fwd_btn.strip()] = _clean_line(line, fast_fwd_btn)
            elif pause_btn in line:
                config[pause_btn.strip()] = _clean_line(line, pause_btn)
            elif reset_btn in line:
                config[reset_btn.strip()] = _clean_line(line, reset_btn)
            elif screenshot_btn in line:
                config[screenshot_btn.strip()] = _clean_line(line, screenshot_btn)
            elif fullscreen_btn in line:
                config[fullscreen_btn.strip()] = _clean_line(line, fullscreen_btn)
            elif save_state_btn in line:
                config[save_state_btn.strip()] = _clean_line(line, save_state_btn)
            elif load_state_btn in line:
                config[load_state_btn.strip()] = _clean_line(line, load_state_btn)
            elif exit_btn in line:
                config[exit_btn.strip()] = _clean_line(line, exit_btn)
            elif input_player in line:
                input,player_num,_ = line.split("_", 2)
                keybind = f"{input}_{player_num}_"
                if keybind not in config:
                    config[keybind] = dict()
                
                # add trailing space to ensure correct button-key mapping
                a_btn_str = f"{keybind}a "
                b_btn_str = f"{keybind}b "
                start_btn_str = f"{keybind}start "
                select_btn_str = f"{keybind}select "
                up_btn_str = f"{keybind}up "
                down_btn_str = f"{keybind}down "
                left_btn_str = f"{keybind}left "
                right_btn_str = f"{keybind}right "

                if a_btn_str in line:
                    config[keybind]["a"] = _clean_line(line, a_btn_str)
                elif b_btn_str in line:
                    config[keybind]["b"] = _clean_line(line, b_btn_str)
                elif start_btn_str in line:
                    config[keybind]["start"] = _clean_line(line, start_btn_str)
                elif select_btn_str in line:
                    config[keybind]["select"] = _clean_line(line, select_btn_str)
                elif up_btn_str in line:
                    config[keybind]["up"] = _clean_line(line, up_btn_str)
                elif down_btn_str in line:
                    config[keybind]["down"] = _clean_line(line, down_btn_str)
                elif left_btn_str in line:
                    config[keybind]["left"] = _clean_line(line, left_btn_str)
                elif right_btn_str in line:
                    config[keybind]["right"] = _clean_line(line, right_btn_str)
                else:
                    pass
            else:
                pass
    
    return config


def copy_native_save(pokemon_name: str,
                     user_rom_name: str,
                     native_saves_dir: str,
                     retroarch_saves_dir: str) -> Tuple[str, str]:
    """Copy native save for this Pokémon static encounter
    into the user's saves dir."""
    pokemon_name = pokemon_name.lower().capitalize()
    logger.info(f"copying native save files for {pokemon_name} -> savefiles dir")

    calibrate_rom_name = "Pokemon - Crystal Version (UE) (V1.1) [C][!]"
    calibrate_rtc_path = os.path.join(native_saves_dir, pokemon_name, f"{calibrate_rom_name}.rtc")
    calibrate_srm_path = os.path.join(native_saves_dir, pokemon_name, f"{calibrate_rom_name}.srm")
    og_rtc_path = os.path.join(retroarch_saves_dir, f"{user_rom_name}.rtc")
    og_srm_path = os.path.join(retroarch_saves_dir, f"{user_rom_name}.srm")

    # rename original files as to not overwrite user's current saves
    og_rename_rtc_path = os.path.join(retroarch_saves_dir, "og_file.rtc")
    if os.path.exists(og_rename_rtc_path):
        # don't do anything if og_file already exists
        # (artifact from previous hunt where shiny was found)
        logger.debug(f"original file already exists and is renamed: {og_rename_rtc_path}")
    elif os.path.exists(og_rtc_path):
        os.rename(og_rtc_path, og_rename_rtc_path)
        logger.debug(f"renamed {og_rtc_path} -> {og_rename_rtc_path}")
    else:
        og_rename_rtc_path = None
    
    og_rename_srm_path = os.path.join(retroarch_saves_dir, "og_file.srm")
    if os.path.exists(og_rename_srm_path):
        # don't do anything if og_file already exists
        # (artifact from previous hunt where shiny was found)
        logger.debug(f"original file already exists and is renamed: {og_rename_srm_path}")
    elif os.path.exists(og_srm_path):
        os.rename(og_srm_path, og_rename_srm_path)
        logger.debug(f"renamed {og_srm_path} -> {og_rename_srm_path}")
    else:
        og_rename_srm_path = None
    
    # copy calibration save files over to savefile dir, then rename
    shutil.copy(calibrate_rtc_path, og_rtc_path)
    shutil.copy(calibrate_srm_path, og_srm_path)
    logger.debug(f"copied {calibrate_rtc_path} -> {og_rtc_path}")
    logger.debug(f"copied {calibrate_srm_path} -> {og_srm_path}")

    return og_rename_rtc_path, og_rename_srm_path


def cleanup_save_dir(user_rom_name: str,
                     retroarch_saves_dir: str,
                     renamed_rtc_file: str,
                     renamed_srm_file: str):
    """Cleanup the RetroArch saves directory."""
    logger.info("cleaning up the savefiles dir")
    og_rtc_file = os.path.join(retroarch_saves_dir, f"{user_rom_name}.rtc")
    og_srm_file = os.path.join(retroarch_saves_dir, f"{user_rom_name}.srm")

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
