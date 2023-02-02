import logging
import os
import platform


import __init__
from controller import EmulatorController, press_key
from emulator import Emulator
from pokemon import Pokemon

from helpers.delay import delay
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


class Trader():

    def __init__(self) -> None:
        self.em1 = Emulator()
        self.cont = self.em1.cont
        self.cont2 = EmulatorController(player_num=2)
        
        
    def press_btn(self, btn: str, presses: int = 1, delay_after_press: float = 0):
        for i in range(0, presses):
            if btn == 'a':
                self.cont.press_a(presses=1)
                self.cont2.press_a(presses=1)
            if btn == 'b':
                self.cont.press_b(presses=1)
                self.cont2.press_b(presses=1)
            if btn == 'up':
                self.cont.move_up(presses=1)
                self.cont2.move_up(presses=1)
            if btn == 'down':
                self.cont.move_down(presses=1)
                self.cont2.move_down(presses=1)
            if btn == 'left':
                self.cont.move_left(presses=1)
                self.cont2.move_left(presses=1)
            if btn == 'right':
                self.cont.move_right(presses=1)
                self.cont2.move_right(presses=1)
            delay(delay_after_press)
    
    def open_menu_overlay(self):
        '''Establishes setup for 2 player Link. Only available with SameBoy/TGB Dual emulator'''
        self.cont.open_menu()
        self.cont.back_menu()
        press_key("left", presses=3, delay_after_press=0.2, in_game=False)
        press_key("down", presses=2, delay_after_press=0.2, in_game=False)
        press_key("Enter", presses=2, delay_after_press=0.3,in_game=False)
        press_key("down",delay_after_press=0.3, in_game=False)
        press_key("Enter", presses=3, delay_after_press=0.1, in_game=False)
        press_key("down", presses=2, delay_after_press=0.1, in_game=False)
        press_key("Enter", presses=3, delay_after_press=0.1, in_game=False)
    
    # def open_game(self):
    #     '''Runs through startup menus. Ensures both emulators open simultaneously'''
    #     self.em1.fast_fwd_on()
    #     delay(3)
    #     self.cont.press_b(presses=3, delay_after_press=0.1)
    #     delay(2)
    #     self.cont.press_a(presses=3, delay_after_press=0.1)
    
    def open_game(self):
        '''Runs through startup menus. Ensures both emulators open simultaneously'''
        self.em1.fast_fwd_on()
        delay(3)
        self.press_btn(btn='b', presses=3, delay_after_press=0.1)
        delay(2)
        self.press_btn(btn='a', presses=3, delay_after_press=0.1)
        logger.info("startup finished")

    # def begin_trade(self):
    #     '''Saves game and prepares trade'''
    #     self.cont.press_a(presses=10, delay_after_press=2)
    #     self.cont.press_b(presses=10, delay_after_press=.5)
    #     delay(5)
    #     self.em1.fast_fwd_off()
    #     # establish setup of player two in chair first
    #     self.cont.move_up(presses=2, delay_after_press=1)
    #     self.cont.move_right(presses=2, delay_after_press=1)
    #     self.cont.move_up(delay_after_press=1)
    #     self.cont.move_left(presses=3, delay_after_press=1)
    #     # force player two into trade menu to desynchronize overworld movement
    #     self.cont.press_a(delay_after_press=0.1)
    #     # establish setup of player one in chair
    #     self.cont.move_up(delay_after_press=1)
    #     self.cont.move_right(delay_after_press=1)
    #     # begin trading for both players
    #     self.cont.press_a(delay_after_press=0.1)

    def begin_trade(self):
        '''Saves game and prepares trade'''
        self.press_btn(btn='a', presses=10, delay_after_press=1)
        self.press_btn(btn='b', presses=10, delay_after_press=.5)
        delay(3)
        self.em1.fast_fwd_off()
        # establish setup of player two in chair first
        self.press_btn(btn='up', presses=2, delay_after_press=1)
        self.cont2.move_right(presses=2, delay_after_press=1)
        self.press_btn(btn= 'up', delay_after_press=1)
        self.press_btn(btn= 'left', presses=2, delay_after_press=1)
        # force player two into trade menu to desynchronize overworld movement
        self.press_btn(btn = 'a', delay_after_press=0.1)
        # establish setup of player one in chair
        self.cont.move_up(delay_after_press=1)
        self.cont.move_right(delay_after_press=1)
        # begin trading for both players
        self.press_btn(btn = 'a', delay_after_press=0.1)

    def trade_pokemon(self, t1: list, t2:list) -> list:
        if len(t1) < len(t2):
            less_poke = t1
        elif len(t2) < len(t1):
            less_poke = t2
        else:
            less_poke = t1
        
        for poke in range(len(less_poke)):
            # if poke > 0 :
            #     self.press_btn(btn = 'down', delay_after_press=0.1)
            self.press_btn(btn = 'a', delay_after_press=2)
            self.press_btn(btn = 'right', delay_after_press=2)
            self.press_btn(btn= 'a', delay_after_press=0.1)


if __name__ == "__main__":
    trainer_1 = ['Lugia', 'Pidgeot', 'Meganium', 'Chinchou', 'Electrode', 'Ursaring']
    trainer_2 = ['Cyndaquil', 'Sentret', 'Sentret']
    
    tr = Trader()
    tr.em1.run_game()
    delay(1)
    # tr.open_menu_overlay()
    tr.open_game()
    tr.begin_trade()
    delay(10)
    tr.trade_pokemon(trainer_1, trainer_2)