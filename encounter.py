import logging

from emulator import Emulator

from helpers.delay import delay
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))

class Encounter():
    static_encounter = ["Sudowoodo", "Suicune", "Lugia", "Ho-Oh", "Celebi"]

    def __init__(self):
        self.em = Emulator()
        self.cont = self.em.cont
    
    def start_game(self):
        delay(1)
        self.em.fast_fwd_on()
        self.cont.press_a(presses=3, delay_after_press=0.5)
        logger.info("start menu finished")

    def encounter_static(self, pokemon: str):
        if pokemon == "Suicune":
            self.cont.move_up(presses=2)
            delay(2)
            self.cont.press_a()
        else:
            self.cont.press_a(presses=2, delay_after_press=2)
        logger.info("battle commenced")
            

    def catch_pokemon(self):
        self.em.fast_fwd_off()
        self.cont.move_down()
        self.cont.press_a()
        self.cont.move_right()
        self.cont.press_a(presses=2)

if __name__ == "__main__":
    en = Encounter()
    en.em.run_game()
    en.start_game()
    en.encounter_static("Suicune")