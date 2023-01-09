import config
from controller import logger as controller_logger
from dex import logger as dex_logger
from emulator import logger as emulator_logger
from helpers.log import get_logger


controller_logger = get_logger(controller_logger.name, config.LOG_LEVEL)
dex_logger = get_logger(dex_logger.name, config.LOG_LEVEL)
emulator_logger = get_logger(emulator_logger.name, config.LOG_LEVEL)
