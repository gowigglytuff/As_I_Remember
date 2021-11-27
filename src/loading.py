

import pygame
from data import *
from features import *
from mapClasses import *
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
    BT = TileSet("assets/csv_maps/csv_tiles/Big_Tileset.png", 32, 32, 40, 10)
    T = TileSet("assets/csv_maps/csv_tiles/tileset.png", 32, 32, 3, 5)
    # store each tile in a dictionary in GameData that will be accessed by the TileMap function
    gd_input.add_tile_dict(BT.load_tile_images())

    # add the player to the game
    gd_input.add_player("Player", Player(2, 3, gc_input, gd_input))
    gd_input.player["Player"].activate_timer()

    # run functions that initiate all rooms
    init_room_1(gc_input, gd_input, "room1")
    init_room_2(gc_input, gd_input, "room2")
    init_room_3(gc_input, gd_input, "room3")
    init_room_4(gc_input, gd_input, "room4")
    #init_room_5(GameController, GameData, "room5")
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
def init_room_1(gc_input, gd_input, room_name):
    # room #1

    # add the room #1, generate the grid, and add the background and doors
    gd_input.add_room(room_name, Room(room_name, 1, 2, 6, 6, 1, 1, gc_input, gd_input))
    gd_input.room_list[room_name].add_room_plot("room1_1_1", Plot("room1", 1, 1, pygame.image.load("assets/backgrounds/room_1_background.png"), gc_input, gd_input, None))
    gd_input.room_list[room_name].activate_plot("room1_1_1")

    # generate the grid for the room
    #gd_input.room_list[room_name].generate_room_grid()
    gd_input.room_list[room_name].compose_room()



    def add_room_doors(gc_input, gd_input, room_name):
        #add the door to the room
        gd_input.room_list[room_name].add_room_door("room1_door1", Door(room_name, "room2", 2, 2, 1, 15, "room1_door1"))
        gd_input.room_list[room_name].add_room_door("room1_door2", Door(room_name, "room4", 5, 1, 2, 4, "room1_door2"))
        #GameData.room_list[room_name].add_room_door("room1_door3", Door(room_name, "room5", 1, 7, 1, 2, "room1_door3"))

    add_room_doors(gc_input, gd_input, room_name)

    # add the NPC characters to the game
    gd_input.add_character("Shuma", Generic_NPC(2, 4, gc_input, gd_input, Spritesheet("assets/NPC_sprites/Shuma.png", 32, 40), "Shuma", "room1", "Your dad have manure for sale? I'd really love to get my hands on a couple bags of it. It's great for the turnips and the kale! Though I think I might get some nitrogen fixed stuff from the co-op for the lettuce..."))
    gd_input.add_character("Maggie", Generic_NPC(5, 5, gc_input, gd_input, Spritesheet("assets/NPC_sprites/Maggie.png", 32, 40), "Maggie", "room1", "This outfit makes me feel really cool and powerful, so I've decided I'm going to wear it everywhere."))
    gd_input.add_character("Laurie", Generic_NPC(4, 3, gc_input, gd_input, Spritesheet("assets/NPC_sprites/Laurie.png", 32, 40), "Laurie", "room1", "Have you seen my drink anywhere?"))

    #add props to the game
    gd_input.add_prop("trunk", Prop(3, 2, gc_input, gd_input,32, 40, Spritesheet("assets/prop_sprites/trunk.png", 32, 40), "trunk",  1, 1, room_name))
    gd_input.add_prop("lamp", Prop(1, 5, gc_input, gd_input, 32, 40, Spritesheet("assets/prop_sprites/lamp.png", 32, 40), "lamp", 1, 1, room_name))

    # add position manager to it's room and make it tell the tile array what it's filled with
    gd_input.add_positioner(room_name, Position_Manager(room_name, gc_input, gd_input))
    gd_input.positioner[room_name].fill_tiles(room_name)
    gd_input.positioner[room_name].fill_doors(room_name)

    # activate the timers for animation and actions for the NPCs (make this apply to all that are in room)
    for character in gd_input.room_list[room_name].character_list:
        gd_input.character_list[character].activate_timers()

def init_room_2(gc_input, gd_input, room_name):
    # room#2

    # add the room #2, generate the grid, and add the background and doors
    gd_input.add_room(room_name, Room(room_name, 1, 1, 15, 15, 1, 1, gc_input, gd_input, map_style="csv"))
    gd_input.room_list[room_name].add_room_plot("room2_1_1", Plot(room_name, 1, 1,
                                                                TileMap("assets/csv_maps/csv_tiles/lake.csv", gd_input.tiles_img_dict).return_map(),
                                                                gc_input, gd_input, "assets/csv_maps/room2.csv"))
    gd_input.room_list[room_name].activate_plot("room2_1_1")
    gd_input.room_list[room_name].generate_room_grid()

    gd_input.room_list[room_name].add_room_door("room2_door1", Door(room_name, "room1", 1, 14, 2, 3, "room2_door1"))
    gd_input.room_list[room_name].add_room_door("room2_door2", Door(room_name, "room3", 8, 12, 2, 4, "room2_door2"))

    # add characters
    gd_input.add_character("Deb", Generic_NPC(4, 4, gc_input, gd_input, Spritesheet("assets/NPC_sprites/Deb.png", 32, 40), "Deb", "room2",
                                  "Hey Shuma, so nice to see you again!, I should probably be in the studio, but when I'm low on inspiration I like to come out here and walk by the water. "))

    # add features for room 2
    gd_input.add_prop("house", Prop(5, 10, gc_input, gd_input, 160, 128, Spritesheet("assets/prop_sprites/House.png", 160, 128), "house", 5, 3, room_name))
    gd_input.add_prop("tree", Tree(3, 6, gc_input))

    gd_input.add_decoration("Grass", Decoration(0, 0, gc_input, gd_input, 32, 32, Spritesheet("assets/decoration_sprites/grass5.png", 32, 32), "Grass", 1, 1, [[2, 11], [2, 12], [2, 13], [2, 14], [3, 11], [3, 12], [3, 13], [3, 14]], room_name))


    # add position manager to it's room and make it tell the tile array what it's filled with, then populate doors
    gd_input.add_positioner(room_name, Position_Manager(room_name, gc_input, gd_input))
    gd_input.positioner[room_name].fill_obstacles("assets/csv_maps/room2.csv", room_name)
    #TODO: Fill out terrain for all other levels
    gd_input.positioner[room_name].fill_terrain("assets/csv_maps/room2.csv", room_name)
    gd_input.positioner[room_name].fill_tiles(room_name)
    gd_input.positioner[room_name].fill_doors(room_name)

    for character in gd_input.room_list[room_name].character_list:
        gd_input.character_list[character].activate_timers()

def init_room_3(gc_input, gd_input, room_name):
    gd_input.add_room(room_name, Room(room_name, 1, 2, 3, 3, 1, 1, gc_input, gd_input))
    gd_input.room_list[room_name].generate_room_grid()
    gd_input.room_list[room_name].add_room_plot("room3_1_1", Plot(room_name, 1, 1, pygame.image.load("assets/backgrounds/room_3_background.png"), gc_input, gd_input, None))
    gd_input.room_list[room_name].add_room_door("room3_door1", Door(room_name, "room2", 2, 5, 8, 13, "room3_door1"))

    gd_input.room_list[room_name].activate_plot("room3_1_1")

    gd_input.add_character("Pixie", Generic_NPC(2, 2, gc_input, gd_input, Spritesheet("assets/NPC_sprites/sprite_sheet.png", 32, 40), "Pixie", "room3", "Hi!"))
    gd_input.add_character("Pixie_b", Generic_NPC(3, 4, gc_input, gd_input, Spritesheet("assets/NPC_sprites/sprite2_sheet.png", 32, 40), "Pixie_b", "room3", "Hi!"))
    gd_input.add_character("Ian", Generic_NPC(3, 2, gc_input, gd_input, Spritesheet("assets/NPC_sprites/Ian.png", 32, 40), "Ian", "room3", "Damnit, the cows got out again... If you see Kleyo can you ask her to give me a call? I should be back at the house by five."))

    gd_input.add_positioner(room_name, Position_Manager(room_name, gc_input, gd_input))
    gd_input.positioner[room_name].fill_tiles(room_name)
    gd_input.positioner[room_name].fill_doors(room_name)

    for character in gd_input.room_list[room_name].character_list:
        gd_input.character_list[character].activate_timers()

def init_room_4(gc_input, gd_input, room_name):

    # add room #4
    gd_input.add_room(room_name, Room(room_name, 1, 1, 100, 50, 2, 1, gc_input, gd_input, map_style="csv"))

    big_map = TileMap("assets/csv_maps/csv_tiles/big_map2.0.csv", gd_input.tiles_img_dict)
    gd_input.room_list[room_name].add_room_plot("room4_1_1", Plot(room_name, 1, 1, big_map.return_map(), gc_input, gd_input, "assets/csv_maps/big_map.csv"))
    gd_input.room_list[room_name].add_room_plot("room4_1_2", Plot(room_name, 2, 1, big_map.return_map(), gc_input, gd_input, "assets/csv_maps/big_map.csv"))
    gd_input.room_list[room_name].activate_plot("room4_1_1")
    gd_input.room_list[room_name].activate_plot("room4_1_2")

    gd_input.room_list[room_name].generate_room_grid()
    gd_input.room_list[room_name].add_room_door("room4_door1", Door(room_name, "room1", 2, 3, 5, 2, "room4_door1"))

    for name in range(50):
        rand_x = randrange(1, 100)
        rand_y = randrange(1, 50)
        gd_input.add_character(("Sheep" + str(name)), Generic_NPC(rand_x, rand_y, gc_input, gd_input, Spritesheet("assets/NPC_sprites/sheep.png", 32, 40), ("Sheep" + str(name)), "room4", "Baaaahhhh"))
        gd_input.character_list["Sheep" + str(name)].activate_timers()

    gd_input.add_positioner(room_name, Position_Manager(room_name, gc_input, gd_input))

    # TODO: figure out how to use csv for rooms with multiple maps in them (Perhaps attach them to BG instead of Room)
    gd_input.positioner[room_name].fill_obstacles("assets/csv_maps/big_map.csv", room_name)
    gd_input.positioner[room_name].fill_tiles(room_name)
    gd_input.positioner[room_name].fill_doors(room_name)

def init_room_5(gc_input, gd_input, room_name):
    #TODO: Fix this room
   # add the room #5, generate the grid, and add the background and doors
    gd_input.add_room(room_name, Room(room_name, 1, 1, 20, 10, 1, 1, gc_input, gd_input, map_style="csv"))
    gd_input.room_list[room_name].add_room_plot("room5_1_1", Plot(room_name, 1, 1,
                                                                TileMap("assets/csv_maps/room5.csv", "grass", "water").return_map(),
                                                                gc_input, gd_input, "assets/csv_maps/room5.csv"))

    gd_input.add_prop("house2", Prop(13, 3, gc_input, gd_input, 192, 128, Spritesheet("assets/prop_sprites/House.png", 192, 128), "house2", 6, 3, room_name))
    gd_input.room_list[room_name].add_room_prop("house2")

    gd_input.room_list[room_name].activate_plot("room5_1_1")

    gd_input.room_list[room_name].generate_room_grid()

    gd_input.add_positioner(room_name, Position_Manager(room_name, gc_input, gd_input))

    gd_input.room_list[room_name].add_room_door("room5_door1", Door(room_name, "room1", 1, 1, 1, 6, "room5_door1"))

    gd_input.positioner[room_name].fill_obstacles("assets/csv_maps/room5.csv", room_name)
    gd_input.positioner[room_name].fill_tiles(room_name)
    gd_input.positioner[room_name].fill_doors(room_name)

def init_room_Coop(gc_input, gd_input):
    # add room Coop
    gd_input.add_room("Coop", Room("Coop", 1, 1, 36, 60, 1, 1, gc_input, gd_input, map_style="csv"))

    coop_map = TileMap("assets/csv_maps/Co-op_area.csv", gd_input.tiles_img_dict)
    gd_input.room_list["Coop"].add_room_plot("Coop_1_1",
                                             Plot("Coop", 1, 1, coop_map.return_map(), gc_input, gd_input,
                                                   "assets/csv_maps/Co-op_area.csv"))

    gd_input.room_list["Coop"].activate_plot("Coop_1_1")


    gd_input.room_list["Coop"].generate_room_grid()
    #GameData.room_list["Coop"].add_room_door("Coop_door1", Door("Coop", "room1", 2, 3, 5, 2, "Coop_door1"))

    gd_input.add_positioner("Coop", Position_Manager("Coop", gc_input, gd_input))

    gd_input.add_prop("Coop_Building", Prop(2, 2, gc_input, gd_input, 832, 1632, Spritesheet("assets/prop_sprites/Coop_Building.png", 832, 1632), "Coop_Building", 6, 3))
    gd_input.room_list["Coop"].add_room_prop("Coop_Building")

    # TODO: figure out how to use csv for rooms with multiple maps in them (Perhaps attach them to BG instead of Room)
    gd_input.positioner["Coop"].fill_obstacles("assets/csv_maps/Coop_allowance.csv", "Coop")
    gd_input.positioner["Coop"].fill_tiles("Coop")
    gd_input.positioner["Coop"].fill_doors("Coop")

