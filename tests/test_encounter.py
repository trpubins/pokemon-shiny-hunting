
import __init__

import image as im
from encounter import Encounter
from pokemon import Pokemon, SpriteType

if __name__ == "__main__":
    en = Encounter()
    en.em.run_game()
    test = SpriteType.NORMAL
    counter = 0
    while test != SpriteType.SHINY:
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
        if test == SpriteType.SHINY:
            break
        else:
            counter += 1
            print(counter)
            en.em.reset()
    print("Shiny Found!")
    
    
    

