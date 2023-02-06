import config
from calibration import logger as calibration_logger
from controller import logger as controller_logger
from dex import logger as dex_logger
from emulator import logger as emulator_logger
from encounter import logger as encounter_logger
from image import logger as image_logger
from main import logger as main_logger
from notifications import logger as notifications_logger
from pokemon import logger as pokemon_logger
from helpers.common import logger as helpers_common_logger
from helpers.tmp import logger as helpers_tmp_logger
from helpers.log import get_logger


calibration_logger = get_logger(calibration_logger.name, config.LOG_LEVEL)
controller_logger = get_logger(controller_logger.name, config.LOG_LEVEL)
dex_logger = get_logger(dex_logger.name, config.LOG_LEVEL)
emulator_logger = get_logger(emulator_logger.name, config.LOG_LEVEL)
encounter_logger = get_logger(encounter_logger.name, config.LOG_LEVEL)
image_logger = get_logger(image_logger.name, config.LOG_LEVEL)
main_logger = get_logger(main_logger.name, config.LOG_LEVEL)
notifications_logger = get_logger(notifications_logger.name, config.LOG_LEVEL)
pokemon_logger = get_logger(pokemon_logger.name, config.LOG_LEVEL)
helpers_common_logger = get_logger(helpers_common_logger.name, config.LOG_LEVEL)
helpers_tmp_logger = get_logger(helpers_tmp_logger.name, config.LOG_LEVEL)