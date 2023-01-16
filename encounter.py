from helpers.delay import delay
from emulator import Emulator

class Encounter():
    static_encounter = ["Sudowoodo", "Suicune", "Lugia", "Ho-Oh", "Celebi"]

    def __init__(self):
        self.em = Emulator()
        self.cont = self.em.cont
    
    def start_game(self):
        delay(1)
        self.em.fast_fwd_on()
        self.cont.press_a(presses=3, delay_after_press=0.25)

    def encounter_static(self, pokemon: str):
        if pokemon == "Suicune":
            self.cont.move_up(presses=2)
            delay(2)
            self.cont.press_a()
        else:
            self.cont.press_a(presses=2, delay_after_press=2)

if __name__ == "__main__":
    en = Encounter()
    en.em.run_game()
    en.start_game()
    en.encounter_static("Suicune")