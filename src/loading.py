import pygame
from data import *
from features import *
from mapClasses import *

def init_game(gd, gc):
    pygame.init()
    pygame.display.set_caption('NPC')

    # add the player to the game
    gd.add_player("Player", Player(2, 2, 2, 2, 32, 40, ["assets/player/P_front.png"], "Bug", "down", gc, gd))


    # add the NPC characters to the game
    gd.add_character("Walker", NPC(2, 3, 2, 3, 32, 40, ["assets/walk_left/f3.png", "assets/walk_left/f4.png", "assets/walk_left/f1.png", "assets/walk_left/f2.png","assets/walk_left/f3.png", "assets/walk_left/f4.png", "assets/walk_left/f1.png", "assets/walk_left/f2.png",
                                "assets/walk_right/right_3.png", "assets/walk_right/right_4.png", "assets/walk_right/right_1.png", "assets/walk_right/right_2.png", "assets/walk_right/right_3.png", "assets/walk_right/right_4.png", "assets/walk_right/right_1.png", "assets/walk_right/right_2.png"],
                                   "Walker", "idle", gc, gd, "left", pygame.USEREVENT + 4, pygame.USEREVENT + 6))

    gd.add_character("Pink_Walker", NPC(5, 5, 5, 5, 32, 40, ["assets/NPC2/pinkNPC_left_1.png", "assets/NPC2/pinkNPC_left_2.png", "assets/NPC2/pinkNPC_left_3.png", "assets/NPC2/pinkNPC_left_4.png", "assets/NPC2/pinkNPC_left_1.png", "assets/NPC2/pinkNPC_left_2.png", "assets/NPC2/pinkNPC_left_3.png", "assets/NPC2/pinkNPC_left_4.png",
                                                             "assets/NPC2/pinkNPC_right_1.png", "assets/NPC2/pinkNPC_right_2.png", "assets/NPC2/pinkNPC_right_3.png", "assets/NPC2/pinkNPC_right_4.png", "assets/NPC2/pinkNPC_right_1.png", "assets/NPC2/pinkNPC_right_2.png", "assets/NPC2/pinkNPC_right_3.png", "assets/NPC2/pinkNPC_right_4.png"],
                                                             "Pink_Walker", "idle", gc, gd, "left", pygame.USEREVENT + 7, pygame.USEREVENT + 9))

    gd.add_prop("Prop1", Prop(3, 3, 3, 2.9, 32, 40, ["assets/prop1.png"], "Prop1"))

    # add the room, generate the grid, and add the background
    gd.add_room("room1", Room("room1", 1, 1, 6, 6, [], ["room1"]))
    gd.room["room1"].generate_room_grid()
    gd.room["room1"].add_room_BG("room1", BG(1, 1, "room1", ["assets/BG.png"]))

    gd.room["room1"].add_room_character("Walker")
    gd.room["room1"].add_room_character("Pink_Walker")
    gd.room["room1"].add_room_prop("Prop1")

    # add position manager to it's room and make it tell the tile array what it's filled with
    gd.add_positioner("room1", Position_Manager("room1", gc, gd))
    gd.positioner["room1"].fill_tiles()

    # activate the timers for animation and actions for the NPC Walker (make this apply to all that are in room)
    for character in gd.character:
        gd.character[character].activate_timers()