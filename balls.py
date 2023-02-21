import logging

import pandas as pd

from emulator import Emulator, ToggleState
from pack import Pack, BallType, collect_inventory

from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))

DATA= pd.read_csv("pokemon.csv") #Read in catch rate and weight for best ball calculations

def highlight_best_ball(list: list[tuple[str, int]]):
    """Hover cursor over best ball in pocket"""
    em.press_start(delay_after_press= 0.5)
    em.press_a(delay_after_press= 0.5)
    best = id_best_ball(list)
    for ball in list:
        if ball[0] == best:
            presses = len(list) - list.index(ball)              #Assumes that cursor is currently hovering over cancel from the check
    em.move_up_precise(presses= presses, delay_after_press=0.25)

def id_best_ball(list: list[tuple[str, int]]) -> str:
    """Returns the string of best ball in pocket"""
    best = 13 # number of different ball types used in game
    best_name = ""
    for ball in list:
        if ball[1] <= best:
            best = ball[1]
            best_name = ball[0]
    return best_name        

def id_ball_hierarchy(list: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Establishes hierarchy of balls in pocket"""
    hiearchy = []
    for ball in list:
        bt = BallType(ball[0])
        index = (bt.ordered_ball())
        hiearchy.append([ball[0], index])
    return hiearchy

if __name__ == "__main__":
    import __init__
    em = Emulator()
    em.state.run = ToggleState.ON              #Change depending on if game is already preloaded to enhance speed
    if  em.state.run != ToggleState.ON:         #If game is closed, do full launch
        em.launch_game()
        em.continue_pokemon_game()
        pack = Pack(em)
        ball_dict = pack.balls.inventory
        ball_inv = [(k, v) for k, v in ball_dict.items()]
    else:                                       #If game is already open (state of pack cannot change; cursor 
                                                #already on pack and balls pocket already open)
        em.state.fast_fwd = ToggleState.ON      #Standard value for fast forward when game is already running
        em.press_start(delay_after_press=0.25)
        em.press_a()
        ball_inv = collect_inventory(em, True)
        em.press_b(presses=2, delay_after_press=0.5)
    logger.info(f"current ball inventory: {ball_inv}")
    hier = id_ball_hierarchy(ball_inv)
    logger.info(f"ranking of current balls: {hier}")
    logger.info(f"best ball in pocket is {id_best_ball(hier)}")
    highlight_best_ball(ball_inv)