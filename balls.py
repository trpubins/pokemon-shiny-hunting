import logging

import pandas as pd

from emulator import Emulator, ToggleState
from encounter import StaticEncounter
from pack import Pack, BallType, collect_inventory
from pokemon import Pokemon

from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))

DATA= pd.read_csv("pokemon.csv") #Read in catch rate and weight for best ball calculations

def highlight_best_ball(list: list[tuple[str, int]], battle: ToggleState = ToggleState.ON) -> int:
    """Hover cursor over best ball in pocket"""
    if battle != ToggleState.ON:
        em.press_start(delay_after_press= 0.5)
        em.press_a(delay_after_press= 0.5)                          #Assumes that cursor is currently over Pack in Menu
        best = id_best_ball(id_ball_hierarchy(list))
        for ball in list:
            if ball[0] == best:
                actions = len(list) - list.index(ball)              #Assumes that cursor is currently hovering over cancel from the check
        em.move_up_precise(presses= actions, delay_after_press=0.25)
    else:
        em.move_down(delay_after_press=0.25)
        em.press_a(delay_after_press=0.25)
        best = id_best_ball(id_ball_hierarchy(list))
        for ball in list:
            if ball[0] == best:
                actions = list.index(ball)                          #Assumes that cursor is currently hovering over top option
        em.move_down_precise(presses= actions, delay_after_press=0.25)
        return actions

def id_best_ball(hierarchy: list[tuple[str, int]]) -> str:
    """Returns the string of best ball in pocket"""
    best = 13 # number of different ball types used in game
    best_name = ""
    for ball in hierarchy:
        if ball[1] <= best:
            best = ball[1]
            best_name = ball[0]
    logger.info(f"best ball in pocket is {best_name}")
    return best_name        

def id_ball_hierarchy(list: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Establishes hierarchy of balls in pocket"""
    hierarchy = []
    for ball in list:
        bt = BallType(ball[0])
        index = (bt.ordered_ball())
        hierarchy.append([ball[0], index])
    logger.info(f"ranking of current balls: {hierarchy}")
    return hierarchy

def throw_best_ball(inventory: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Throws best ball in pocket available"""
    num = highlight_best_ball(inventory, em.state.battle_state())
    em.press_a(presses=2, delay_after_press=0.5)
    logger.info("ball thrown")
    for ball in inventory:
        if inventory.index(ball) == num:
            ball_list = list(ball)
            ball_list[1] -= 1
            if ball_list[1] == 0:
                del inventory[num]
            else:
                ball = tuple(ball_list)
                inventory[num] = ball
    logger.info(f"current ball inventory: {inventory}")
    return inventory

if __name__ == "__main__":
    import __init__
    from config import POKEMON_STATIC_ENCOUNTER
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
        em.press_a(delay_after_press=1)         #Cannot use press_b twice on Mac when Retroarch is already open? Is opening up my Notes application
        em.press_start(delay_after_press=1)     #Press_a for cancel and Press_start to exit menu
    logger.info(f"current ball inventory: {ball_inv}")
    hier = id_ball_hierarchy(ball_inv)
    em.take_screenshot()
    while em.state.battle_state() == ToggleState.OFF:
        pokemon = Pokemon(POKEMON_STATIC_ENCOUNTER)
        encounter = StaticEncounter(em, pokemon)
        encounter._encounter_static()
        em.press_b(presses=5, delay_after_press=0.25)
        em.take_screenshot()
    ball_inv = throw_best_ball(ball_inv)
    
