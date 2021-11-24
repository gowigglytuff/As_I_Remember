from random import randint

import pygame
from data import *
from keyboards import InGame

from loading import *
from features import *
from mapClasses import *
from keyboards import *
from inventory import *
from menus import *

mm = MenuManager()
GameData = GameData()
GameController = GameController(GameData, mm)
em = EventsManager(GameData, GameController)
Picaso = Picaso(GameData, GameController)
inv = Inventory(GameController, GameData)
GameController.set_inventory(inv)



def main():
    init_game(GameData, GameController)
    run_game_loop()

def run_game_loop():
    running = True

    # TODO: deal with this phrase stuff
    # NPC1 = Feature(4, 3, 128, 128, ["assets/NPC.png", "assets/NPC - f2.png", "assets/NPC-blue.png"], "Mary")
    Phrase1 = Phrase("Hello World", True, 100, 300, (255, 255, 255), 20)
    Phrase2 = Phrase("Goodbye World", True, 100, 300, (255, 255, 255), 20)

    # set up the events that allow things to move (add these to the individual classes of each of the dudes)
    printout = pygame.USEREVENT + 3
    pygame.time.set_timer(printout, 500)

    while running:
        pygame.draw.rect(GameController.screen, (0, 0, 0), (0, 0, 1000, 10000))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                GameController.current_keyboard_manager.parse_key_pressed(event.key)

            if event.type == pygame.KEYUP:
                GameController.current_keyboard_manager.parse_key_released(event.key)


            # check to see if any events have occurred
            for character in GameData.room_list[GameController.current_room].character_list:
                if event.type == GameData.character_list[character].initiate:
                    if GameData.character_list[character].state == "idle":
                        GameData.character_list[character].do_activity()

            #check for a single step in series of walk cycle steps for each character
            for character in GameData.room_list[GameController.current_room].character_list:
                try:
                    if event.type == GameData.character_list[character].action_clock:
                        GameData.character_list[character].check_if_walking()
                except AttributeError:
                    pass

            # check for a single step in series of walk cycle steps for Player
            if event.type == GameData.player["Player"].step_timer:
                GameData.player["Player"].continue_walking()

        if isinstance(GameController.current_keyboard_manager, InGame):
            if GameController.current_keyboard_manager.current_direction_key is not None:
                if not GameData.player["Player"].check_if_walking():
                    GameData.player["Player"].try_walk(GameController.current_keyboard_manager.current_direction_key)

        Picaso.big_draw()
        pygame.display.update()
        GameController.tick()


if __name__ == "__main__":
    main()