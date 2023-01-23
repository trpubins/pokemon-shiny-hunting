"""High-level emulator functionality and tracking emulator state."""

from enum import Enum
import logging
import os
import platform

import pyautogui as gui

from config import EMULATOR_NAME, POKEMON_GAME, RETROARCH_APP_FP
from controller import EmulatorController, press_key
from pokemon import Pokemon
from helpers.delay import delay
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
    
    def continue_pokemon_game(self):
        """Continue the Pokémon game from last save."""
        logger.debug("continue game")
        # TODO - need to implement
        # assume game has been launched
        # need to get past load screen and press through Continue

    def launch_game(self):
        """Launch the game inside the emulator."""
        self.launch()

        logger.debug("navigating to game")
        if platform.system() == "Darwin":
            press_key("left", delay_after_press=0.5)
            press_key("down", presses=2, delay_after_press=0.5)
            press_key("right", delay_after_press=0.5)
        elif platform.system() == "Windows":
            press_key("right", presses=3, in_game=False)
        press_key("Enter", in_game=False)
        delay(0.5)

        logger.debug(f"run game: Pokémon {POKEMON_GAME}")
        press_key("Enter", in_game=False)
    
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
        delay(3)  # ensure sys is fully open & ready to perform next action
    
    def find_shiny(self, pokemon: Pokemon, static_enounter: bool = True) -> bool:
        """Find a shiny Pokémon."""
        if static_enounter:
            # TODO - implement functionality using separate module, encounter.py
            pass
        # until implemented, always return True
        return True

    def reset(self):
        """Reset the emulator."""
        self.cont.press_reset_btn()
        logger.debug("emulator reset")
    
    def take_screenshot(self):
        """Take a screenshot in the emulator."""
        self.cont.press_screenshot_btn()
        logger.debug("screenshot taken")
    
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
    em.launch_game()