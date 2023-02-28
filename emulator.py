"""High-level emulator functionality and tracking emulator state."""

from enum import Enum
from inspect import signature
import logging
import os

from config import EMULATOR_NAME, POKEMON_GAME, RETROARCH_APP_FP, DISP_BRIGHTNESS
from controller import EmulatorController, press_key
from image import is_in_battle
from helpers.common import delay, set_disp_brightness
from helpers.file_mgmt import cd
from helpers.platform import Platform
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
        delay(1, universal=True)
        self.fast_fwd_on()
        delay(1, universal=False)
        self.press_b(presses=1, delay_after_press=0.5)
        self.press_a(presses=1, delay_after_press=0.25)
        self.press_a(presses=2, delay_after_press=0.5)

    def launch_game(self):
        """Launch the game inside the emulator."""
        self.launch()
        set_disp_brightness(DISP_BRIGHTNESS)

        logger.debug("navigating to game")
        # assume RetroArch menu driver set to ozone
        press_key("left", delay_after_press=0.1, delay_universal=True)
        press_key("down", presses=2, delay_after_press=0.1, delay_universal=True)
        press_key("right", delay_after_press=0.1, delay_universal=True)
        press_key("Enter")
        delay(0.25, universal=True)

        logger.info(f"run game: Pokémon {POKEMON_GAME}")
        self.state.game_run()
        press_key("Enter")
    
    def launch(self):
        """Launch the emulator application."""
        logger.info(f"launching {EMULATOR_NAME} emulator")
        logger.debug(f"opening {RETROARCH_APP_FP}")
        if Platform.is_mac():
            os.system(f"open {RETROARCH_APP_FP}")
        elif Platform.is_windows():
            with cd(os.path.dirname(RETROARCH_APP_FP)):
                exe = os.path.basename(RETROARCH_APP_FP)
                os.system(f"start {exe}")
        delay(3, universal=True)  # ensure sys is fully open & ready to perform next action
    
    def quit(self):
        """Quit the emulator."""
        logger.info(f"quitting {EMULATOR_NAME} emulator")
        self.cont.press_exit_btn(presses=2, delay_after_press=0.25)
        set_disp_brightness(DISP_BRIGHTNESS)
        self.state.game_off()
    
    def kill_process(self):
        """Kill the emulator process."""
        logger.info(f"killing {EMULATOR_NAME} process")
        if Platform.is_mac():
            app_name, _ = os.path.basename(RETROARCH_APP_FP).split(".")
            os.system(f"killall {app_name}")
        elif Platform.is_windows():
            exe = os.path.basename(RETROARCH_APP_FP)
            os.system(f"taskkill /IM {exe}")
        delay(1, universal=True)
        set_disp_brightness(DISP_BRIGHTNESS)
        self.state.game_off()
        

    def interact(func):
        """Interact with controls inside the emulator.
        To ensure safe interaction, turn off fast fwd prior
        to action. Resumes original fast fwd state after action."""
        n_params = len(signature(func).parameters)
        def wrapper_func(self, presses: int = 1, delay_after_press: float = None):
            fast_fwd_orig_state = self.state.fast_fwd
            self.fast_fwd_off()
            delay(0.5, universal=True)
            
            # call Emulator method based on the method's number of parameters
            if n_params == 3:
                func(self, presses, delay_after_press)
            else:
                func(self, delay_after_press)
            
            if fast_fwd_orig_state == ToggleState.ON:
                self.fast_fwd_on()
        return wrapper_func
    
    @interact
    def press_a_precise(self, presses: int = 1, delay_after_press: float = None):
        """Press the A button with precision (guarantees exact number of presses)."""
        self.cont.press_a(presses, delay_after_press)
    
    def press_a(self, presses: int = 1, delay_after_press: float = None):
        """Press the A button."""
        self.cont.press_a(presses, delay_after_press)
    
    @interact
    def press_b_precise(self, presses: int = 1, delay_after_press: float = None):
        """Press the B button with precision (guarantees exact number of presses)."""
        self.cont.press_b(presses, delay_after_press)
    
    def press_b(self, presses: int = 1, delay_after_press: float = None):
        """Press the B button."""
        self.cont.press_b(presses, delay_after_press)
    
    def press_start(self, delay_after_press: float = None):
        """Press the START button."""
        self.cont.press_start(delay_after_press)
    
    def press_select(self, delay_after_press: float = None):
        """Press the SELECT button."""
        self.cont.press_select(delay_after_press)
    
    @interact
    def move_up_precise(self, presses: int = 1, delay_after_press: float = None):
        """Move UP using the d-pad with precision (guarantees exact number of presses)."""
        self.cont.move_up(presses, delay_after_press)
    
    def move_up(self, presses: int = 1, delay_after_press: float = None):
        """Move UP using the d-pad."""
        self.cont.move_up(presses, delay_after_press)
    
    @interact
    def move_down_precise(self, presses: int = 1, delay_after_press: float = None):
        """Move DOWN using the d-pad with precision (guarantees exact number of presses)."""
        self.cont.move_down(presses, delay_after_press)
    
    def move_down(self, presses: int = 1, delay_after_press: float = None):
        """Move DOWN using the d-pad."""
        self.cont.move_down(presses, delay_after_press)
    
    @interact
    def move_left_precise(self, presses: int = 1, delay_after_press: float = None):
        """Move LEFT using the d-pad with precision (guarantees exact number of presses)."""
        self.cont.move_left(presses, delay_after_press)
    
    def move_left(self, presses: int = 1, delay_after_press: float = None):
        """Move LEFT using the d-pad."""
        self.cont.move_left(presses, delay_after_press)
    
    @interact
    def move_right_precise(self, presses: int = 1, delay_after_press: float = None):
        """Move RIGHT using the d-pad with precision (guarantees exact number of presses)."""
        self.cont.move_right(presses, delay_after_press)
    
    def move_right(self, presses: int = 1, delay_after_press: float = None):
        """Move RIGHT using the d-pad."""
        self.cont.move_right(presses, delay_after_press)
    
    def reset(self, delay_after_press: float = None):
        """Reset the emulator."""
        self.cont.press_reset_btn(delay_after_press)
        logger.debug("emulator reset")
    
    def take_screenshot(self, delay_after_press: float = None):
        """Take a screenshot in the emulator."""
        self.cont.press_screenshot_btn(delay_after_press)
        logger.debug("screenshot taken")
    
    def save_state(self, delay_after_press: float = None):
        """Save the emulator state."""
        self.cont.press_save_state_btn(delay_after_press)
        logger.info("saved emulator state")
    
    def load_state(self, delay_after_press: float = None):
        """Load the emulator state."""
        self.cont.press_load_state_btn(delay_after_press)
        logger.info("loaded emulator state")
    
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
    
    def pause_on(self):
        """Turn pause ON."""
        if self.state.is_pause_off():
            self.cont.toggle_pause()
            self.state.pause_on()
        logger.debug("pause is ON")
    
    def pause_off(self):
        """Turn pause OFF."""
        if self.state.is_pause_on():
            self.cont.toggle_pause()
            self.state.pause_off()
        logger.debug("pause is OFF")


class EmulatorState():
    """Track state inside an emulator."""
    def __init__(self):
        self.fast_fwd = ToggleState.OFF
        self.pause = ToggleState.OFF
        self.run = ToggleState.OFF
        self.battle = ToggleState.OFF
        self.game = POKEMON_GAME
    
    def is_fast_fwd_on(self) -> bool:
        return self.fast_fwd == ToggleState.ON
    
    def is_fast_fwd_off(self) -> bool:
        return self.fast_fwd == ToggleState.OFF
    
    def is_pause_on(self) -> bool:
        return self.pause == ToggleState.ON
    
    def is_pause_off(self) -> bool:
        return self.pause == ToggleState.OFF
    
    def is_game_run(self) -> bool:
        return self.run == ToggleState.ON

    def is_game_off(self) -> bool:
        return self.run == ToggleState.OFF

    def fast_fwd_on(self):
        self.fast_fwd = ToggleState.ON
    
    def fast_fwd_off(self):
        self.fast_fwd = ToggleState.OFF
    
    def pause_on(self):
        self.pause = ToggleState.ON
    
    def pause_off(self):
        self.pause = ToggleState.OFF

    def game_run(self):
        self.run = ToggleState.ON

    def game_off(self):
        self.run = ToggleState.OFF
    
    def battle_state(self) -> ToggleState:
        if is_in_battle():
            self.battle = ToggleState.ON
            logger.info("BattleState is ON")
        else:
            self.battle = ToggleState.OFF
            logger.info("BattleState is OFF")
        return self.battle

if __name__ == "__main__":
    em = Emulator()
    em.launch_game()