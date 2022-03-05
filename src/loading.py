

import pygame
from data import *
from features import *
from main import gl
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
    FT = TileSet("assets/room_maps/csv_tiles/Full_Tileset_Adjusted.png", 32, 32,40, 40)
    BT = TileSet("assets/room_maps/csv_tiles/Big_Tileset.png", 32, 32, 40, 10)
    T = TileSet("assets/room_maps/csv_tiles/tileset.png", 32, 32, 3, 5)
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
    GameController.add_keyboard_manager(InRegularMenu.ID, InRegularMenu(GameController, GameData))

    # sets the initial Keyboard Manager to be the InGame Manager
    GameController.set_keyboard_manager(InGame.ID)

def load_menus(GameController, GameData):

    #TODO: Fix this
    GameData.add_overlay("text_box", TextBox(GameController, GameData, "text_box", 250, 550, Spritesheet("assets/menu_images/text_box.png", 500, 150)))

    # load menus - stores all the information for the various menus in the game in GameData
    # The start menu which pops up when the player presses left control
    GameData.add_overlay("start_menu", Overlay(GameController, GameData, "start_menu", 700, 200, Spritesheet("assets/menu_images/start_menu.png", 150, 400)))
    GameData.add_menu("start_menu", StartMenu(GameController, GameData, "start_menu", ["Chore List", "Map", "Bag", "Outfits", "Profile", "Save", "Options", "Vibes"], True, "start_menu"))

    # the menu which pops up when the player has selected bag from the start menu
    GameData.add_overlay("inventory_menu", Overlay(GameController, GameData, "inventory_menu", 700, 200, Spritesheet("assets/menu_images/inventory_menu.png", 200, 400)))
    GameData.add_menu("inventory_menu", InventoryMenu(GameController, GameData, "inventory_menu", GameController.inventory.current_items, True, "inventory_menu"))
    GameData.add_menu("inventory_select_menu", InventorySelectMenu(GameController, GameData, "inventory_select_menu", GameController.inventory.current_items, True, "inventory_menu"))

    # the menu which pops up when the player has selected bag from the start menu and scrolls left or right
    GameData.add_overlay("key_inventory_menu", Overlay(GameController, GameData, "key_inventory_menu", 700, 200, Spritesheet("assets/menu_images/inventory_menu.png", 200, 400)))
    GameData.add_menu("key_inventory_menu", KeyInventoryMenu(GameController, GameData, "key_inventory_menu", GameController.inventory.current_key_items, True, "key_inventory_menu"))

    # the menu that pops up when a player selects an item from the inventory or key inventory
    GameData.add_overlay("use_menu", Overlay(GameController, GameData, "use_menu", 590, 200, Spritesheet("assets/menu_images/use_menu.png", 100, 100)))
    GameData.add_menu("use_menu", UseMenu(GameController, GameData, "use_menu", ["Use", "Toss"], True, "use_menu"))

    GameData.add_overlay("yes_no_menu", Overlay(GameController, GameData, "yes_no_menu", 490, 200, Spritesheet("assets/menu_images/yes_no_menu.png", 90, 76)))
    GameData.add_menu("yes_no_menu", YesNoMenu(GameController, GameData, "yes_no_menu", ["Yes", "No"], True, "yes_no_menu"))

    # the overlay that presents the profile card
    GameData.add_overlay("profile_menu_overlay", Overlay(GameController, GameData, "profile_menu_overlay", 350, 300, Spritesheet("assets/misc_sprites/ID.png", 300, 200)))
    GameData.add_menu("profile_menu", ProfileMenu(GameController, GameData, "profile_menu", [], True, "profile_menu_overlay"))

    GameData.add_overlay("To_do_list", Overlay(GameController, GameData, "To_do_list", 350, 200, Spritesheet("assets/misc_sprites/to_do_list.png", 300, 400)))
    GameData.add_menu("to_do_list_menu", ProfileMenu(GameController, GameData, "to_do_list_menu", ["say hi to your mom", "kiss your cat", "eat a pear", "say hi to your mom", "kiss your cat", "eat a pear", "say hi to your mom", "kiss your cat", "eat a pear", "say hi to your mom", "kiss your cat", "eat a pear"], True, "To_do_list"))

    # the menu that pops up when you talk to an NPC and have to decide how to interact with them
    GameData.add_menu("conversation_options_menu", ConversationOptionsMenu(GameController, GameData, "conversation_options_menu", ["Talk", "Give Gift"], True, "text_box"))
    GameData.add_menu("in_conversation_menu", InConversationMenu(GameController, GameData, "in_conversation_menu", [], True, "text_box"))

    # the menu which pops up when you're shopping
    GameData.add_overlay("buying_menu", Overlay(GameController, GameData, "buying_menu", 700, 200, Spritesheet("assets/menu_images/inventory_menu.png", 200, 400)))
    GameData.add_menu("buying_menu", BuyingMenu(GameController, GameData, "buying_menu", [], True, "buying_menu"))

    # the menu that pops up when you talk to an NPC and have to decide how to interact with them
    GameData.add_menu("shopkeeper_interact_menu", ShopKeeperInteractMenu(GameController, GameData, "shopkeeper_interact_menu", ["Buy", "Sell"], True, "text_box"))

    GameData.add_menu("stats_menu", StaticMenu(GameController, GameData))

    GameData.add_menu("game_action_dialogue_menu", GameActionDialogue(GameController, GameData))

    # the overlay that is always present at the top of the screen containing current statur information
    #TODO: Make this actually a thing
    GameData.add_overlay("top_bar", Overlay(GameController, GameData, "top_bar", 100, 100, Spritesheet("assets/menu_images/top_bar.png", 700, 100)))




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
    GameData.add_item("Item1", Item("Item1", GameData, GameController))
    GameData.add_item("Item2", Item("Item2", GameData, GameController))
    GameData.add_item("Item3", Item("Item3", GameData, GameController))
    GameData.add_item("Item4", Item("Item4", GameData, GameController))
    GameData.add_item("Item5", Item("Item5", GameData, GameController))
    GameData.add_item("Item6", Item("Item6", GameData, GameController))
    GameData.add_item("Item7", Item("Item7", GameData, GameController))
    GameData.add_item("TimeSeed", Item("TimeSeed", GameData, GameController))
    GameData.add_item("Book 1", Item("Book 1", GameData, GameController))
    GameData.add_item("Book 2", Item("Book 2", GameData, GameController))
    GameData.add_item("Book 3", Item("Book 3", GameData, GameController))


    # adds the number of items to your inventory - temporary - for testing purposes
    GameController.inventory.get_item("Cheese", 2)
    GameController.inventory.get_item("Mask", 102)
    GameController.inventory.get_item("Stick", 91)
    GameController.inventory.get_item("Fork", 91)
    GameController.inventory.get_item("Pen", 91)
    GameController.inventory.get_item("Cup", 91)
    GameController.inventory.get_item("Bottle", 91)
    GameController.inventory.get_item("Coin", 91)
    GameController.inventory.get_item("Paper", 91)
    GameController.inventory.get_item("Item1", 2)
    GameController.inventory.get_item("Item2", 1)
    GameController.inventory.get_item("Item3", 1)
    GameController.inventory.get_item("Item4", 1)
    GameController.inventory.get_item("Item5", 1)
    GameController.inventory.get_item("Item6", 1)
    GameController.inventory.get_item("Item7", 1)

    #GameController.inventory.get_item("Item6", 1)

def load_key_items(GameController, GameData):
    # adds all the key items that exist in the game to the storage in GameData
    GameData.add_key_item("Hammer", KeyItem("Hammer", GameData, GameController))
    GameData.add_key_item("Shovel", KeyItem("Shovel", GameData, GameController))
    GameData.add_key_item("Clippers", KeyItem("Clippers", GameData, GameController))
    GameData.add_key_item("Gameboy", KeyItem("Gameboy", GameData, GameController))
    GameData.add_key_item("Radio", KeyItem("Radio", GameData, GameController))
    GameData.add_key_item("Net", KeyItem("Net", GameData, GameController))
    GameData.add_key_item("Time Seed", KeyItem("Time Seed", GameData, GameController))

    # adds the key item to your key item inventory - for testing purposes
    GameController.inventory.get_key_item("Hammer")
    GameController.inventory.get_key_item("Shovel")
    GameController.inventory.get_key_item("Clippers")
    GameController.inventory.get_key_item("Gameboy")
    GameController.inventory.get_key_item("Radio")
    GameController.inventory.get_key_item("Net")
    GameController.inventory.get_key_item("Time Seed")


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

    gd_input.add_room("computer_centre", ComputerCentreRoom(gc_input, gd_input))
    gd_input.room_list["computer_centre"].activate_room()

    gd_input.add_room("hornby_creative", HornbyCreativeRoom(gc_input, gd_input))
    gd_input.room_list["hornby_creative"].activate_room()

    gd_input.add_room("to_the_moon", ToTheMoon(gc_input, gd_input))
    gd_input.room_list["to_the_moon"].activate_room()

    gd_input.add_room("hornby_realestate", HornbyRealestate(gc_input, gd_input))
    gd_input.room_list["hornby_realestate"].activate_room()

    gd_input.add_room("island_potters", IslandPotters(gc_input, gd_input))
    gd_input.room_list["island_potters"].activate_room()

    gd_input.add_room("bike_shop", BikeShop(gc_input, gd_input))
    gd_input.room_list["bike_shop"].activate_room()