
import __init__

import image as im
from encounter import Encounter
from pokemon import Pokemon, SpriteType

def test_for_shiny():
    en = Encounter()
    en.em.run_game()
    test = SpriteType.NORMAL
    counter = 0
    while test != SpriteType.SHINY and counter <= 3:
        en.start_game()
        en.encounter_static("Suicune")
        en.em.take_screenshot()
        shot = im.get_latest_screenshot_fn()
        name = im.crop_name_in_battle(shot)
        name = im.determine_name(name)
        sprite = im.crop_pokemon_in_battle(shot)
        pokemon = Pokemon(name)
        test = im.determine_sprite_type(pokemon, sprite)
        print(test)
        counter += 1
        print(counter)
        if test == SpriteType.SHINY:
            print("Shiny Found!")
            break
        elif counter > 3:
            break
        else:
            en.em.reset()
    en.catch_pokemon()

if __name__ == "__main__":
    test_for_shiny()
    
    
    

