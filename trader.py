import logging
import os
import platform

from controller import press_key
from emulator import Emulator
from helpers.delay import delay

class Trader():

    def __init__(self) -> None:
        self.em = Emulator()
    
    def open_menu_overlay(self):
        self.em.cont.open_menu()
        self.em.cont.back_menu()
        press_key("left", presses=3, delay_after_press=0.1, in_game=False)
        press_key("down", presses=3, delay_after_press=0.1, in_game=False)
        press_key("Enter", in_game=False)
        press_key("down", in_game=False)
        press_key("Enter", presses=2, delay_after_press=0.1, in_game=False)
        press_key("down", presses=2, delay_after_press=0.1, in_game=False)
        press_key("Enter", presses=2, delay_after_press=0.1, in_game=False)
    
    def begin_trade(self):
        self.em.cont.press_a(presses=6, delay_after_press=.66)


if __name__ == "__main__":
    tr = Trader()
    tr.em.run_game()
    delay(1)
    tr.open_menu_overlay()
    