"""This module is intended to be run from the pokemon/ directory."""

# add workspace dir to system path, otherwise cannot import project modules
import os
from typing import Tuple, Dict
import sys
proj_root_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.pardir
)
sys.path.append(proj_root_path)

from bs4 import BeautifulSoup
import requests

from dex import gen_2_dex
from pokemon import create_pokemon_sprite_fn, get_sprite_name
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

POKEMON_DB_BASE_URL = "https://pokemondb.net"


def download_png_img(url: str, path: str) -> bool:
    """Download image from the provided url.
    Assumes image at url is a PNG format."""
    logger.info(f"image url: {url}")
    logger.info(f"image path: {path}")
    try:
        response = requests.get(url)

        if response.status_code != 200:
            logger.error(f"failed! {url}")
            return False

        # if we're here, response was successful so write image to file
        img = open(path, "wb")
        img.write(response.content)
        img.close()

        logger.info(f"success!")
        return True
    except TypeError:
        logger.error(f"failed! {url}")
        return False


def find_sprite_urls(pokemon_name: str,
                     generation: int,
                     game: str) -> Dict[str, str]:
    """Scrape Pokémon DB for the sprite image url(s)."""
    sprite_name = get_sprite_name(pokemon_name)
    sprites_url = f"{POKEMON_DB_BASE_URL}/sprites/{sprite_name}"
    logger.info(f"sprites_url: {sprites_url}")
    soup = load_url(sprites_url)

    table = soup.find("h2", text=f"Generation {generation}").find_next("table")
    rows = table.find_all("tr")
    for row in rows:
        if row.find("th"):
            # don't need the header row
            pass
        else:
            data = row.find_all("td")
            data_game = data[0].text
            if game.lower() not in data_game.lower():
                # not our game so move on to next row
                continue
            normal_img = data[1].find("span", class_="img-fixed")
            normal_img_url = normal_img["data-src"]
            
            shiny_img = data[2].find("span", class_="img-fixed")
            shiny_img_url = shiny_img["data-src"]
            break
    
    return {
        "normal": normal_img_url, "shiny": shiny_img_url
    }


def get_sprite(pokemon_name: str, generation: int, game: str, dirs: Tuple[str, str]):
    normal_dir, shiny_dir = dirs
    normal_fp = create_pokemon_sprite_fn(pokemon_name, game, _dir=normal_dir)
    shiny_fp = create_pokemon_sprite_fn(pokemon_name, game, _dir=shiny_dir)

    if os.path.exists(normal_fp) and os.path.exists(shiny_fp):
        logger.info(f"image path: {normal_fp}")
        logger.info("already exists!")
        logger.info(f"image path: {shiny_fp}")
        logger.info("already exists!")
        return
    
    sprite_img_urls = find_sprite_urls(pokemon_name, generation, game)
    download_png_img(sprite_img_urls["normal"], normal_fp)
    download_png_img(sprite_img_urls["shiny"], shiny_fp)
    return


def load_url(url: str) -> BeautifulSoup:
    """
    Loads the specified url into html and a BeautifulSoup object.

    :param url: The url address
    :return: A BeautifulSoup obj representing the html content at the url
    """

    # request the website content and and instantiate BeautifulSoup obj
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup


def create_output_folders(game: str) -> Tuple[str, str]:
    """Creates relative output folders if they don't already exist."""
    file_dir = os.path.dirname(os.path.realpath(__file__))
    normal_dir = f"{file_dir}/sprites/{game.lower()}/normal"
    shiny_dir = f"{file_dir}/sprites/{game.lower()}/shiny"
    try:
        os.makedirs(normal_dir)
        logger.info(f"created normal dir")
    except OSError:
        logger.info(f"normal dir already exists")
    
    try:
        os.makedirs(shiny_dir)
        logger.info(f"created shiny dir")
    except OSError:
        logger.info(f"shiny dir already exists")
    
    return normal_dir, shiny_dir 


if __name__ == "__main__":
    generation = 2
    game = "Crystal"
    logger.info(f"generation: {generation}")
    logger.info(f"game: {game}")
    pokedex = gen_2_dex()
    logger.info(f"pokedex:\n{pokedex}")

    # create output dir if not already exists
    dirs = create_output_folders(game)
    
    # download sprite for each pokemon
    for index, row in pokedex.iterrows():            
        pokemon_number = row.get("NUMBER")
        pokemon_name = row.get("NAME")
        get_sprite(pokemon_name, generation, game, dirs)
        
