"""High-level emulator functionality and tracking emulator state."""

from enum import Enum
import logging
import os
import platform

import pyautogui as gui

from config import EMULATOR_NAME, POKEMON_GAME, RETROARCH_APP_FP
from controller import EmulatorController, delay, nav_to_game, press_key
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


class ToggleState(str, Enum):
    """Enumeration for toggling on/off."""
    ON = 'on'
    OFF = 'off'


class Emulator():
    """Take actions inside an emulator."""
    def __init__(self):
        self.cont = EmulatorController()
        self.state = EmulatorState()
    
    def run_game(self):
        """Run the game inside the emulator."""
        self.launch()
        delay(2)  # ensure sys is opening with proper time to perform navigation
        nav_to_game()
        delay(0.5)
        press_key("Enter")
    
    def launch(self):
        """Launch the emulator application."""
        logger.info(f"launching {EMULATOR_NAME} emulator")
        if platform.system() == "Darwin":
            logger.debug(f"opening {RETROARCH_APP_FP}")
            os.system(f"open {RETROARCH_APP_FP}")
        elif platform.system() == "Windows":
            gui.hotkey("ctrl", "esc")
            gui.write(EMULATOR_NAME)
            gui.press("Enter")

    def fast_fwd_on(self):
        """Turn fast forwad ON."""
        if self.state.is_fast_fwd_off():
            self.cont.toggle_fast_fwd()
            self.state.fast_fwd_on()
        logger.debug("fast forward is ON")
    
    def fast_fwd_off(self):
        """Turn fast forwad OFF."""
        if self.state.is_fast_fwd_on():
            self.cont.toggle_fast_fwd()
            self.state.fast_fwd_off()
        logger.debug("fast forward is OFF")
    
    def reset(self):
        """Reset the emulator."""
        self.cont.press_reset_btn()
        logger.debug("emulator reset")
    
    def take_screenshot(self):
        """Take a screenshot in the emulator."""
        self.cont.press_screenshot_btn()
        logger.debug("screenshot taken")


class EmulatorState():
    """Track state inside an emulator."""
    def __init__(self):
        self.fast_fwd = ToggleState.OFF
        self.game = POKEMON_GAME
    
    def is_fast_fwd_on(self) -> bool:
        return self.fast_fwd == ToggleState.ON
    
    def is_fast_fwd_off(self) -> bool:
        return self.fast_fwd == ToggleState.OFF
    
    def fast_fwd_on(self):
        self.fast_fwd = ToggleState.ON
    
    def fast_fwd_off(self):
        self.fast_fwd = ToggleState.OFF


if __name__ == "__main__":
    em = Emulator()
    em.run_game()