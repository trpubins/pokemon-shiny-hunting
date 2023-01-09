"""Programmatically control I/O devices."""

import logging
import platform
import time

import pyautogui as gui           #pyautogui is great for hotkeys and utilizing special characters on the system level, but it cannot register output in the applications
if platform.system() == "Windows":
    import pydirectinput as inp   #pydirect input is perfect for controlling common button presses with the emulator development

from config import RETROARCH_CFG_FP
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


class EmulatorController():
    """Make controller actions inside an emulator."""
    def __init__(self, player_num: int = 1):
        self.player_num = player_num
        
        # parse the retroarch config file
        keybind = f"input_player{player_num}_"
        a_btn_str = f"{keybind}a = "
        b_btn_str = f"{keybind}b = "
        start_btn_str = f"{keybind}start = "
        select_btn_str = f"{keybind}select = "
        up_btn_str = f"{keybind}up = "
        down_btn_str = f"{keybind}down = "
        left_btn_str = f"{keybind}left = "
        right_btn_str = f"{keybind}right = "
        fast_fwd_btn_str = "input_toggle_fast_forward = "
        reset_btn_str = "input_reset = "
        screenshot_btn_str = "input_screenshot = "

        def _clean_line(line: str, sub_str: str) -> str:
            return line.replace(sub_str, "").replace("\"", "").replace("\n", "")

        with open(RETROARCH_CFG_FP, "r") as infile:
            for line in infile:
                if a_btn_str in line:
                    self.a_btn = _clean_line(line, a_btn_str)
                elif b_btn_str in line:
                    self.b_btn = _clean_line(line, b_btn_str)
                elif start_btn_str in line:
                    self.start_btn = _clean_line(line, start_btn_str)
                elif select_btn_str in line:
                    self.select_btn = _clean_line(line, select_btn_str)
                elif up_btn_str in line:
                    self.up_btn = _clean_line(line, up_btn_str)
                elif down_btn_str in line:
                    self.down_btn = _clean_line(line, down_btn_str)
                elif left_btn_str in line:
                    self.left_btn = _clean_line(line, left_btn_str)
                elif right_btn_str in line:
                    self.right_btn = _clean_line(line, right_btn_str)
                elif fast_fwd_btn_str in line:
                    self.fast_fwd_btn = _clean_line(line, fast_fwd_btn_str)
                elif reset_btn_str in line:
                    self.reset_btn = _clean_line(line, reset_btn_str)
                elif screenshot_btn_str in line:
                    self.screenshot_btn = _clean_line(line, screenshot_btn_str)
                else:
                    pass
    
    def press_a(self):
        self._press_btn_emulator(self.a_btn)
        logger.debug(f"pressed a button")
    
    def press_b(self):
        self._press_btn_emulator(self.b_btn)
        logger.debug(f"pressed b button")
    
    def press_start(self):
        self._press_btn_emulator(self.start_btn)
        logger.debug(f"pressed start button")
    
    def press_select(self):
        self._press_btn_emulator(self.select_btn)
        logger.debug(f"pressed select button")
    
    def move_up(self):
        self._press_btn_emulator(self.up_btn)
        logger.debug(f"moved up")
    
    def move_down(self):
        self._press_btn_emulator(self.down_btn)
        logger.debug(f"moved down")
    
    def move_left(self):
        self._press_btn_emulator(self.left_btn)
        logger.debug(f"moved left")
    
    def move_right(self):
        self._press_btn_emulator(self.right_btn)
        logger.debug(f"moved right")
    
    def toggle_fast_fwd(self):
        self._press_btn_emulator(self.fast_fwd_btn)
        logger.debug(f"toggled fast forward")

    def press_reset_btn(self):
        self._press_btn_emulator(self.reset_btn)
        logger.debug(f"pressed reset button")
    
    def press_screenshot_btn(self):
        self._press_btn_emulator(self.screenshot_btn)
        logger.debug(f"pressed screenshot button")
    
    def _press_btn_emulator(self, btn: str):
        if platform.system() == "Darwin":
            _press_mac_key(btn)
        elif platform.system() == "Windows":
            inp.typewrite(btn)


def nav_to_game():
    logger.debug("navigating to game")
    if platform.system() == "Darwin":
        press_key("left")
        delay(0.5)
        press_key("down", presses=2)
        delay(0.5)
        press_key("right")
        delay(0.5)
        press_key("enter")
    elif platform.system() == "Windows":
        press_key("right", presses=3)
        press_key("Enter")


def delay(sec: int):
    logger.debug(f"delay {sec}s")
    time.sleep(sec)


def press_key(key: str, presses: int = 1):
    if platform.system() == "Darwin":
        _press_mac_key(key, presses)
    elif platform.system() == "Windows":
        _press_win_key(key, presses)


def _press_win_key(key: str, presses: int = 1):
    inp.press(key, presses=presses)


def _press_mac_key(key: str, presses: int = 1):
    for i in range(presses):
        gui.keyDown(key)
        gui.keyUp(key)
        logger.debug(f"pressed key: {key}")
