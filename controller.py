"""Programmatically control I/O devices."""

import logging
import platform

import pyautogui as gui           #pyautogui is great for hotkeys and utilizing special characters on the system level, but it cannot register output in the applications
if platform.system() == "Windows":
    import pydirectinput as inp   #pydirect input is perfect for controlling common button presses with the emulator development

from config import RETROARCH_CFG_FP
from helpers.delay import delay
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
        fullscreen_btn_str = "input_toggle_fullscreen = "

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
                elif fullscreen_btn_str in line:
                    self.fullscreen_btn = _clean_line(line, fullscreen_btn_str)
                else:
                    pass
    
    def press_a(self, presses: int = 1, delay_after_press: float = None):
        press_key(self.a_btn, presses, delay_after_press=delay_after_press)
        logger.debug(f"pressed a button {presses}x")
    
    def press_b(self, presses: int = 1, delay_after_press: float = None):
        press_key(self.b_btn, presses, delay_after_press=delay_after_press)
        logger.debug(f"pressed b button {presses}x")
    
    def press_start(self, delay_after_press: float = None):
        press_key(self.start_btn, delay_after_press=delay_after_press)
        logger.debug(f"pressed start button")
    
    def press_select(self, delay_after_press: float = None):
        press_key(self.select_btn, delay_after_press=delay_after_press)
        logger.debug(f"pressed select button")
    
    def move_up(self, presses: int = 1, delay_after_press: float = None):
        press_key(self.up_btn, presses, delay_after_press=delay_after_press)
        logger.debug(f"moved up {presses}x")
    
    def move_down(self, presses: int = 1, delay_after_press: float = None):
        press_key(self.down_btn, presses, delay_after_press=delay_after_press)
        logger.debug(f"moved down {presses}x")
    
    def move_left(self, presses: int = 1, delay_after_press: float = None):
        press_key(self.left_btn, presses, delay_after_press=delay_after_press)
        logger.debug(f"moved left {presses}x")
    
    def move_right(self, presses: int = 1, delay_after_press: float = None):
        press_key(self.right_btn, presses, delay_after_press=delay_after_press)
        logger.debug(f"moved right {presses}x")
    
    def toggle_fast_fwd(self, delay_after_press: float = None):
        press_key(self.fast_fwd_btn, delay_after_press=delay_after_press)
        logger.debug(f"toggled fast forward")

    def press_reset_btn(self, delay_after_press: float = None):
        press_key(self.reset_btn, delay_after_press=delay_after_press)
        logger.debug(f"pressed reset button")
    
    def press_screenshot_btn(self, delay_after_press: float = None):
        press_key(self.screenshot_btn, delay_after_press=delay_after_press)
        logger.debug(f"pressed screenshot button")
    
    def press_fullscreen_btn(self, presses: int = 1, delay_after_press: float = None):
        press_key(self.fullscreen_btn, presses, delay_after_press=delay_after_press)
        logger.debug(f"pressed fullscreen button {presses}x")


def press_key(key: str,
              presses: int = 1,
              delay_after_press: float = None,
              in_game: bool = True):
    """Virtually press the specified key."""
    for i in range(presses):
        if platform.system() == "Darwin":
            gui.keyDown(key)
            gui.keyUp(key)
        elif platform.system() == "Windows":
            if in_game:
                inp.typewrite(key)
            else:
                inp.press(key)
        logger.debug(f"pressed key: {key}")
        if delay_after_press is not None:
            delay(delay_after_press)
