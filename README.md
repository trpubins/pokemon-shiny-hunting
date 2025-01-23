# pokemon-shiny-hunting

Automate the shiny-hunting process for a Pokémon emulator.

## Getting Started

### Prerequisites

1. Python 3.9 | 3.10 | 3.11 installed on system

>WARNING: Dependency build errors occur with Python 3.12 or later.

### Set Up Environment

To create the dev environment, navigate to the project root directory and run the following

```bash
make setup [PYTHON3=python3]
```

>NOTE: This command creates a virtual environment to `./.venv` and downloads all the
packages required to debug/test the source code as well as other developer tools. Specify
a minor version of Python 3 using the `PYTHON3=python3.<minor>` arg.

If the dev environment has already been setup, then the dependencies can be updated with

```bash
make update [PYTHON3=python3]
```

### Project Config File

Inside the project root directory, create a file named `config.ini`. Below is an example:

```ini
[DEFAULT]
RETROARCH_DIR: /Users/<UserName>/Library/Application Support/RetroArch  # optional (str)
RETROARCH_CFG_FP: %(RETROARCH_DIR)s/config/retroarch.cfg                # required (str)
RETROARCH_APP_FP: /Applications/RetroArch.app                           # required (str)
EMULATOR_CORE_AVG_FPS: 300                                              # required (int)
ROM_NAME: Name_of_Your_ROM_no_ext                                       # required (str)
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

- User Interface > Menu > ozone
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

### server

>Note: server shell scripts are written for bash shell environments

As an added feature, an Asynchronous Server Gateway Interface (ASGI) server has been designed with API endpoints available to run, status, and stop the `main` shiny hunting application. The endpoints are as follows:

| Endpoint                    | Description                                                                                   |
|-----------------------------|-----------------------------------------------------------------------------------------------|
| /                           | Provides status on the server (available or busy)                                             |
| /shiny_hunt/{pokemon_name}  | Launches a new static encounter shiny hunt if server is available                             |
| /status_hunt                | Provides a progress report on the hunt, namely if/not shiny found and the number of attempts  |
| /stop_hunt                  | Stops hunting for a pokemon                                                                   |

To run the server, you must first have the environment variable `POKEMON_PROJ_PATH` set to the directory containing this README. Navigate into the server directory and in a bash terminal run:

```bash
./run_server.sh
```

Similarly, to kill the process running the uvicorn server, navigate into the server directory and in a bash terminal run:

```bash
./kill_server.sh
```
