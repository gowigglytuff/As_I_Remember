from room_page import *
from goals import *
from goals import *
from room_page import *
from key_items import *


def init_game(gd_input, gc_input):
    '''
    :type gc_input: GameController
    :type gd_input: GameData
    :return: None
    '''
    # initialize pygame
    pygame.init()
    pygame.display.set_caption('As I Remember')
    pygame.key.set_repeat()

    # Load all the differnt keyboard modes that the you encounter when in different things like the menus and stuff
    load_keyboard_managers(gc_input, gd_input)

    # load all the different menus
    # load_menus(gc_input, gd_input)
    load_menus2(gc_input, gd_input)

    # load the full list of items that are available in the game
    load_items(gc_input, gd_input)

    # load the full list of key items that are available in the game
    load_key_items(gc_input, gd_input)

    load_goals(gc_input, gd_input)

    # Load the Tileset
    FT = TileSet("assets/room_maps/csv_tiles/Full_Tileset_Adjusted.png", 32, 32,40, 40)
    BT = TileSet("assets/room_maps/csv_tiles/Big_Tileset.png", 32, 32, 40, 10)
    T = TileSet("assets/room_maps/csv_tiles/tileset.png", 32, 32, 3, 5)
    # store each tile in a dictionary in GameData that will be accessed by the TileMap function
    gd_input.add_tile_dict(FT.load_tile_images())

    # add the player to the game
    gd_input.add_player(Player.NAME, Player(0, 0, gc_input, gd_input))
    gd_input.player[Player.NAME].activate_timer()

    # run functions that initiate all rooms
    init_all_rooms(gc_input, gd_input)



def load_keyboard_managers(GameController, GameData):
    # load all keyboard managers
    # TODO: add other possible Keyboard_managers
    GameController.add_keyboard_manager(InGame.ID, InGame(GameController, GameData))
    GameController.add_keyboard_manager(InMenu.ID, InMenu(GameController, GameData))

    # sets the initial Keyboard Manager to be the InGame Manager
    GameController.set_keyboard_manager(InGame.ID)

def load_menus2(GameController, GameData):
    # GameData.add_overlay("text_box_2", TextBox2(GameController, GameData, "text_box_2", 250, 550, Spritesheet("assets/menu_images/text_box.png", 500, 150)))
    GameData.add_menu(GameActionDialogue.NAME, GameActionDialogue(GameController, GameData))
    GameData.add_menu(StatsMenu.NAME, StatsMenu(GameController, GameData))

    GameData.add_menu(StartMenu.NAME, StartMenu(GameController, GameData, ["Chore List", "Map", "Bag", "Outfits", "Profile", "Save", "Options", "Vibes"]))
    GameData.add_menu(InventoryMenu.NAME, InventoryMenu(GameController, GameData, GameController.inventory.current_items))
    GameData.add_menu(ToDoListMenu.NAME, ToDoListMenu(GameController, GameData, ["say hi to your mom", "kiss your cat", "eat a pear", "say hi to your mom", "kiss your cat", "eat a pear", "say hi to your mom", "kiss your cat", "eat a pear", "say hi to your mom", "kiss your cat", "eat a pear"]))

    GameData.add_menu(KeyInventoryMenu.NAME, KeyInventoryMenu(GameController, GameData, GameController.inventory.current_key_items))

    # the menu that pops up when a player selects an item from the inventory or key inventory
    GameData.add_menu(UseMenu.NAME, UseMenu(GameController, GameData, ["Use", "Toss"]))

    GameData.add_menu(YesNoMenu.NAME, YesNoMenu(GameController, GameData, ["Yes", "No"]))

    GameData.add_menu(ProfileMenu.NAME, ProfileMenu(GameController, GameData, []))

    GameData.add_menu(MapMenu.NAME, MapMenu(GameController, GameData, []))

    GameData.add_menu(ConversationOptionsMenu.NAME, ConversationOptionsMenu(GameController, GameData, ["Talk", "Give Gift"]))

    GameData.add_menu(CharacterDialogue.NAME, CharacterDialogue(GameController, GameData, []))

    GameData.add_menu(GiftingMenu.NAME, GiftingMenu(GameController, GameData, GameController.inventory.current_items))

    GameData.add_menu(ShopkeeperDialogue.NAME, ShopkeeperDialogue(GameController, GameData, []))

    # the menu that pops up when you talk to an NPC and have to decide how to interact with them
    GameData.add_menu(ShopKeeperInteractMenu.NAME, ShopKeeperInteractMenu(GameController, GameData, ["Buy", "Sell"]))

    GameData.add_menu(BuyingMenu.NAME, BuyingMenu(GameController, GameData, []))

    GameData.add_menu(SellingMenu.NAME, SellingMenu(GameController, GameData, GameController.inventory.current_items))

def load_goals(gc_input, gd_input):
    gd_input.add_goal(Goal1.NAME, Goal1( gd_input, gc_input))
    gd_input.add_goal(Goal2.NAME, Goal2(gd_input, gc_input))


def load_items(GameController, GameData):
    # adds all the items that exist in the game to the storage in GameData
    GameData.add_item(Cheese.NAME, Cheese(GameData, GameController))
    GameData.add_item(Bread.NAME, Bread(GameData, GameController))
    GameData.add_item(TimeSeed.NAME, TimeSeed(GameData, GameController))
    GameData.add_item(Mask.NAME, Mask(GameData, GameController))
    GameData.add_item(Stick.NAME, Stick(GameData, GameController))
    GameData.add_item(Toy.NAME, Toy(GameData, GameController))
    GameData.add_item(Book1.NAME, Book1(GameData, GameController))
    GameData.add_item(Book2.NAME, Book2(GameData, GameController))
    GameData.add_item(Book3.NAME, Book3(GameData, GameController))


    # adds the number of items to your inventory - temporary - for testing purposes
    for item in GameData.item_list:
        GameController.inventory.get_item(GameData.item_list[item].name, 2)

    # GameController.inventory.get_item(Cheese.NAME, 2)
    # GameController.inventory.get_item(Bread.NAME, 2)


def load_key_items(GameController, GameData):
    # adds all the key items that exist in the game to the storage in GameData
    GameData.add_key_item(Shovel.NAME, Shovel(GameData, GameController))
    GameData.add_key_item(Hammer.NAME, Hammer(GameData, GameController))
    GameData.add_key_item(SeedPouch.NAME, SeedPouch(GameData, GameController))

    # GameData.add_key_item("Hammer", KeyItem("Hammer", GameData, GameController))
    # GameData.add_key_item("Clippers", KeyItem("Clippers", GameData, GameController))
    # GameData.add_key_item("Gameboy", KeyItem("Gameboy", GameData, GameController))
    # GameData.add_key_item("Radio", KeyItem("Radio", GameData, GameController))
    # GameData.add_key_item("Net", KeyItem("Net", GameData, GameController))


    # adds the key item to your key item inventory - for testing purposes
    GameController.inventory.get_key_item(Hammer.NAME)
    GameController.inventory.get_key_item(Shovel.NAME)
    GameController.inventory.get_key_item(SeedPouch.NAME)

    # GameController.inventory.get_key_item("Clippers")
    # GameController.inventory.get_key_item("Gameboy")
    # GameController.inventory.get_key_item("Radio")
    # GameController.inventory.get_key_item("Net")



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