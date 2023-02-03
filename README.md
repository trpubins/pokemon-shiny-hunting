# pokemon-shiny-hunting

Automate the shiny-hunting process for a Pokémon emulator.

## Config File

Inside the project root directory, create a file named `config.ini`. Below is an example:

```ini
[DEFAULT]
RETROARCH_DIR: /Users/<UserName>/Library/Application Support/RetroArch  # required (str)
RETROARCH_CFG_FP: %(RETROARCH_DIR)s/config/retroarch.cfg                # required (str)
RETROARCH_SCREENSHOTS_DIR: %(RETROARCH_DIR)s/screenshots                # required (str)
RETROARCH_APP_FP: /Applications/RetroArch.app                           # required (str)
POKEMON_GAME: Crystal                                                   # required (str)
POKEMON_STATIC_ENCOUNTER: Suicune                                       # required (str)
LOG_LEVEL: DEBUG                                                        # optional (str), default is INFO
USERNAME: your-username                                                 # optional (str), default is User
RECEIVER_EMAIL: receiver@email.com                                      # optional (str), default is None
SENDER_EMAIL: sender@email.com                                          # optional (str), default is None
SENDER_EMAIL_PASS: sEndeR-EmaiL-pa22                                    # optional (str), default is None
DISP_BRIGHTNESS: 0.5                                                    # optional (float between [0,1]), default is None
```

## RetroArch Config

In order to successfully run the program, ensure the following RetroArch settings are as follows:

- Video > GPU Screenshot > OFF
- On-Screen Display > On-Screen Notifications > Notification Visibility > Screenshot Notification Persistence > Instant
- Input > Polling Behavior > Normal

Lastly, ensure that all controls mapped to the keyboard work as expected when the game is running in the emulator. See Input > Port 1 Controls in RetroArch settings.

## Dependencies

### Python environment

First ensure your python environment is up to date.

```bash
pip install -r requirements.txt
```

### Other packages

If user is running on Mac and wants the application to set their display's brightness, they are required to install a CLI [display brightness utility](https://github.com/nriley/brightness) for macOS.
It can be easily installed with Homebrew:

```bash
brew install brightness
```

Note: the `brightness` utility is optional. Application will function fine without utilizing the display brightness feature.

## Usage

***Important❗***: ALL scripts must be executed from the project root directory.

```bash
cd <path-to>/pokemon-shiny-hunting
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
