import logging

from emulator import Emulator

from helpers.delay import delay
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))

class Encounter():
    static_encounter = [
        {"name": "Electrode", "max_moves": 70, "explode": True},
        {"name": "Gyarados", "max_moves": 85, "explode": False},
        {"name": "Lapras", "max_moves": 100, "explode": False},
        {"name": "Snorlax", "max_moves": 60, "explode": False},
        {"name": "Sudowoodo", "max_moves": 60, "explode": False},
        {"name": "Suicune", "max_moves": 95, "explode": False},
        {"name": "Lugia", "max_moves": 65, "explode": False},
        {"name": "Ho-Oh", "max_moves": 65, "explode": False},
        {"name": "Celebi", "max_moves": 50, "explode": False},
        ]

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
        self.em.fast_fwd_on()


if __name__ == "__main__":
    en = Encounter()
    en.em.run_game()
    en.start_game()
    en.encounter_static("Suicune")