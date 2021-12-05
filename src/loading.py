

import pygame
from data import *
from features import *
from mapClasses import *
from room_page import *
from TileMap import *
from keyboards import *
from random import randrange
from inventory import *

def init_game(gd_input, gc_input):
    '''
    :type gc_input: GameController
    :type gd_input: GameData
    :return:
    '''
    # initialize pygame
    pygame.init()
    pygame.display.set_caption('As I Remember')
    pygame.key.set_repeat()

    # Load all the differnt keyboard modes that the you encounter when in different things like the menus and stuff
    load_keyboard_managers(gc_input, gd_input)

    # load all the different menus
    load_menus(gc_input, gd_input)

    # load the full list of items that are available in the game
    load_items(gc_input, gd_input)

    # load the full list of key items that are available in the game
    load_key_items(gc_input, gd_input)

    # Load the Tileset
    FT = TileSet("assets/csv_maps/csv_tiles/Full_Tileset_Adjusted.png", 32, 32,40, 40)
    BT = TileSet("assets/csv_maps/csv_tiles/Big_Tileset.png", 32, 32, 40, 10)
    T = TileSet("assets/csv_maps/csv_tiles/tileset.png", 32, 32, 3, 5)
    # store each tile in a dictionary in GameData that will be accessed by the TileMap function
    gd_input.add_tile_dict(FT.load_tile_images())

    # add the player to the game
    gd_input.add_player("Player", Player(2, 3, gc_input, gd_input))
    gd_input.player["Player"].activate_timer()

    # run functions that initiate all rooms
    init_all_rooms(gc_input, gd_input)


def load_keyboard_managers(GameController, GameData):
    # load all keyboard managers
    # TODO: add other possible Keyboard_managers
    GameController.add_keyboard_manager(InGame.ID, InGame(GameController, GameData))
    GameController.add_keyboard_manager(InStartMenu.ID, InStartMenu(GameController, GameData))
    GameController.add_keyboard_manager(InConversation.ID, InConversation(GameController, GameData))
    GameController.add_keyboard_manager(InConversationOptions.ID, InConversationOptions(GameController, GameData))
    GameController.add_keyboard_manager(InInventory.ID, InInventory(GameController, GameData))
    GameController.add_keyboard_manager(InKeyInventory.ID, InKeyInventory(GameController, GameData))
    GameController.add_keyboard_manager(InUseInventory.ID, InUseInventory(GameController, GameData))
    GameController.add_keyboard_manager(InUseKeyInventory.ID, InUseKeyInventory(GameController, GameData))
    GameController.add_keyboard_manager(InToDoList.ID, InToDoList(GameController, GameData))

    GameController.add_keyboard_manager(InProfile.ID, InProfile(GameController, GameData))

    # sets the initial Keyboard Manager to be the InGame Manager
    GameController.set_keyboard_manager(InGame.ID)

def load_menus(GameController, GameData):
    # load menus - stores all the information for the various menus in the game in GameData
    # The start menu which pops up when the player presses left control
    GameData.add_overlay("start_menu", Overlay(GameController, GameData, "start_menu", 700, 200, Spritesheet("assets/menu_images/start_menu.png", 150, 400)))
    GameData.add_menu("start_menu", StartMenu(GameController, GameData, "start_menu", ["Chore List", "Map", "Bag", "Outfits", "Profile", "Save", "Options", "Vibes"], True, "start_menu"))

    GameData.add_overlay("yes_no_menu", Overlay(GameController, GameData, "yes_no_menu", 600, 200, Spritesheet("assets/menu_images/yes_no_menu.png", 90, 76)))
    GameData.add_menu("yes_no_menu", Menu(GameController, GameData, "yes_no_menu", ["Yes", "No"], True, "yes_no_menu"))

    # the menu which pops up when the player has selected bag from the start menu
    GameData.add_overlay("inventory_menu", Overlay(GameController, GameData, "inventory_menu", 700, 200, Spritesheet("assets/menu_images/inventory_menu.png", 200, 400)))
    GameData.add_menu("inventory_menu", InventoryMenu(GameController, GameData, "inventory_menu", GameController.inventory.current_items, True, "inventory_menu"))

    # the menu which pops up when the player has selected bag from the start menu and scrolls left or right
    GameData.add_overlay("key_inventory_menu", Overlay(GameController, GameData, "key_inventory_menu", 700, 200, Spritesheet("assets/menu_images/inventory_menu.png", 200, 400)))
    GameData.add_menu("key_inventory_menu", KeyInventoryMenu(GameController, GameData, "key_inventory_menu", GameController.inventory.current_key_items, True, "key_inventory_menu"))

    # the menu that pops up when a player selects an item from the inventory or key inventory
    GameData.add_overlay("use_menu", Overlay(GameController, GameData, "use_menu", 590, 200, Spritesheet("assets/menu_images/use_menu.png", 100, 100)))
    GameData.add_menu("use_menu", StartMenu(GameController, GameData, "use_menu", ["Use", "Toss"], True, "use_menu"))

    # Add non-menu overlays
    # the overlay that presents the profile card
    GameData.add_overlay("ID_card", ProfileCard(GameController, GameData, "ID_Card", 350, 300, Spritesheet("assets/misc_sprites/ID.png", 300, 200)))

    GameData.add_overlay("To_do_list", ToDoList(GameController, GameData, "To_do_list", 350, 200, Spritesheet("assets/misc_sprites/to_do_list.png", 300, 400)))

    # the overlay that is always present at the top of the screen containing current statur information
    #TODO: Make this actually a thing
    GameData.add_overlay("top_bar", Overlay(GameController, GameData, "top_bar", 100, 100, Spritesheet("assets/menu_images/top_bar.png", 700, 100)))

    #TODO: Fix this
    GameData.add_overlay("text_box",
                   TextBox(GameController, GameData, "text_box", 250, 550, Spritesheet("assets/menu_images/text_box.png", 500, 150)))

    # the menu that pops up when you talk to an NPC and have to decide how to interact with them
    GameData.add_menu("character_interact_menu",
                TalkingMenu(GameController, GameData, "character_interact_menu", ["Talk", "Give Gift"], True, "text_box"))

def load_items(GameController, GameData):
    # adds all the items that exist in the game to the storage in GameData
    GameData.add_item("Cheese", Item("Cheese", GameData, GameController))
    GameData.add_item("Mask", Item("Mask", GameData, GameController))
    GameData.add_item("Stick", Item("Stick", GameData, GameController))
    GameData.add_item("Fork", Item("Fork", GameData, GameController))
    GameData.add_item("Pen", Item("Pen", GameData, GameController))
    GameData.add_item("Cup", Item("Cup", GameData, GameController))
    GameData.add_item("Bottle", Item("Bottle", GameData, GameController))
    GameData.add_item("Coin", Item("Coin", GameData, GameController))
    GameData.add_item("Paper", Item("Paper", GameData, GameController))

    # adds the number of items to your inventory - temporary - for testing purposes
    GameController.inventory.get_item("Cheese", 9)
    GameController.inventory.get_item("Mask", 102)
    GameController.inventory.get_item("Stick", 91)
    GameController.inventory.get_item("Fork", 91)
    GameController.inventory.get_item("Pen", 91)
    GameController.inventory.get_item("Cup", 91)
    GameController.inventory.get_item("Bottle", 91)
    GameController.inventory.get_item("Coin", 91)
    GameController.inventory.get_item("Paper", 91)

def load_key_items(GameController, GameData):
    # adds all the key items that exist in the game to the storage in GameData
    GameData.add_key_item("Hammer", Item("Hammer", GameData, GameController))
    GameData.add_key_item("Shovel", Item("Shovel", GameData, GameController))
    GameData.add_key_item("Clippers", Item("Clippers", GameData, GameController))

    # adds the key item to your key item inventory - for testing purposes
    GameController.inventory.get_key_item("Hammer")
    GameController.inventory.get_key_item("Shovel")
    GameController.inventory.get_key_item("Clippers")


"""
initiate the rooms following this process:
1. add the room to the storage in GameData using: GameData.add_room
2. add the plots that make up the room to the list in the room class using: GameData.room_list[room name].add_room_plot
3. activate the plot - this means that it appears in the current plot list of the room and will be 
    displayed using: GameData.room_list[room name].activate_plot
4. generate the grid of the room which is stored in an dictionary in the room 
    class using: GameData.room_list[room name].generate_room_grid()
5. add any doors in the room to the list in the room class using: GameData.room_list[room name].add_room_door
6. add any characters in the room to the storage in GameData using: GameData.add_character 
7. add any props and decorations in the room to the storage in GameData using:  GameData.add_prop and GameData.add_decoration
8. attach the characters and doors to the room using add_room_character and add_room_prop to add their names to a list 
    in the room class using: GameData.room_list[room name].add_room_character and GameData.room_list["room1"].add_room_prop 
9. add the position manager that's in charge of managing the positions of all the features in the room to the storage 
    in GameData using:  GameData.add_positioner
10. fill out the tile grid with all the "obstacles" (places that can't be walked) that are in the room based on a csv 
    file that matches the room using: GameData.positioner[room name].fill_obstacles
11. fill out the tile grid with all the features that have been placed in the room thus 
    far using: GameData.positioner[room name].fill_tiles
11. fill out the tile grid with all the doors that were setup earlier in the 
    list using: GameData.positioner[room name].fill_doors
12. activate the animation and action timers for all of the characters that are in the 
    room using: a for loop and GameData.character_list[character].activate_timers()
"""

def init_all_rooms(gc_input, gd_input):
    # room #1
    gd_input.add_room("room1", Room1(gc_input, gd_input))
    gd_input.room_list["room1"].activate_room()

    # room #2
    gd_input.add_room("room2", Room2(gc_input, gd_input))
    gd_input.room_list["room2"].activate_room()

    # room 3
    gd_input.add_room("room3", Room3(gc_input, gd_input))
    gd_input.room_list["room3"].activate_room()

    # add room #4
    gd_input.add_room("room4", Room4(gc_input, gd_input))
    gd_input.room_list["room4"].activate_room()

    # add room Coop
    gd_input.add_room("Coop", Room5(gc_input, gd_input))
    gd_input.room_list["Coop"].activate_room()

    # add room #6
    gd_input.add_room("room6", Room6(gc_input, gd_input))
    gd_input.room_list["room6"].activate_room()

    gd_input.add_room("Ringside", Ringside(gc_input, gd_input))
    gd_input.room_list["Ringside"].activate_room()