"""Manages the RetroArch configuration."""

class RetroArchConfig():
    """Store key RetroArch settings in memory."""
    def __init__(self, config_fp: str):
        config = _parse_retroarch_config(config_fp)
        
        # paths
        self.cheat_db_path = config["cheat_database_path"]
        self.cores_dir = config["libretro_directory"]
        self.log_dir = config["log_dir"]
        self.savefile_dir = config["savefile_directory"]
        self.savestate_dir = config["savestate_directory"]
        self.screenshot_dir = config["screenshot_directory"]

        # buttons
        self.fast_fwd_btn = config["input_toggle_fast_forward"]
        self.pause_btn_str = config["input_pause_toggle"]
        self.reset_btn_str = config["input_reset"]
        self.screenshot_btn_str = config["input_screenshot"]
        self.fullscreen_btn_str = config["input_toggle_fullscreen"]
        self.save_state_btn_str = config["input_save_state"]
        self.load_state_btn_str = config["input_load_state"]
        self.exit_btn_str = config["input_exit_emulator"]
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
            replace("=", "").replace(" ", "").replace("\n", "")
    
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