import logging

import __init__
from emulator import Emulator
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


if __name__ == "__main__":
    logger.info("running main")
    em = Emulator()
    em.run_game()
