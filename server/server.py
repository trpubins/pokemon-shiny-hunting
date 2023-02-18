"""Serves up endpoints to drive the pokemon shiny hunting application."""

import logging
from multiprocessing import Process, Queue
# add workspace dir to system path, otherwise cannot import project modules
import os
import sys
proj_root_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.pardir
)
sys.path.append(proj_root_path)
from typing import Tuple

from fastapi import FastAPI, Response, status

import __init__
from main import run as go_shiny_hunt
from emulator import Emulator
from encounter import StaticEncounter
from pokemon import Pokemon
from helpers.log import mod_fname
logger = logging.getLogger(mod_fname(__file__))


# globals
app = FastAPI()
app.pokemon: Pokemon = None
app.shiny_found: bool = False
app.n_attempts: int = 0
app.bkgd_process: Process = None  # prefer process over background task (thread) so that we can easily terminate it
app.queue: Queue = Queue()  # requried for multiprocess communication

# 4 endpoints:
#### /            - Provides status on the server (available or busy)
#### /shiny_hunt  - Launches a new static encounter shiny hunt if server is available
#### /status_hunt - Provides a progress report on the hunt, namely if/not shiny found and the number of attempts
#### /stop_hunt   - Stops hunting for a pokemon

@app.get("/", status_code=status.HTTP_200_OK)
def status_server():
    if is_server_available():
        msg = "Server Available"
    else:
        msg = "Server Busy"
    logger.info(f"response: {msg}")
    return msg


@app.get("/shiny_hunt/{pokemon_name}", status_code=status.HTTP_200_OK)
async def shiny_hunt(pokemon_name: str, resp: Response):
    
    logger.info(f"received {pokemon_name} as path parameter")

    if not is_server_available():
        resp.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        msg = "Servery Busy"
        logger.info(f"response: {msg}")
        return msg

    # create objects and init server state variables
    emulator = Emulator()
    pokemon = Pokemon(pokemon_name)
    encounter = StaticEncounter(emulator, pokemon)
    app.pokemon = pokemon
    app.shiny_found = False
    app.n_attempts = 0

    # execute hunt in the background (asynchronously)
    kwargs = {
        "emulator": emulator,
        "encounter": encounter,
        "queue": app.queue
    }
    app.bkgd_process = Process(target=go_shiny_hunt, kwargs=kwargs)
    app.bkgd_process.start()
    
    # provide response immediately
    msg = f"Started shiny hunt for {encounter.pokemon.name}"
    logger.info(f"response: {msg}")
    return msg


@app.get("/status_hunt", status_code=status.HTTP_200_OK)
def status_hunt():
    if is_server_available() and not did_hunting_commence():
        msg = "No hunt to status"
    else:
        shiny_found, n_attempts = get_app_state()
        if shiny_found:
            msg = f"Shiny {app.pokemon.name} found after {n_attempts} attempts"
        else:
            msg = f"No shiny {app.pokemon.name} found after {n_attempts} attempts"
    logger.info(f"response: {msg}")
    return msg


@app.get("/stop_hunt", status_code=status.HTTP_200_OK)
def stop_hunt():
    if is_server_available():
        msg = "No hunt to stop"
    else:
        _, n_attempts = get_app_state()
        logger.warning(f"terminating pid {app.bkgd_process.pid}")
        app.bkgd_process.terminate()
        app.bkgd_process = None
        msg = f"Stopped hunting {app.pokemon.name} after {n_attempts} attempts"
    logger.info(f"response: {msg}")
    return msg


def is_server_available() -> bool:
    """Uses server state to determine if it is available for new request."""
    return app.bkgd_process is None or not app.bkgd_process.is_alive()


def did_hunting_commence() -> bool:
    """Determine if hunting has started or not."""
    return app.n_attempts > 0


def get_app_state() -> Tuple[bool, int]:
    """Retrieve the state of the shiny hunting application."""
    if not app.queue.empty():
        logger.info("queue contains data. updating server state")
        app_state = app.queue.get()
        app.shiny_found = app_state["shiny_found"]
        app.n_attempts = app_state["n_attempts"]
    else:
        logger.info("queue is empty")
    
    return app.shiny_found, app.n_attempts
