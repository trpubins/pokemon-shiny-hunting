# pokemon-shiny-hunting

Automate the shiny-hunting process for a Pokémon emulator.

## Config File

Inside the project root directory, create a file named `config.ini`. Below is an example:

```ini
[DEFAULT]
RETROARCH_DIR: /Users/<UserName>/Library/Application Support/RetroArch
RETROARCH_CFG_FP: %(RETROARCH_DIR)s/config/retroarch.cfg
RETROARCH_SCREENSHOTS_DIR: %(RETROARCH_DIR)s/screenshots
RETROARCH_APP_FP: /Applications/RetroArch.app
POKEMON_GAME: Crystal
LOG_LEVEL: DEBUG  # or INFO
```

## Usage

***Important❗***: ALL scripts must be executed from the project root directory.

```bash
cd <path-to>/pokemon-shiny-hunting
```

### Python environment

First ensure your python environment is up to date.

```bash
pip install -r requirements.txt
```

### main

The `main.py` script is the primary application, making use of the other modules. Activate your python environment first and run:

```bash
python main.py
```

### tests

Use the test scripts to perform unit testing. After developing new functionality, add new test(s). Create a new function in an existing test script or create a new test script entirely if a new module was created. For test function names, strictly follow the format: `test_n_<function_name>` where `n` is the test number in the test script.

By default, a given test script executes all the tests in that script. Optionally, provide `--test-number` at the command line to run a specific test.

```bash
# runs all tests in the specified script
python tests/test_image.py
```

```bash
# runs only test 4 in the specified script
python tests/test_image.py --test-number 4
```

You can also run all test scripts at once with:

```bash
# runs all test scripts
python tests/test_all.py
```
