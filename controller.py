"""Programmatically control I/O devices."""

import logging

#pyautogui is for hotkeys and inputs at the system level, cannot register inputs inside the emulator core
import pyautogui as gui

from config import RETROARCH_CFG
from helpers.common import delay
from helpers.platform import Platform
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))

if Platform.is_windows():
    #pydirectinput is for controlling common button presses within the emulator
    import pydirectinput as inp


class EmulatorController():
    """Make controller actions inside an emulator."""
    def __init__(self, player_num: int = 1):
        self.player_num = player_num
        
        if player_num == 1:
            self.input_player = RETROARCH_CFG.input_player_1
        elif player_num == 2:
            self.input_player = RETROARCH_CFG.input_player_2
        else:
            raise RuntimeError(f"Only acceping player1 and player2 inputs at this time.\
                Update retroarch.py to include more player inputs.")
    
    def press_a(self, presses: int = 1, delay_after_press: float = None):
        press_key(self.input_player.a_btn, presses, delay_after_press=delay_after_press)
        logger.debug(f"pressed a button {presses}x")
    
    def press_b(self, presses: int = 1, delay_after_press: float = None):
        press_key(self.input_player.b_btn, presses, delay_after_press=delay_after_press)
        logger.debug(f"pressed b button {presses}x")
    
    def press_start(self, delay_after_press: float = None):
        press_key(self.input_player.start_btn, delay_after_press=delay_after_press)
        logger.debug(f"pressed start button")
    
    def press_select(self, delay_after_press: float = None):
        press_key(self.input_player.select_btn, delay_after_press=delay_after_press)
        logger.debug(f"pressed select button")
    
    def move_up(self, presses: int = 1, delay_after_press: float = None):
        press_key(self.input_player.up_btn, presses, delay_after_press=delay_after_press)
        logger.debug(f"moved up {presses}x")
    
    def move_down(self, presses: int = 1, delay_after_press: float = None):
        press_key(self.input_player.down_btn, presses, delay_after_press=delay_after_press)
        logger.debug(f"moved down {presses}x")
    
    def move_left(self, presses: int = 1, delay_after_press: float = None):
        press_key(self.input_player.left_btn, presses, delay_after_press=delay_after_press)
        logger.debug(f"moved left {presses}x")
    
    def move_right(self, presses: int = 1, delay_after_press: float = None):
        press_key(self.input_player.right_btn, presses, delay_after_press=delay_after_press)
        logger.debug(f"moved right {presses}x")
    
    def toggle_fast_fwd(self, delay_after_press: float = None):
        press_key(RETROARCH_CFG.fast_fwd_btn, delay_after_press=delay_after_press)
        logger.debug(f"toggled fast forward")
    
    def toggle_pause(self, delay_after_press: float = None):
        press_key(RETROARCH_CFG.pause_btn, delay_after_press=delay_after_press)
        logger.debug(f"toggled pause")

    def press_reset_btn(self, delay_after_press: float = None):
        press_key(RETROARCH_CFG.reset_btn, delay_after_press=delay_after_press)
        logger.debug(f"pressed reset button")
    
    def press_screenshot_btn(self, delay_after_press: float = None):
        press_key(RETROARCH_CFG.screenshot_btn, delay_after_press=delay_after_press)
        logger.debug(f"pressed screenshot button")
    
    def press_fullscreen_btn(self, presses: int = 1, delay_after_press: float = None):
        press_key(RETROARCH_CFG.fullscreen_btn, presses, delay_after_press=delay_after_press)
        logger.debug(f"pressed fullscreen button {presses}x")
    
    def press_save_state_btn(self, delay_after_press: float = None):
        press_key(RETROARCH_CFG.save_state_btn, delay_after_press=delay_after_press)
        logger.debug(f"pressed save state button")
    
    def press_load_state_btn(self, delay_after_press: float = None):
        press_key(RETROARCH_CFG.load_state_btn, delay_after_press=delay_after_press)
        logger.debug(f"pressed load state button")
    
    def press_exit_btn(self, presses: int = 1, delay_after_press: float = None):
        press_key(RETROARCH_CFG.exit_btn, presses, delay_after_press=delay_after_press)
        logger.debug(f"pressed exit button {presses}x")


def press_key(key: str,
              presses: int = 1,
              delay_after_press: float = None,
              delay_universal: bool = False):
    """Virtually press the specified key."""
    for i in range(presses):
        if Platform.is_mac():
            gui.keyDown(key)
            gui.keyUp(key)
        elif Platform.is_windows():
            inp.press(key)
        logger.debug(f"pressed key: {key}")
        if delay_after_press is not None:
            delay(delay_after_press, delay_universal)
