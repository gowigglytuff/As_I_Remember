from room_page import *
from goals import *
from goals import *
from room_page import *
from key_items import *
from ss_outfits import *


def init_game(gd_input, gc_input, gst_input):
    '''
    :type gc_input: GameController
    :type gd_input: GameData
    :return: None
    '''

    # initialize pygame
    pygame.init()
    pygame.display.set_caption('As I Remember')
    pygame.key.set_repeat()

    # start_music(gc_input, gd_input)

    # Load all the different keyboard modes that you encounter when in different things like the menus and stuff
    load_keyboard_managers(gc_input, gd_input, gst_input)
    load_menus2(gc_input, gd_input)
    load_items(gc_input, gd_input)
    load_outfits(gc_input, gd_input)
    load_key_items(gc_input, gd_input)
    load_goals(gc_input, gd_input)
    load_tileset(gc_input, gd_input)
    load_player(gc_input, gd_input)
    init_all_rooms(gc_input, gd_input, gst_input)
    load_spreadsheets(gc_input, gd_input)
    gc_input.read_all_states()



def start_music(GameController, GameData):
    pygame.mixer.init()
    pygame.mixer.music.load("assets/music/little_song.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)

def load_player(GameController, GameData):
    GameData.add_player(Player.NAME, Player(0, 0, GameController, GameData))
    GameData.player[Player.NAME].activate_timer()

def load_tileset(GameController, GameData):
    # Load the Tileset
    T = TileSet("assets/room_maps/csv_tiles/MapTileset.png", 32, 32, 40, 40)
    # store each tile in a dictionary in GameData that will be accessed by the TileMap function
    GameData.add_tile_dict(T.load_tile_images())

def load_spreadsheets(GameController, GameData):
    GameData.add_spreadsheet(ThanksSpreadsheet.NAME, ThanksSpreadsheet(GameController, GameData))
    GameData.add_spreadsheet(PlayerLocationSheet.NAME, PlayerLocationSheet(GameController, GameData))


def load_keyboard_managers(GameController, GameData, gst_input):
    # load all keyboard managers
    GameData.add_keyboard_manager(InGame.ID, InGame(GameController, GameData, gst_input))
    GameData.add_keyboard_manager(InMenu.ID, InMenu(GameController, GameData))

    # sets the initial Keyboard Manager to be the InGame Manager
    GameController.set_current_keyboard_manager(InGame.ID)


def load_menus2(GameController, GameData):
    # GameData.add_overlay("text_box_2", TextBox2(GameController, GameData, "text_box_2", 250, 550, Spritesheet("assets/menu_images/text_box.png", 500, 150)))
    GameData.add_menu(GameActionDialogue.NAME, GameActionDialogue(GameController, GameData))
    GameData.add_menu(StatsMenu.NAME, StatsMenu(GameController, GameData))
    GameData.add_menu(UseMenu.NAME, UseMenu(GameController, GameData))
    GameData.add_menu(YesNoMenu.NAME, YesNoMenu(GameController, GameData))

    GameData.add_menu(StartMenu.NAME, StartMenu(GameController, GameData))
    GameData.add_menu(InventoryMenu.NAME, InventoryMenu(GameController, GameData))
    GameData.add_menu(KeyInventoryMenu.NAME, KeyInventoryMenu(GameController, GameData))
    GameData.add_menu(ToDoListMenu.NAME, ToDoListMenu(GameController, GameData))
    GameData.add_menu(ProfileMenu.NAME, ProfileMenu(GameController, GameData))
    GameData.add_menu(MapMenu.NAME, MapMenu(GameController, GameData))
    GameData.add_menu(OutfitsMenu.NAME, OutfitsMenu(GameController, GameData))
    GameData.add_menu(HitchikingMenu.NAME, HitchikingMenu(GameController, GameData))

    GameData.add_menu(ConversationOptionsMenu.NAME, ConversationOptionsMenu(GameController, GameData))
    GameData.add_menu(CharacterDialogue.NAME, CharacterDialogue(GameController, GameData))
    GameData.add_menu(GiftingMenu.NAME, GiftingMenu(GameController, GameData))

    GameData.add_menu(ShopKeeperInteractMenu.NAME, ShopKeeperInteractMenu(GameController, GameData))
    GameData.add_menu(ShopkeeperDialogue.NAME, ShopkeeperDialogue(GameController, GameData))
    GameData.add_menu(BuyingMenu.NAME, BuyingMenu(GameController, GameData))
    GameData.add_menu(SellingMenu.NAME, SellingMenu(GameController, GameData))

    GameData.add_menu(GameMasterInteractMenu.NAME, GameMasterInteractMenu(GameController, GameData))
    GameData.add_menu(InfoSelectMenu.NAME, InfoSelectMenu(GameController, GameData))


def load_goals(gc_input, gd_input):
    gd_input.add_goal(Goal1.NAME, Goal1( gd_input, gc_input))
    gd_input.add_goal(Goal2.NAME, Goal2(gd_input, gc_input))


def load_outfits(GameController, GameData):
    GameData.add_outfit(CowboyOutfit.NAME, CowboyOutfit(GameData, GameController))
    GameData.add_outfit(NormalOutfit.NAME, NormalOutfit(GameData, GameController))
    GameData.add_outfit(FrogOutfit.NAME, FrogOutfit(GameData, GameController))
    GameData.add_outfit(ShumaOutfit.NAME, ShumaOutfit(GameData, GameController))


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
    GameData.add_item(FossilA.NAME, FossilA(GameData, GameController))
    GameData.add_item(FossilB.NAME, FossilB(GameData, GameController))
    GameData.add_item(FossilC.NAME, FossilC(GameData, GameController))

    # TODO: Make this only the items you start with
    # adds the number of items to your inventory - temporary - for testing purposes
    for item in GameData.item_list:
        GameController.inventory.get_item(GameData.item_list[item].name, 2)


def load_key_items(GameController, GameData):
    # adds all the key items that exist in the game to the storage in GameData
    GameData.add_key_item(Shovel.NAME, Shovel(GameData, GameController))
    GameData.add_key_item(Hammer.NAME, Hammer(GameData, GameController))
    GameData.add_key_item(SeedPouch.NAME, SeedPouch(GameData, GameController))
    GameData.add_key_item(HitchingThumb.NAME, HitchingThumb(GameData, GameController))
    GameData.add_key_item(WaterBottle.NAME, WaterBottle(GameData, GameController))
    GameData.add_key_item(GymPass.NAME, GymPass(GameData, GameController))
    GameData.add_key_item(BirdCall.NAME, BirdCall(GameData, GameController))
    GameData.add_key_item(Cellphone.NAME, Cellphone(GameData, GameController))
    GameData.add_key_item(Net.NAME, Net(GameData, GameController))
    GameData.add_key_item(Radio.NAME, Radio(GameData, GameController))
    GameData.add_key_item(Lighter.NAME, Lighter(GameData, GameController))
    GameData.add_key_item(Gameboy.NAME, Gameboy(GameData, GameController))
    GameData.add_key_item(Boomerang.NAME, Boomerang(GameData, GameController))
    GameData.add_key_item(CoopNumber.NAME, CoopNumber(GameData, GameController))
    GameData.add_key_item(Compass.NAME, Compass(GameData, GameController))


    # TODO: Make it so you get all these throughout the game
    # adds the key item to your key item inventory - for testing purposes
    GameController.inventory.get_key_item(Hammer.NAME)
    GameController.inventory.get_key_item(Shovel.NAME)
    GameController.inventory.get_key_item(SeedPouch.NAME)
    GameController.inventory.get_key_item(HitchingThumb.NAME)
    GameController.inventory.get_key_item(WaterBottle.NAME)
    GameController.inventory.get_key_item(GymPass.NAME)
    GameController.inventory.get_key_item(BirdCall.NAME)
    GameController.inventory.get_key_item(Cellphone.NAME)
    GameController.inventory.get_key_item(Net.NAME)
    GameController.inventory.get_key_item(Radio.NAME)
    GameController.inventory.get_key_item(Lighter.NAME)
    GameController.inventory.get_key_item(Gameboy.NAME)
    GameController.inventory.get_key_item(Boomerang.NAME)
    GameController.inventory.get_key_item(CoopNumber.NAME)
    GameController.inventory.get_key_item(Compass.NAME)


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

def init_all_rooms(gc_input, gd_input, gst_input):

    gd_input.add_room("Ringside", Ringside(gc_input, gd_input, gst_input))
    gd_input.room_list["Ringside"].activate_room()

    gd_input.add_room("Sandpiper", Sandpiper(gc_input, gd_input, gst_input))
    gd_input.room_list["Sandpiper"].activate_room()

    gd_input.add_room("computer_centre", ComputerCentreRoom(gc_input, gd_input, gst_input))
    gd_input.room_list["computer_centre"].activate_room()

    gd_input.add_room("hornby_creative", HornbyCreativeRoom(gc_input, gd_input, gst_input))
    gd_input.room_list["hornby_creative"].activate_room()

    gd_input.add_room("to_the_moon", ToTheMoon(gc_input, gd_input, gst_input))
    gd_input.room_list["to_the_moon"].activate_room()

    gd_input.add_room("hornby_realestate", HornbyRealestate(gc_input, gd_input, gst_input))
    gd_input.room_list["hornby_realestate"].activate_room()

    gd_input.add_room("island_potters", IslandPotters(gc_input, gd_input, gst_input))
    gd_input.room_list["island_potters"].activate_room()

    gd_input.add_room("bike_shop", BikeShop(gc_input, gd_input, gst_input))
    gd_input.room_list["bike_shop"].activate_room()
