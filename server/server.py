"""Serves up endpoints to drive the pokemon shiny hunting application."""

import logging
# add workspace dir to system path, otherwise cannot import project modules
import os
import sys
proj_root_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.pardir
)
sys.path.append(proj_root_path)

from fastapi import BackgroundTasks, FastAPI, Response, status
from starlette.requests import Request

import __init__
from emulator import Emulator
from encounter import StaticEncounter
from image import get_latest_screenshot_fn
from notifications import send_notification
from pokemon import Pokemon
from helpers.file_mgmt import cdtmp
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


# globals
app = FastAPI()
app.emulator: Emulator = None
app.encounter: StaticEncounter = None
app.server_available: bool = True

# 4 endpoints:
#### /            - Provides status on the server (available or busy)
#### /shiny_hunt  - Launches a new static encounter shiny hunt if server is available
#### /status_hunt - Provides a progress report on the hunt, namely if/not shiny found and the number of attempts
#### /stop_hunt   - Stops hunting for a pokemon

@app.get("/", status_code=status.HTTP_200_OK)
def status_server():
    if app.server_available:
        msg = "Server Available"
    else:
        msg = "Server Busy"
    return {"message": msg}


@app.get("/shiny_hunt/{pokemon_name}", status_code=status.HTTP_200_OK)
async def shiny_hunt(pokemon_name: str, background_tasks: BackgroundTasks, resp: Response):
    
    logger.info(f"received {pokemon_name} as path parameter")

    if not app.server_available:
        resp.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "message": "Server Busy"
        }
    
    # update server state
    app.server_available = False

    # create objects and assign to state variables
    emulator = Emulator()
    pokemon = Pokemon(pokemon_name)
    encounter = StaticEncounter(emulator, pokemon)
    app.emulator = emulator
    app.encounter = encounter

    # execute hunt in the background (asynchronously)
    background_tasks.add_task(go_shiny_hunt, emulator, encounter, logger)
    
    # return get response to lambda to avoid task timeout
    return {
        "message": f"Started shiny hunt for {encounter.pokemon.name}"
    }


@app.get("/status_hunt", status_code=status.HTTP_200_OK)
def stop_hunt():
    if app.server_available:
        msg = "No hunt to status"
    else:
        if app.encounter.shiny_found:
            msg = f"Shiny {app.encounter.pokemon.name} found after {app.encounter.n_attempts} attempts"
        else:
            msg = f"No shiny {app.encounter.pokemon.name} found after {app.encounter.n_attempts} attempts"
    return {"message": msg}


@app.get("/stop_hunt", status_code=status.HTTP_200_OK)
def stop_hunt():
    if app.server_available:
        msg = "No hunt to stop"
    else:
        kill_emulator_process(app.emulator)
        msg = f"Stopped hunting {app.encounter.pokemon.name}"
    return {"message": msg}


def go_shiny_hunt(emulator: Emulator, encounter: StaticEncounter, logger: logging.Logger):
    """Try to find a shiny from a static encounter."""
    emulator.launch_game()
    try:
        with cdtmp(sub_dirname="pokemon_shiny_hunting"):
            shiny_found = encounter.find_shiny(max_attempts=8000)
            logger.info(f"total number attempts: {encounter.n_attempts}")
    except KeyboardInterrupt as k:
        logger.warning("Keyboard interrupt by user")
        kill_emulator_process(emulator)
        raise k
    except Exception as e:
        logger.error("Exception occurred while shiny hunting")
        kill_emulator_process(emulator)
        raise e
    
    if shiny_found:
        emulator.save_state()
        emulator.fast_fwd_off()
        emulator.pause_on()
        attachments = [get_latest_screenshot_fn()]
    else:
        kill_emulator_process(emulator)
        attachments = []
    send_notification(encounter.pokemon, encounter.n_attempts, shiny_found,
                      attachments=attachments, send=True)


def kill_emulator_process(emulator: Emulator):
    """Kill the process running the emulator and
    indicate the server is once again available."""
    emulator.kill_process()
    app.server_available = True