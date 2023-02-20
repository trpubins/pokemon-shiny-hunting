"""Model a Pokémon pack."""

from enum import Enum
import logging
import os
from typing import List, Tuple

from emulator import Emulator
from image import (
    determine_pack_items,
    get_latest_screenshot_fn
)
from helpers.common import delay
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


MAX_PACK_ITEMS = 5
"""The max number of items shown in a single pack screenshot."""


class Pack():
    """Describes all the items in a pack."""
    def __init__(self, emulator: Emulator):
        all_inventory = collect_pack_inventory(emulator)
        self.items,self.machines,self.keyitems,self.balls = all_inventory


class Inventory():
    """Generic class to track inventory."""
    def __init__(self, inventory: List[Tuple[str,int]]):
        self.inventory = dict()
        for name,qty in inventory:
            self.inventory[name] = qty


class InventoryNoQty():
    """Generic class to track inventory without considering quantity."""
    def __init__(self, inventory: List[Tuple[str,int]]):
        self.inventory = list()
        for name,_ in inventory:
            self.inventory.append(name)


class Items(Inventory):
    """Track inventory of pack Items."""
    pass


class KeyItems(InventoryNoQty):
    """Track inventory of pack Key Items."""
    pass


class Machines(Inventory):
    """Track inventory of pack TM/HM."""
    def __init__(self, inventory: List[Tuple[str,int]]):
        super().__init__(inventory)
        self.tm = dict()  # technical machine, TM
        self.hm = list()  # hidden machine, HM
        for name,qty in inventory:
            if qty is not None:
                self.tm[name] = qty
            else:
                self.hm.append(name)


class Balls(Inventory):
    """Track inventory of pack Balls."""
    pass


class BallType(str, Enum):
    """Enumeration for ball types."""
    MASTER = "masterball"
    ULTRA = "ultraball"
    GREAT = "greatball"
    POKE = "pokeball"
    SAFARI = "safariball"
    FAST = "fastball"
    LEVEL = "levelball"
    LURE = "lureball"
    HEAVY = "heavyball"
    LOVE = "loveball"
    FRIEND = "friendball"
    MOON = "moonball"
    SPORT = "sportball"


def collect_pack_inventory(emulator: Emulator) -> Tuple[Items, Machines, KeyItems, Balls]:
    """Collect inventory of all items in the pack."""
    # assume user is in the Pokémon world
    # assume pause menu has not yet been interacted
    emulator.press_start(delay_after_press=0.25)
    emulator.move_down_precise(presses=2)
    emulator.press_a(delay_after_press=0.25)
    
    # get inventory of each section in the pack
    items_list = collect_inventory(emulator, get_qty=True)
    emulator.move_left_precise(presses=1)
    machines_list = collect_inventory(emulator, get_qty=True)
    emulator.move_left_precise(presses=1)
    keyitems_list = collect_inventory(emulator, get_qty=False)
    emulator.move_left_precise(presses=1)
    balls_list = collect_inventory(emulator, get_qty=True)

    # back out of the pause menu
    emulator.press_b(presses=1, delay_after_press=0.5)
    emulator.press_b(presses=1, delay_after_press=0.25)
    
    return (
        Items(items_list), 
        Machines(machines_list),
        KeyItems(keyitems_list),
        Balls(balls_list)
    )

def collect_inventory(emulator: Emulator, get_qty: bool) -> List[Tuple[str, int]]:
    """Generic function to collect inventory for any section in the pack."""
    inventory = []
    unique_pack_items = [None]  # initialize with None element to kick off while loop
    emulator.move_down_precise(presses=MAX_PACK_ITEMS - 1, delay_after_press=0.1)  # assume cursor starts on unique item
    while len(inventory) % MAX_PACK_ITEMS == 0 and len(unique_pack_items) > 0:
        emulator.take_screenshot(delay_after_press=0.25)
        pack_img_fn = get_latest_screenshot_fn()
        pack_items = determine_pack_items(pack_img_fn, get_qty=get_qty)
        os.remove(pack_img_fn)
        
        # add only unique items to inventory
        unique_pack_items = [e for e in pack_items if e not in inventory]
        inventory += unique_pack_items
        emulator.move_down_precise(presses=MAX_PACK_ITEMS, delay_after_press=0.1)
    return inventory


if __name__ == "__main__":
    import __init__
    em = Emulator()
    em.launch_game()
    em.continue_pokemon_game()
    pack = Pack(em)
    logger.info(f"balls: {pack.balls.inventory}")
    logger.info(f"items: {pack.items.inventory}")
    logger.info(f"tm: {pack.machines.tm}")
    logger.info(f"hm: {pack.machines.hm}")
    logger.info(f"key items: {pack.keyitems.inventory}")
    em.kill_process()
