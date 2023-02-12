"""Manages a user configuration."""

from configparser import ConfigParser, NoOptionError
import os

from retroarch import RetroArchConfig
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

PROJ_ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
CFG_FN = os.path.join(PROJ_ROOT_PATH, "config.ini")
SECTION = "DEFAULT"
EMULATOR_NAME = "RetroArch"

logger.debug(f"parsing: {CFG_FN}")
if not os.path.isfile(CFG_FN):
    raise FileNotFoundError(f"Unable to locate {CFG_FN}. Create {CFG_FN} according to https://docs.python.org/3.9/library/configparser.html#quick-start with {SECTION} section.")

config = ConfigParser()
config.read(CFG_FN)

RETROARCH_APP_FP = config.get(SECTION, "RETROARCH_APP_FP")
RETROARCH_CFG_FP = config.get(SECTION, "RETROARCH_CFG_FP")
RETROARCH_CFG = RetroArchConfig(RETROARCH_CFG_FP)

EMULATOR_CORE_AVG_FPS = int(config.get(SECTION, "EMULATOR_CORE_AVG_FPS"))
ROM_NAME = config.get(SECTION, "ROM_NAME")
POKEMON_GAME = config.get(SECTION, "POKEMON_GAME")
POKEMON_STATIC_ENCOUNTER = config.get(SECTION, "POKEMON_STATIC_ENCOUNTER")
try:
    LOG_LEVEL = config.get(SECTION, "LOG_LEVEL")
except NoOptionError:
    LOG_LEVEL = "INFO"  # default to INFO logging level
try:
    USERNAME = config.get(SECTION, "USERNAME")
except NoOptionError:
    USERNAME = "User"
try:
    RECEIVER_EMAIL = config.get(SECTION, "RECEIVER_EMAIL")
    SENDER_EMAIL = config.get(SECTION, "SENDER_EMAIL")
    SENDER_EMAIL_PASS = config.get(SECTION, "SENDER_EMAIL_PASS")
except NoOptionError:
    RECEIVER_EMAIL = None
    SENDER_EMAIL = None
    SENDER_EMAIL_PASS = None
try:
    DISP_BRIGHTNESS = float(config.get(SECTION, "DISP_BRIGHTNESS"))
except NoOptionError:
    DISP_BRIGHTNESS = None 


logger.info(f"RETROARCH_CFG_FP: {RETROARCH_CFG_FP}")
logger.info(f"RETROARCH_APP_FP: {RETROARCH_APP_FP}")
logger.info(f"EMULATOR_CORE_AVG_FPS: {EMULATOR_CORE_AVG_FPS}")
logger.info(f"ROM_NAME: {ROM_NAME}")
logger.info(f"POKEMON_GAME: {POKEMON_GAME}")
logger.info(f"POKEMON_STATIC_ENCOUNTER: {POKEMON_STATIC_ENCOUNTER}")
logger.info(f"LOG_LEVEL: {LOG_LEVEL}")
logger.info(f"USERNAME: {USERNAME}")
logger.info(f"RECEIVER_EMAIL: {RECEIVER_EMAIL}")
logger.info(f"SENDER_EMAIL: {SENDER_EMAIL}")
logger.info(f"SENDER_EMAIL_PASS: {SENDER_EMAIL_PASS}")
logger.info(f"DISP_BRIGHTNESS: {DISP_BRIGHTNESS}")
