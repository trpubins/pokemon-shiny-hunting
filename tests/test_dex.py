import click

import __init__

from dex import get_pokemon_number, gen_2_dex
from helpers import test_util
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

MODULE = "dex.py"


def test_1_get_pokemon_number():
    logger.info("Test 1 - get_pokemon_number")
    assert(get_pokemon_number("bulbasaur") == 1)
    assert(get_pokemon_number("BULBASAUR") == 1)
    assert(get_pokemon_number("MEW") == 151)
    assert(get_pokemon_number("celebi") == 251)
    logger.info("Test 1 - success!")


def test_2_gen_2_dex():
    logger.info("Test 2 - gen_2_dex")
    df = gen_2_dex()
    assert(df.shape[0] == 251)
    bulbasaur = df.loc[df["NAME"].str.upper() == "BULBASAUR"]
    assert(bulbasaur.get("NUMBER").values[0] == 1)
    celebi = df.loc[df["NAME"].str.upper() == "CELEBI"]
    assert(celebi.get("NUMBER").values[0] == 251)
    logger.info("Test 2 - success!")


@click.command()
@click.option("-n", "--test-number", required=False, type=int,
              help="The test number to run.")
def run_tests(test_number: int = None):
    logger.info(f"Testing {MODULE}")
    
    if test_number is None:
        test_util.run_tests(module_name=__name__)
    else:
        try:
            test_util.run_tests(module_name=__name__, test_number=test_number)
        except ValueError as e:
            logger.error(f"Invalid test_number specified: {test_number}")
            raise e
    logger.info("All tests pass!")


if __name__ == "__main__":
    run_tests()