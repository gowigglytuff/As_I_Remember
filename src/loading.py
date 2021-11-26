

import pygame
from data import *
from features import *
from mapClasses import *
from TileMap import *
from keyboards import *
from random import randrange
from inventory import *

def init_game(GameData, GameController):
    '''
    :type GameController: GameController
    :type GameData: GameData
    :return:
    '''
    # initialize pygame
    pygame.init()
    pygame.display.set_caption('As I Remember')
    pygame.key.set_repeat()

    # Load all the differnt keyboard modes that the you encounter when in different things like the menus and stuff
    load_keyboard_managers(GameController, GameData)

    # load all the different menus
    load_menus(GameController, GameData)

    # load the full list of items that are available in the game
    load_items(GameController, GameData)

    # load the full list of key items that are available in the game
    load_key_items(GameController, GameData)

    # Load the Tileset
    BT = TileSet("assets/csv_maps/csv_tiles/Big_Tileset.png", 32, 32, 40, 10)
    T = TileSet("assets/csv_maps/csv_tiles/tileset.png", 32, 32, 3, 5)
    # store each tile in a dictionary in GameData that will be accessed by the TileMap function
    GameData.add_tile_dict(BT.load_tile_images())

    # add the player to the game
    GameData.add_player("Player", Player(2, 3, 2, 3, 32, 40, Spritesheet("assets/NPC_sprites/Shuma.png", 32, 40), "Bug", GameController, GameData))
    GameData.player["Player"].activate_timer()

    # run functions that initiate all rooms
    init_room_1(GameController, GameData)
    init_room_2(GameController, GameData)
    init_room_3(GameController, GameData)
    init_room_4(GameController, GameData)
    # init_room_5(GameController, GameData)
    #init_room_Coop(GameController, GameData)

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
def init_room_1(GameController, GameData):
    # room #1

    # add the room #1, generate the grid, and add the background and doors
    GameData.add_room("room1", Room("room1", 1, 2, 6, 6, 1, 1, GameController, GameData))
    GameData.room_list["room1"].add_room_plot("room1_1_1", Plot("room4", 1, 1, pygame.image.load("assets/backgrounds/room_1_background.png"), GameController, GameData, None))
    GameData.room_list["room1"].activate_plot("room1_1_1")

    # generate the grid for the room
    GameData.room_list["room1"].generate_room_grid()

    #add the door to the room
    GameData.room_list["room1"].add_room_door("room1_door1", Door("room1", "room2", 2, 2, 1, 15, "room1_door1"))
    GameData.room_list["room1"].add_room_door("room1_door2", Door("room1", "room4", 5, 1, 2, 4, "room1_door2"))
    #GameData.room_list["room1"].add_room_door("room1_door3", Door("room1", "room5", 1, 7, 1, 2, "room1_door3"))

    # add the NPC characters to the game
    GameData.add_character("Shuma", Pixie(2, 4, 2, 4, 32, 40, Spritesheet("assets/NPC_sprites/Shuma.png", 32, 40), "Shuma", GameController, GameData, "Your dad have manure for sale? I'd really love to get my hands on a couple bags of it. It's great for the turnips and the kale! Though I think I might get some nitrogen fixed stuff from the co-op for the lettuce..."))
    GameData.add_character("Maggie", Pixie(5, 5, 5, 5, 32, 40, Spritesheet("assets/NPC_sprites/Maggie.png", 32, 40), "Maggie", GameController, GameData, "This outfit makes me feel really cool and powerful, so I've decided I'm going to wear it everywhere."))
    GameData.add_character("Laurie", Pixie(4, 3, 4, 3, 32, 40, Spritesheet("assets/NPC_sprites/Laurie.png", 32, 40), "Laurie", GameController, GameData, "Have you seen my drink anywhere?"))

    #add props to the game
    GameData.add_prop("trunk", Prop(3, 2, 3, 2, 32, 40, Spritesheet("assets/prop_sprites/trunk.png", 32, 40), "trunk", GameController, GameData, 1, 1, 10))
    GameData.add_prop("lamp", Prop(1, 5, 1, 5, 32, 40, Spritesheet("assets/prop_sprites/lamp.png", 32, 40), "lamp", GameController, GameData, 1, 1))

    #add all the features to the current room
    GameData.room_list["room1"].add_room_character("Shuma")
    GameData.room_list["room1"].add_room_character("Maggie")
    GameData.room_list["room1"].add_room_character("Laurie")
    GameData.room_list["room1"].add_room_prop("trunk")
    GameData.room_list["room1"].add_room_prop("lamp")

    # add position manager to it's room and make it tell the tile array what it's filled with
    GameData.add_positioner("room1", Position_Manager("room1", GameController, GameData))
    GameData.positioner["room1"].fill_tiles("room1")
    GameData.positioner["room1"].fill_doors("room1")

    # activate the timers for animation and actions for the NPCs (make this apply to all that are in room)
    for character in GameData.room_list["room1"].character_list:
        GameData.character_list[character].activate_timers()

def init_room_2(GameController, GameData):
    # room#2

    # add the room #2, generate the grid, and add the background and doors
    GameData.add_room("room2", Room("room2", 1, 1, 15, 15, 1, 1, GameController, GameData, map_style="csv"))
    GameData.room_list["room2"].add_room_plot("room2_1_1", Plot("room2", 1, 1,
                                                          TileMap("assets/csv_maps/csv_tiles/lake.csv", GameData.tiles_img_dict).return_map(),
                                                          GameController, GameData, "assets/csv_maps/room2.csv"))
    GameData.room_list["room2"].activate_plot("room2_1_1")
    GameData.room_list["room2"].generate_room_grid()

    GameData.room_list["room2"].add_room_door("room2_door1", Door("room2", "room1", 1, 14, 2, 3, "room2_door1"))
    GameData.room_list["room2"].add_room_door("room2_door2", Door("room2", "room3", 8, 12, 2, 4, "room2_door2"))

    # add characters
    GameData.add_character("Deb", Pixie(4, 4, 4, 4, 32, 40, Spritesheet("assets/NPC_sprites/Deb.png", 32, 40), "Deb", GameController, GameData,
                                  "Hey Shuma, so nice to see you again!, I should probably be in the studio, but when I'm low on inspiration I like to come out here and walk by the water. "))

    # add features for room 2
    GameData.add_prop("house", Prop(5, 10, 5, 10, 160, 128, Spritesheet("assets/prop_sprites/House.png", 160, 128), "house", GameController, GameData, 5, 3, offset_y=32))
    GameData.add_prop("tree", Tree(3, 6, GameController))
    GameData.add_prop("tree2", Prop(7, 7, 7, 7, 64, 96, Spritesheet("assets/prop_sprites/tree.png", 64, 96), "tree2", GameController, GameData, 2, 1, offset_y=64))
    GameData.add_prop("tree3", Prop(10, 7, 10, 7, 64, 96, Spritesheet("assets/prop_sprites/tree.png", 64, 96), "tree3", GameController, GameData, 2, 1, offset_y=64))
    GameData.add_prop("tree4", Prop(5, 4, 5, 4, 64, 96, Spritesheet("assets/prop_sprites/tree.png", 64, 96), "tree4",
                                   GameController, GameData, 2, 1, offset_y=64))
    GameData.add_prop("tree5", Prop(8, 4, 8, 4, 64, 96, Spritesheet("assets/prop_sprites/tree.png", 64, 96), "tree5",
                                    GameController, GameData, 2, 1, offset_y=64))
    GameData.add_prop("tree6", Prop(11, 4, 11, 4, 64, 96, Spritesheet("assets/prop_sprites/tree.png", 64, 96), "tree6",
                                    GameController, GameData, 2, 1, offset_y=64))

    GameData.add_decoration("Grass", Decoration(0, 0, 2, 13, 32, 32, Spritesheet("assets/decoration_sprites/grass5.png", 32, 32), "Grass", GameController, GameData, 1, 1, [[2, 11], [2, 12], [2, 13], [2, 14],[3, 11], [3, 12], [3, 13], [3, 14]]))

    # attach all features to room
    GameData.room_list["room2"].add_room_prop("house")
    GameData.room_list["room2"].add_room_prop("tree")
    GameData.room_list["room2"].add_room_prop("tree2")
    GameData.room_list["room2"].add_room_prop("tree3")
    GameData.room_list["room2"].add_room_prop("tree4")
    GameData.room_list["room2"].add_room_prop("tree5")
    GameData.room_list["room2"].add_room_prop("tree6")
    GameData.room_list["room2"].add_room_character("Deb")

    GameData.room_list["room2"].add_room_decoration("Grass")

    # add position manager to it's room and make it tell the tile array what it's filled with, then populate doors
    GameData.add_positioner("room2", Position_Manager("room2", GameController, GameData))
    GameData.positioner["room2"].fill_obstacles("assets/csv_maps/room2.csv", "room2")
    #TODO: Fill out terrain for all other levels
    GameData.positioner["room2"].fill_terrain("assets/csv_maps/room2.csv", "room2")
    GameData.positioner["room2"].fill_tiles("room2")
    GameData.positioner["room2"].fill_doors("room2")

    for character in GameData.room_list["room2"].character_list:
        GameData.character_list[character].activate_timers()

def init_room_3(GameController, GameData):
    GameData.add_room("room3", Room("room3", 1, 2, 3, 3, 1, 1, GameController, GameData))
    GameData.room_list["room3"].generate_room_grid()
    GameData.room_list["room3"].add_room_plot("room3_1_1", Plot("room3", 1, 1, pygame.image.load("assets/backgrounds/room_3_background.png"), GameController, GameData, None))
    GameData.room_list["room3"].add_room_door("room3_door1", Door("room3", "room2", 2, 5, 8, 13, "room3_door1"))

    GameData.room_list["room3"].activate_plot("room3_1_1")

    GameData.add_character("Pixie", Pixie(2, 2, 2, 2, 32, 40, Spritesheet("assets/NPC_sprites/sprite_sheet.png", 32, 40), "Pixie", GameController, GameData, "Hi!"))

    GameData.add_character("Pixie_b", Pixie(3, 4, 3, 4, 32, 40, Spritesheet("assets/NPC_sprites/sprite2_sheet.png", 32, 40), "Pixie_b", GameController, GameData, "Hi!"))

    GameData.add_character("Ian", Pixie(3, 2, 3, 2, 32, 40, Spritesheet("assets/NPC_sprites/Ian.png", 32, 40), "Ian", GameController, GameData, "Damnit, the cows got out again... If you see Kleyo can you ask her to give me a call? I should be back at the house by five."))

    GameData.room_list["room3"].add_room_character("Pixie")
    GameData.room_list["room3"].add_room_character("Pixie_b")
    GameData.room_list["room3"].add_room_character("Ian")


    GameData.add_positioner("room3", Position_Manager("room3", GameController, GameData))
    GameData.positioner["room3"].fill_tiles("room3")
    GameData.positioner["room3"].fill_doors("room3")

    for character in GameData.room_list["room3"].character_list:
        GameData.character_list[character].activate_timers()

def init_room_4(GameController, GameData):

    # add room #4
    GameData.add_room("room4", Room("room4", 1, 1, 100, 50, 2, 1, GameController, GameData, map_style="csv"))

    big_map = TileMap("assets/csv_maps/csv_tiles/big_map2.0.csv", GameData.tiles_img_dict)
    GameData.room_list["room4"].add_room_plot("room4_1_1", Plot("room4", 1, 1, big_map.return_map(), GameController, GameData, "assets/csv_maps/big_map.csv"))
    GameData.room_list["room4"].add_room_plot("room4_1_2", Plot("room4", 2, 1, big_map.return_map(), GameController, GameData, "assets/csv_maps/big_map.csv"))
    GameData.room_list["room4"].activate_plot("room4_1_1")
    GameData.room_list["room4"].activate_plot("room4_1_2")

    GameData.room_list["room4"].generate_room_grid()
    GameData.room_list["room4"].add_room_door("room4_door1", Door("room4", "room1", 2, 3, 5, 2, "room4_door1"))

    for name in range(50):
        rand_x = randrange(1, 100)
        rand_y = randrange(1, 50)
        GameData.add_character(("Sheep" + str(name)), Pixie(rand_x, rand_y, rand_x, rand_y, 32, 40, Spritesheet("assets/NPC_sprites/sheep.png", 32, 40), ("Sheep" + str(name)), GameController, GameData, "Baaaahhhh"))
        GameData.room_list["room4"].add_room_character(("Sheep" + str(name)))
        GameData.character_list["Sheep" + str(name)].activate_timers()

    GameData.add_positioner("room4", Position_Manager("room4", GameController, GameData))

    # TODO: figure out how to use csv for rooms with multiple maps in them (Perhaps attach them to BG instead of Room)
    GameData.positioner["room4"].fill_obstacles("assets/csv_maps/big_map.csv", "room4")
    GameData.positioner["room4"].fill_tiles("room4")
    GameData.positioner["room4"].fill_doors("room4")

def init_room_5(GameController, GameData):
    #TODO: Fix this room
   # add the room #5, generate the grid, and add the background and doors
    GameData.add_room("room5", Room("room5", 1, 1, 20, 10, 1, 1, GameController, GameData, map_style="csv"))
    GameData.room_list["room5"].add_room_plot("room5_1_1", Plot("room5", 1, 1,
                                                          TileMap("assets/csv_maps/room5.csv", "grass", "water").return_map(),
                                                          GameController, GameData, "assets/csv_maps/room5.csv"))

    GameData.add_prop("house2", Prop(13, 3, 13, 3, 192, 128, Spritesheet("assets/prop_sprites/House.png", 192, 128), "house2", GameController, GameData, 6, 3, offset_y=32))
    GameData.room_list["room5"].add_room_prop("house2")

    GameData.room_list["room5"].activate_plot("room5_1_1")

    GameData.room_list["room5"].generate_room_grid()

    GameData.add_positioner("room5", Position_Manager("room5", GameController, GameData))

    GameData.room_list["room5"].add_room_door("room5_door1", Door("room5", "room1", 1, 1, 1, 6, "room5_door1"))

    GameData.positioner["room5"].fill_obstacles("assets/csv_maps/room5.csv", "room5")
    GameData.positioner["room5"].fill_tiles("room5")
    GameData.positioner["room5"].fill_doors("room5")

def init_room_Coop(GameController, GameData):
    # add room Coop
    GameData.add_room("Coop", Room("Coop", 1, 1, 36, 60, 1, 1, GameController, GameData, map_style="csv"))

    coop_map = TileMap("assets/csv_maps/Co-op_area.csv", GameData.tiles_img_dict)
    GameData.room_list["Coop"].add_room_plot("Coop_1_1",
                                              Plot("Coop", 1, 1, coop_map.return_map(), GameController, GameData,
                                                   "assets/csv_maps/Co-op_area.csv"))

    GameData.room_list["Coop"].activate_plot("Coop_1_1")


    GameData.room_list["Coop"].generate_room_grid()
    #GameData.room_list["Coop"].add_room_door("Coop_door1", Door("Coop", "room1", 2, 3, 5, 2, "Coop_door1"))

    GameData.add_positioner("Coop", Position_Manager("Coop", GameController, GameData))

    GameData.add_prop("Coop_Building",
                      Prop(2, 2, 2, 2, 832, 1632, Spritesheet("assets/prop_sprites/Coop_Building.png", 832, 1632), "Coop_Building",
                           GameController, GameData, 6, 3, offset_y=32))
    GameData.room_list["Coop"].add_room_prop("Coop_Building")

    # TODO: figure out how to use csv for rooms with multiple maps in them (Perhaps attach them to BG instead of Room)
    GameData.positioner["Coop"].fill_obstacles("assets/csv_maps/Coop_allowance.csv", "Coop")
    GameData.positioner["Coop"].fill_tiles("Coop")
    GameData.positioner["Coop"].fill_doors("Coop")

