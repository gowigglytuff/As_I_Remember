from random import randrange

import pygame, csv, os

from TileMap import TileMap
from features import GenericNPC, Spritesheet, TammaNPC, StandingNPC, ShopKeeper, ShopKeeperTamma, ShopKeeperCheryl
from prop_page import GenericProp, Tree, Decoration, Building, BenchHorizontal, BenchVertical, PlumTree, PicnicTable, Computer, Counter, ComputerBack, Bookcase, Dress
from keyboards import Direction, Facing
from mapClasses import Plot, Door, Tile, Position_Manager


class Room(object):
    def __init__(self, gc_input, gd_input):
        self.gc_input = gc_input
        self.gd_input = gd_input

        self.name = None
        self.room_width = 0
        self.room_height = 0
        self.left_edge_x = 0
        self.top_edge_y = 0
        self.right_edge_x = 0
        self.bottom_edge_y = 0

        self.map_style = None

        self.plot_list = {}
        self.total_plots_x = 0
        self.total_plots_y = 0
        self.plot_size_x = 0
        self.plot_size_y = 0
        self.active_plots = []

        self.tiles_array = []
        self.active_tiles = []

        self.door_list = {}
        self.character_list = []
        self.decoration_list = []
        self.prop_list = []

        self.building_height = 1

        self.terrain_map = None
        self.obstacle_map = None

    def add_room_plots(self, img, terrain_file):
        for plots_x in range(self.total_plots_x):
            for plots_y in range(self.total_plots_y):
                #print(plots_x + 1, plots_y + 1)
                self.gd_input.room_list[self.name].add_room_plot((self.name + "_" + str(plots_x+1) + "_" + str(plots_y+1)), Plot(self.name, plots_x+1, plots_y+1, img, self.gc_input, self.gd_input, terrain_file))

    def generate_room_grid(self):
        """
        adds an array to tiles_array which is a grid for the current room
        :return: null
        """
        for section in range(self.room_width + 3):
            section_name = []
            self.tiles_array.append(section_name)

        for letter in range(self.room_width + 2):
            for number in range(self.room_height + 3):
                spot_name = Tile(letter, number, False, "None", "None")
                self.tiles_array[letter].append(spot_name)

    def add_room_plot(self, plot_name, plot_object):
        self.plot_list[plot_name] = plot_object

    def add_room_character(self, character_name):
        self.character_list.append(character_name)

    def add_room_prop(self, prop_name):
        self.prop_list.append(prop_name)

    def add_room_decoration(self, decoration_name):
        self.decoration_list.append(decoration_name)

    def add_room_door(self, door_name, door_object):
        self.door_list[door_name] = door_object

    def activate_plot(self, plot_name):
        self.active_plots.append(plot_name)

    def draw_bg(self, screen):
        for plot in self.active_plots:
            self_x = (((((self.plot_list[plot].plot_x)-1) * self.plot_size_x + self.gc_input.camera[0]) + 1) * self.gd_input.square_size[0]) + self.gd_input.base_locator_x
            self_y = (((((self.plot_list[plot].plot_y)-1) * self.plot_size_y + self.gc_input.camera[1]) + 1) * self.gd_input.square_size[1]) + self.gd_input.base_locator_y
            screen.blit(self.plot_list[plot].plot_img, (self_x, self_y))

    def add_room_and_plots(self):
        pass
    def add_room_doors(self):
        pass
    def add_room_characters(self):
        pass
    def add_room_props(self):
        pass

    def activate_room(self):
        self.add_room_and_plots()
        self.gd_input.room_list[self.name].generate_room_grid()
        self.add_room_doors()
        self.add_room_characters()
        self.add_room_props()
        # add position manager to it's room and make it tell the tile array what it's filled with
        self.gd_input.add_positioner(self.name, Position_Manager(self.name, self.gc_input, self.gd_input))
        self.gd_input.positioner[self.name].fill_tiles(self.name)
        self.gd_input.positioner[self.name].fill_doors(self.name)
        # activate the timers for animation and actions for the NPCs (make this apply to all that are in room)
        for character in self.gd_input.room_list[self.name].character_list:
            self.gd_input.character_list[character].activate_timers()

        #TODO: make this uses the plots csv instead of the rooms
        if self.obstacle_map is not None:
            self.gd_input.positioner[self.name].fill_obstacles(self.obstacle_map, self.name)


        if self.terrain_map is not None:
            self.gd_input.positioner[self.name].fill_terrain(self.terrain_map, self.name)


class Room1(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.terrain_map = None
        self.obstacle_map = None

        self.name = "room1"
        self.room_width = 6
        self.room_height = 6
        self.left_edge_x = 1
        self.top_edge_y = 2

        self.right_edge_x = self.left_edge_x + self.room_width - 1
        self.bottom_edge_y = self.top_edge_y + self.room_height - 1

        self.map_style = "image"

        self.total_plots_x = 1
        self.total_plots_y = 1
        self.plot_size_x = int(self.room_width/self.total_plots_x)
        self.plot_size_y = int(self.room_height/self.total_plots_y)

    def add_room_and_plots(self):
        self.gd_input.room_list[self.name].add_room_plot("room1_1_1", Plot("room1", 1, 1, pygame.image.load("assets/backgrounds/room_1_background.png"), self.gc_input, self.gd_input, None))
        self.gd_input.room_list[self.name].activate_plot("room1_1_1")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("ringside_door1", Door(self.name, "Ringside", 2, 2, 8, 70, "ringside_door1"))
        self.gd_input.room_list[self.name].add_room_door("ringside_door2", Door(self.name, "room4", 5, 1, 2, 4, "room1_door2"))

    def add_room_characters(self):
        self.gd_input.add_character("Shuma", GenericNPC(2, 4, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Shuma.png", 32, 40), "Shuma", self.name, "Your dad have manure for sale? I'd really love to get my hands on a couple bags of it. It's great for the turnips and the kale! Though I think I might get some nitrogen fixed stuff from the co-op for the lettuce...", "pace", Facing.FRONT))
        self.gd_input.add_character("Maggie", GenericNPC(5, 5, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Maggie.png", 32, 40), "Maggie", self.name, "This outfit makes me feel really cool and powerful, so I've decided I'm going to wear it everywhere.", "stand_still", Facing.FRONT))
        self.gd_input.add_character("Laurie", GenericNPC(4, 3, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Laurie.png", 32, 40), "Laurie", self.name, "Have you seen my drink anywhere?", "square", Facing.FRONT))

    def add_room_props(self):
        self.gd_input.add_prop("trunk", GenericProp(3, 2, self.gc_input, self.gd_input, 32, 40, Spritesheet("assets/prop_sprites/trunk.png", 32, 40), "trunk", 1, 1, self.name))
        self.gd_input.add_prop("lamp", GenericProp(1, 5, self.gc_input, self.gd_input, 32, 40, Spritesheet("assets/prop_sprites/lamp.png", 32, 40), "lamp", 1, 1, self.name))

class Room2(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)

        self.terrain_map = "assets/room_maps/room2.csv"
        self.obstacle_map = "assets/room_maps/room2.csv"

        self.name = "room2"
        self.room_width = 15
        self.room_height = 15
        self.left_edge_x = 1
        self.top_edge_y = 1

        self.right_edge_x = self.left_edge_x + self.room_width - 1
        self.bottom_edge_y = self.top_edge_y + self.room_height - 1

        self.map_style = "csv"

        self.total_plots_x = 1
        self.total_plots_y = 1
        self.plot_size_x = int(self.room_width/self.total_plots_x)
        self.plot_size_y = int(self.room_height/self.total_plots_y)

    def add_room_and_plots(self):
        self.gd_input.room_list[self.name].add_room_plot("room2_1_1", Plot(self.name, 1, 1, TileMap("assets/room_maps/csv_tiles/lake.csv", self.gd_input.tiles_img_dict).return_map(), self.gc_input, self.gd_input, "assets/room_maps/room2.csv"))
        self.gd_input.room_list[self.name].activate_plot("room2_1_1")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("room2_door1", Door(self.name, "room1", 1, 14, 2, 3, "room2_door1"))
        self.gd_input.room_list[self.name].add_room_door("room2_door2", Door(self.name, "room3", 8, 12, 2, 4, "room2_door2"))
        self.gd_input.room_list[self.name].add_room_door("room2_door3", Door(self.name, "Coop", 13, 12, 1, 56, "room2_door3"))
        self.gd_input.room_list[self.name].add_room_door("room2_door4", Door(self.name, "room6", 14, 8, 7, 4, "room2_door4"))

    def add_room_characters(self):
        self.gd_input.add_character("Deb", GenericNPC(4, 4, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Deb.png", 32, 40), "Deb", self.name, "Hey Shuma, so nice to see you again!, I should probably be in the studio, but when I'm low on inspiration I like to come out here and walk by the water. ", "square", Facing.FRONT))
        self.gd_input.add_character("Alex", GenericNPC(9, 9, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/alex_lamont_CS.png", 32, 40), "Alex", self.name, "Hey Shuma, nice to see you! Stop by later and I'll sling you some free icecream! haha... I'm just kidding it's $5.00 a cone.", "left_right", Facing.FRONT))
        self.gd_input.add_character("Jamara", GenericNPC(6, 8, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Jamara_CS.png", 32, 40), "Jamara", self.name, "What do you think the greatest joy in life is? I haven't figured it out yet... I enjoy a whole lot of stuff, but I feel like nothing I've done so far is quite it.", "pace", Facing.FRONT))
        self.gd_input.add_character("Donna", GenericNPC(3, 11, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Donna_Tuelle_CS.png", 32, 40), "Donna", self.name, "You know, Jennessa does such a good job, I'm almost considering retiring... not quite, but a very strong almost.", "square", Facing.FRONT))

    def add_room_props(self):
        self.gd_input.add_prop("house", GenericProp(5, 10, self.gc_input, self.gd_input, 160, 128, Spritesheet("assets/prop_sprites/Buildings/House.png", 160, 128), "house", 5, 3, self.name))
        self.gd_input.add_prop("tree1", Tree(3, 6, "tree1", self.gc_input, self.gd_input, self.name))
        self.gd_input.add_prop("tree2", Tree(6, 6, "tree2", self.gc_input, self.gd_input, self.name))
        self.gd_input.add_prop("tree3", Tree(9, 6, "tree3", self.gc_input, self.gd_input, self.name))

        self.gd_input.add_decoration("Grass", Decoration(0, 0, self.gc_input, self.gd_input, 32, 32, Spritesheet("assets/decoration_sprites/grass5.png", 32, 32), "Grass", 1, 1, [[2, 11], [2, 12], [2, 13], [2, 14], [3, 11], [3, 12], [3, 13], [3, 14]], self.name))

class Room3(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.terrain_map = None
        self.obstacle_map = None

        self.name = "room3"
        self.room_width = 3
        self.room_height = 3
        self.left_edge_x = 1
        self.top_edge_y = 2

        self.right_edge_x = self.left_edge_x + self.room_width - 1
        self.bottom_edge_y = self.top_edge_y + self.room_height - 1

        self.map_style = "image"

        self.total_plots_x = 1
        self.total_plots_y = 1
        self.plot_size_x = int(self.room_width/self.total_plots_x)
        self.plot_size_y = int(self.room_height/self.total_plots_y)

    def add_room_and_plots(self):
        self.gd_input.room_list[self.name].add_room_plot("room3_1_1", Plot(self.name, 1, 1, pygame.image.load("assets/backgrounds/room_3_background.png"), self.gc_input, self.gd_input, None))
        self.gd_input.room_list[self.name].activate_plot("room3_1_1")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("room3_door1", Door(self.name, "room2", 2, 5, 8, 13, "room3_door1"))

    def add_room_characters(self):
        self.gd_input.add_character("Pixie", GenericNPC(2, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/sprite_sheet.png", 32, 40), "Pixie", "room3", "Hi!", "stand_still", Facing.FRONT))
        self.gd_input.add_character("Pixie_b", GenericNPC(3, 4, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/sprite2_sheet.png", 32, 40), "Pixie_b", "room3", "Hi!", "stand_still", Facing.FRONT))
        self.gd_input.add_character("Ian", GenericNPC(3, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Ian.png", 32, 40), "Ian", "room3", "Damnit, the cows got out again... If you see Kleyo can you ask her to give me a call? I should be back at the house by five.", "stand_still", Facing.FRONT))

    def add_room_props(self):
        pass

class Room4(Room):
    def __init__(self, gc_input, gd_input):
            super().__init__(gc_input, gd_input)
            self.terrain_map = None
            self.obstacle_map = "assets/room_maps/big_map.csv"

            self.name = "room4"
            self.room_width = 100
            self.room_height = 50
            self.left_edge_x = 1
            self.top_edge_y = 1

            self.right_edge_x = self.left_edge_x + self.room_width - 1
            self.bottom_edge_y = self.top_edge_y + self.room_height - 1

            self.map_style = "csv"

            self.total_plots_x = 2
            self.total_plots_y = 1
            self.plot_size_x = int(self.room_width / self.total_plots_x)
            self.plot_size_y = int(self.room_height / self.total_plots_y)

    def add_room_and_plots(self):
        big_map = TileMap("assets/room_maps/csv_tiles/big_map2.0.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list[self.name].add_room_plot("room4_1_1", Plot(self.name, 1, 1, big_map.return_map(), self.gc_input, self.gd_input, "assets/room_maps/big_map.csv"))
        self.gd_input.room_list[self.name].add_room_plot("room4_1_2", Plot(self.name, 2, 1, big_map.return_map(), self.gc_input, self.gd_input, "assets/room_maps/big_map.csv"))
        self.gd_input.room_list[self.name].activate_plot("room4_1_1")
        self.gd_input.room_list[self.name].activate_plot("room4_1_2")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("room4_door1", Door(self.name, "room1", 2, 3, 5, 2, "room4_door1"))

    def add_room_characters(self):
        for name in range(50):
            rand_x = randrange(1, 100)
            rand_y = randrange(1, 50)
            self.gd_input.add_character(("Sheep" + str(name)), GenericNPC(rand_x, rand_y, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/sheep.png", 32, 40), ("Sheep" + str(name)), "room4", "Baaaahhhh", "stand_still", Facing.FRONT))

    def add_room_props(self):
        pass

class Room5(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.terrain_map = "assets/room_maps/Coop_allowance.csv"
        self.obstacle_map = "assets/room_maps/Coop_allowance.csv"

        self.name = "Coop"
        self.room_width = 36
        self.room_height = 60
        self.left_edge_x = 1
        self.top_edge_y = 1

        self.right_edge_x = self.left_edge_x + self.room_width - 1
        self.bottom_edge_y = self.top_edge_y + self.room_height - 1

        self.map_style = "csv"

        self.total_plots_x = 1
        self.total_plots_y = 1
        self.plot_size_x = int(self.room_width / self.total_plots_x)
        self.plot_size_y = int(self.room_height / self.total_plots_y)

    def add_room_and_plots(self):
        coop_map = TileMap("assets/room_maps/Co-op_area.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list["Coop"].add_room_plot("Coop_1_1", Plot("Coop", 1, 1, coop_map.return_map(), self.gc_input, self.gd_input, "assets/room_maps/Coop_allowance.csv"))
        self.gd_input.room_list[self.name].activate_plot("Coop_1_1")

    def add_room_doors(self):
        self.gd_input.room_list["Coop"].add_room_door("Coop_door1", Door("Coop", "room2", 1, 57, 13, 11, "Coop_door1"))

    def add_room_characters(self):
        pass

    def add_room_props(self):
        #self.gd_input.add_prop("Coop_Building", Coop(2, 2, self.gc_input, self.gd_input, 832, 1632, "assets/prop_sprites/Buildings/Coop_Building.png", "Coop_Building", 26, 51, self.name))
        #self.gd_input.add_prop("Computer_Centre", ComputerCentre(25, 53, self.gc_input, self.gd_input, 192, 128, "assets/prop_sprites/Buildings/computer_centre.png", "Computer_Centre", 6, 4, self.name))
        #self.gd_input.add_prop("Island_Potters", IslandPotters(7, 53, self.gc_input, self.gd_input, 160, 96, "assets/prop_sprites/Buildings/island_potters.png", "Island_Potters", 5, 3, self.name))
        #self.gd_input.add_prop("Lix", Lix(23, 42, self.gc_input, self.gd_input, (8*32), (5*32), "assets/prop_sprites/Buildings/lix.png", "Lix", 8, 5, self.name))
        #self.gd_input.add_prop("Real_Estate", RealEstate(1, 52, self.gc_input, self.gd_input, (5*32), (5*32), "assets/prop_sprites/Buildings/real_estate_2.png", "Real_Estate", 5, 5, self.name))
        pass

class Room6(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)

        self.terrain_map = None
        self.obstacle_map = None

        self.name = "room6"
        self.room_width = 10
        self.room_height = 10
        self.left_edge_x = 1
        self.top_edge_y = 1

        self.right_edge_x = self.left_edge_x + self.room_width - 1
        self.bottom_edge_y = self.top_edge_y + self.room_height - 1

        self.map_style = "image"

        self.total_plots_x = 1
        self.total_plots_y = 1
        self.plot_size_x = int(self.room_width/self.total_plots_x)
        self.plot_size_y = int(self.room_height/self.total_plots_y)

    def add_room_and_plots(self):
        room6_map = TileMap("assets/room_maps/room6.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list[self.name].add_room_plot("room6_1_1", Plot("room6", 1, 1, room6_map.return_map(), self.gc_input, self.gd_input, None))
        self.gd_input.room_list[self.name].activate_plot("room6_1_1")
    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("room6_door1", Door(self.name, "room2", 7, 5, 14, 9, "room6_door1"))
    def add_room_characters(self):
        pass
    def add_room_props(self):
        pass

class Ringside(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.terrain_map = None
        self.obstacle_map = None

        self.name = "Ringside"
        self.room_width = 55
        self.room_height = 106
        self.left_edge_x = 1
        self.top_edge_y = 1

        self.right_edge_x = self.left_edge_x + self.room_width - 1
        self.bottom_edge_y = self.top_edge_y + self.room_height - 1

        self.map_style = "image"

        self.total_plots_x = 1
        self.total_plots_y = 1
        self.plot_size_x = int(self.room_width / self.total_plots_x)
        self.plot_size_y = int(self.room_height / self.total_plots_y)

    def add_room_and_plots(self):
        ringside_map = TileMap("assets/room_maps/ringside_map.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list["Ringside"].add_room_plot("Ringside_1_1", Plot("Coop", 1, 1, ringside_map.return_map(), self.gc_input, self.gd_input, "assets/room_maps/ringside_map.csv"))
        self.gd_input.room_list[self.name].activate_plot("Ringside_1_1")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("ringside_to_computer_centre", Door("Ringside", "computer_centre", 11, 84, 3, 3, "ringside_to_computer_centre"))
        self.gd_input.room_list[self.name].add_room_door("ringside_to_hornby_creative", Door("Ringside", "hornby_creative", 12, 76, 4, 3, "ringside_to_hornby_creative"))
        self.gd_input.room_list[self.name].add_room_door("ringside_to_to_the_moon", Door("Ringside", "to_the_moon", 41, 81, 2, 3, "ringside_to_to_the_moon"))
        self.gd_input.room_list[self.name].add_room_door("ringside_to_hornby_realestate", Door("Ringside", "hornby_realestate", 39, 75, 1, 3, "ringside_to_hornby_realestate"))
        self.gd_input.room_list[self.name].add_room_door("ringside_to_island_potters_1", Door("Ringside", "island_potters", 39, 63, 2, 3,  "ringside_to_island_potters_1"))
        self.gd_input.room_list[self.name].add_room_door("ringside_to_island_potters_2", Door("Ringside", "island_potters", 41, 63, 4, 3, "ringside_to_island_potters_2"))
        self.gd_input.room_list[self.name].add_room_door("ringside_to_bike_shop", Door("Ringside", "bike_shop", 40, 91, 2, 6, "ringside_to_bike_shop"))

    def add_room_characters(self):
        self.gd_input.add_character("Deb", GenericNPC(29, 76, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Deb.png", 32, 40), "Deb", self.name, "Something strange is going on around here, have you heard about the children disapearing? Their parents couldn't even remember their names...", "look_around", Facing.FRONT))
        self.gd_input.add_character("Alex", GenericNPC(17, 70, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/alex_lamont_CS.png", 32, 40), "Alex", self.name, "Hey Shuma, I feel like I haven't seen you in a long time... but didn't we just go to the beach togther on Friday? I seem to be losing track of time so much recently...", "square", Facing.FRONT))
        self.gd_input.add_character("Jamara", GenericNPC(31, 90, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Jamara_CS.png", 32, 40), "Jamara", self.name, "What do you think the greatest joy in life is? I haven't figured it out yet... I enjoy a whole lot of stuff, but I feel like nothing I've done so far is quite it.", "pace", Facing.FRONT))
        self.gd_input.add_character("Donna", GenericNPC(39, 78, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Donna_Tuelle_CS.png", 32, 40), "Donna", self.name, "You know, it's the strangest thing, my daughter Alex showed up the other day to ask me to watch her kids... but I don't remember having grandkids. I watched them anyway, but I swear I've never met them...", "left_right", Facing.FRONT))
        self.gd_input.add_character("Clair", GenericNPC(30, 60, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Clair_CS.png", 32, 40), "Clair", self.name, "I love this place but sometimes I feel like I should just pack everything up and run far away...", "square", Facing.FRONT))

    def add_room_props(self):
            self.gd_input.add_prop("Coop_Building", Building(10, 8, self.gc_input, self.gd_input, 832, 1632, "assets/prop_sprites/Buildings/Coop_Building.png", "Coop_Building", 26, 51, self.name, "assets/prop_sprites/Buildings/building_csv/coop_fill_csv.csv"))
            self.gd_input.add_prop("Computer_Centre", Building(9, 82, self.gc_input, self.gd_input, 192, 128, "assets/prop_sprites/Buildings/computer_centre.png", "Computer_Centre", 6, 4, self.name, "assets/prop_sprites/Buildings/building_csv/computer_centre_fill_map.csv"))
            self.gd_input.add_prop("Hornby_Creative", Building(9, 74, self.gc_input, self.gd_input, 192, 128, "assets/prop_sprites/Buildings/hornby_creative.png", "Hornby_Creative", 6, 4, self.name, "assets/prop_sprites/Buildings/building_csv/hornby_creative_fill_map.csv"))
            self.gd_input.add_prop("Island_Potters", Building(38, 61, self.gc_input, self.gd_input, 160, 96, "assets/prop_sprites/Buildings/island_potters.png", "Island_Potters", 5, 3, self.name, "assets/prop_sprites/Buildings/building_csv/island_potters_fill_map.csv"))
            self.gd_input.add_prop("Lix", Building(15, 63, self.gc_input, self.gd_input, (8*32), (5*32), "assets/prop_sprites/Buildings/lix.png", "Lix", 8, 5, self.name, "assets/prop_sprites/Buildings/building_csv/lix_fill_map.csv"))
            self.gd_input.add_prop("Real_Estate", Building(38, 72, self.gc_input, self.gd_input, (5*32), (5*32), "assets/prop_sprites/Buildings/real_estate_2.png", "Real_Estate", 5, 5, self.name, "assets/prop_sprites/Buildings/building_csv/real_estate_csv.csv"))
            self.gd_input.add_prop("To_The_Moon", Building(39, 78, self.gc_input, self.gd_input, (5 * 32), (5 * 32), "assets/prop_sprites/Buildings/to_the_moon.png", "To_The_Moon", 5, 5, self.name, "assets/prop_sprites/Buildings/building_csv/to_the_moon_fill_map.csv"))
            self.gd_input.add_prop("Fibres", Building(31, 60, self.gc_input, self.gd_input, (5 * 32), (5 * 32), "assets/prop_sprites/Buildings/Fibres.png", "Fibres", 5, 5, self.name, "assets/prop_sprites/Buildings/building_csv/fibres_fill_map.csv"))
            self.gd_input.add_prop("Vorizo", Building(27, 93, self.gc_input, self.gd_input, (3 * 32), (3 * 32), "assets/prop_sprites/Buildings/vorizo.png", "Vorizo", 3, 3, self.name, "assets/prop_sprites/Buildings/building_csv/vorizo_fill_map.csv"))
            self.gd_input.add_prop("Bike_Shop", Building(39, 85, self.gc_input, self.gd_input, (4 * 32), (7 * 32), "assets/prop_sprites/Buildings/bike_shop.png", "Bike_Shop", 4, 7, self.name, "assets/prop_sprites/Buildings/building_csv/bike_shop_fill_map.csv"))

            self.gd_input.add_prop("tree1", Tree(29, 74, "tree1", self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop("Bench1", BenchHorizontal(28, 78, "Bench1", self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop("Bench2", BenchHorizontal(29, 70, "Bench2", self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop("Bench4", BenchVertical(26, 73, "Bench4", self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop("Bench5", BenchVertical(33, 73, "Bench5", self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop("Bench6", BenchVertical(22, 69, "Bench6", self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop("Bench7", BenchVertical(21, 79, "Bench7", self.gc_input, self.gd_input, self.name))

            self.gd_input.add_prop("tree2", Tree(37, 69, "tree2", self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop("Bench3", BenchHorizontal(37, 70, "Bench3", self.gc_input, self.gd_input, self.name))

            self.gd_input.add_prop("Picnic_Table5", PicnicTable(17, 82, "Picnic_Table5", self.gc_input, self.gd_input, self.name))

            self.gd_input.add_prop("Picnic_Table1", PicnicTable(9, 65, "Picnic_Table1", self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop("Picnic_Table2", PicnicTable(9, 69, "Picnic_Table2", self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop("Picnic_Table3", PicnicTable(13, 65, "Picnic_Table3", self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop("Picnic_Table4", PicnicTable(13, 69, "Picnic_Table4", self.gc_input, self.gd_input, self.name))

class ComputerCentreRoom(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)

        self.terrain_map = None
        self.obstacle_map = None

        self.name = "computer_centre"
        self.room_width = 6
        self.room_height = 2
        self.left_edge_x = 1
        self.top_edge_y = 2

        self.right_edge_x = self.left_edge_x + self.room_width - 1
        self.bottom_edge_y = self.top_edge_y + self.room_height - 1

        self.map_style = "image"

        self.total_plots_x = 1
        self.total_plots_y = 1
        self.plot_size_x = int(self.room_width/self.total_plots_x)
        self.plot_size_y = int(self.room_height/self.total_plots_y)

    def add_room_and_plots(self):
        comp_map = TileMap("assets/room_maps/computer_centre_map.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list[self.name].add_room_plot("CSM_1_1", Plot("computer_centre", 1, 1, comp_map.return_map(), self.gc_input, self.gd_input, None))
        self.gd_input.room_list[self.name].activate_plot("CSM_1_1")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("computer_centre_to_ringside", Door("computer_centre", "Ringside",  3, 4, 11, 85, "computer_centre_to_ringside"))

    def add_room_characters(self):
        self.gd_input.add_character("CC_Guy2", GenericNPC(2, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40), "CC_Guy2", self.name, "You have such strange customs here, what in the world is a yurt?", "stay_left", Facing.LEFT))
        self.gd_input.add_character("CC_Guy3", GenericNPC(4, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40), "CC_Guy3", self.name, "Leave me alone human!.. I mean... dude", "stay_left", Facing.LEFT))
        self.gd_input.add_character("CC_Guy1", GenericNPC(6, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40), "CC_Guy1", self.name, "Do you know what this strange box is?", "stay_front", Facing.FRONT))

    def add_room_props(self):
        self.gd_input.add_prop("CC_computer1", Computer(3, 2, "CC_computer1", self.gc_input, self.gd_input, "computer_centre"))
        self.gd_input.add_prop("CC_computer2", Computer(1, 2, "CC_computer2", self.gc_input, self.gd_input, "computer_centre"))
        self.gd_input.add_prop("CC_computer3", ComputerBack(6, 3, "CC_computer3", self.gc_input, self.gd_input, "computer_centre"))

class HornbyCreativeRoom(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)

        self.terrain_map = None
        self.obstacle_map = None

        self.name = "hornby_creative"
        self.room_width = 6
        self.room_height = 2
        self.left_edge_x = 1
        self.top_edge_y = 2

        self.right_edge_x = self.left_edge_x + self.room_width - 1
        self.bottom_edge_y = self.top_edge_y + self.room_height - 1

        self.map_style = "image"

        self.total_plots_x = 1
        self.total_plots_y = 1
        self.plot_size_x = int(self.room_width/self.total_plots_x)
        self.plot_size_y = int(self.room_height/self.total_plots_y)

    def add_room_and_plots(self):
        HC_map = TileMap("assets/room_maps/hornby_creative_map.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list[self.name].add_room_plot("HC_1_1", Plot("hornby_creative", 1, 1, HC_map.return_map(), self.gc_input, self.gd_input, None))
        self.gd_input.room_list[self.name].activate_plot("HC_1_1")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("hornby_creative_to_ringside", Door("hornby_creative", "Ringside", 4, 4, 12, 77, "hornby_creative_to_ringside"))

    def add_room_characters(self):
        self.gd_input.add_character("Tamma", ShopKeeperTamma(1, 2, self.gc_input, self.gd_input, self.name))
        self.gd_input.add_character("Cheryl", ShopKeeperCheryl(3, 2, self.gc_input, self.gd_input, self.name))

    def add_room_props(self):
        self.gd_input.add_prop("counter1", Counter(2, 2, "counter1", self.gc_input, self.gd_input, self.name))
        self.gd_input.add_prop("pink_dress_stand", Dress(5, 2, "pink_dress_stand", self.gc_input, self.gd_input, self.name, Spritesheet("assets/prop_sprites/pink_dress_stand.png", 32, 32)))
        self.gd_input.add_prop("green_dress_stand", Dress(6, 2, "green_dress_stand", self.gc_input, self.gd_input, self.name, Spritesheet("assets/prop_sprites/green_dress_stand.png", 32, 32)))
        self.gd_input.add_prop("blue_dress_stand", Dress(6, 3, "blue_dress_stand", self.gc_input, self.gd_input, self.name, Spritesheet("assets/prop_sprites/blue_dress_stand.png", 32, 32)))

class ToTheMoon(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)

        self.terrain_map = None
        self.obstacle_map = None

        self.name = "to_the_moon"
        self.room_width = 3
        self.room_height = 2
        self.left_edge_x = 1
        self.top_edge_y = 2

        self.right_edge_x = self.left_edge_x + self.room_width - 1
        self.bottom_edge_y = self.top_edge_y + self.room_height - 1

        self.map_style = "image"

        self.total_plots_x = 1
        self.total_plots_y = 1
        self.plot_size_x = int(self.room_width/self.total_plots_x)
        self.plot_size_y = int(self.room_height/self.total_plots_y)

    def add_room_and_plots(self):
        TTM_map = TileMap("assets/room_maps/to_the_moon_map.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list[self.name].add_room_plot("TTM_1_1", Plot("to_the_moon", 1, 1, TTM_map.return_map(), self.gc_input, self.gd_input, None))
        self.gd_input.room_list[self.name].activate_plot("TTM_1_1")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("to_the_moon_to_ringside", Door("to_the_moon", "Ringside", 2, 4, 41, 82, "to_the_moon_to_ringside"))

    def add_room_characters(self):
        self.gd_input.add_character("Guy1", GenericNPC(1, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40), "Guy1", self.name, "We've got a lil section by local authors", "stay_front", Facing.FRONT))

    def add_room_props(self):
        self.gd_input.add_prop("TTM_Bookcase_2", Bookcase(3, 2, "TTM_Bookcase_2", self.gc_input, self.gd_input, self.name))
        self.gd_input.add_prop("TTM_Bookcase_1", Bookcase(3, 3, "TTM_Bookcase_1", self.gc_input, self.gd_input, self.name))
        self.gd_input.add_prop("TTM_counter_1", Counter(1, 3, "TTM_counter_1", self.gc_input, self.gd_input, self.name))

class HornbyRealestate(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)

        self.terrain_map = None
        self.obstacle_map = None

        self.name = "hornby_realestate"
        self.room_width = 4
        self.room_height = 2
        self.left_edge_x = 1
        self.top_edge_y = 2

        self.right_edge_x = self.left_edge_x + self.room_width - 1
        self.bottom_edge_y = self.top_edge_y + self.room_height - 1

        self.map_style = "image"

        self.total_plots_x = 1
        self.total_plots_y = 1
        self.plot_size_x = int(self.room_width/self.total_plots_x)
        self.plot_size_y = int(self.room_height/self.total_plots_y)

    def add_room_and_plots(self):
        HR_map = TileMap("assets/room_maps/hornby_realestate_map.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list[self.name].add_room_plot("HR_1_1", Plot("hornby_realestate", 1, 1, HR_map.return_map(), self.gc_input, self.gd_input, None))
        self.gd_input.room_list[self.name].activate_plot("HR_1_1")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("hornby_realestate_to_ringside", Door("hornby_realestate", "Ringside", 1, 4, 39, 76, "hornby_realestate_to_ringside"))

    def add_room_characters(self):
        self.gd_input.add_character("Guy4", GenericNPC(2, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40), "Guy4", self.name, "Sorry, Jenessa's out for the day.", "stay_left", Facing.LEFT))
        self.gd_input.add_character("Guy5", GenericNPC(4, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40), "Guy5", self.name, "Sorry, Donna's out for the day.", "stay_front", Facing.FRONT))
    def add_room_props(self):
        self.gd_input.add_prop("HR_computer1", Computer(1, 2, "HR_computer1", self.gc_input, self.gd_input, self.name))
        self.gd_input.add_prop("HR_computer2", ComputerBack(4, 3, "HR_computer2", self.gc_input, self.gd_input, self.name))

class IslandPotters(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)

        self.terrain_map = None
        self.obstacle_map = None

        self.name = "island_potters"
        self.room_width = 5
        self.room_height = 2
        self.left_edge_x = 1
        self.top_edge_y = 2

        self.right_edge_x = self.left_edge_x + self.room_width - 1
        self.bottom_edge_y = self.top_edge_y + self.room_height - 1

        self.map_style = "image"

        self.total_plots_x = 1
        self.total_plots_y = 1
        self.plot_size_x = int(self.room_width/self.total_plots_x)
        self.plot_size_y = int(self.room_height/self.total_plots_y)

    def add_room_and_plots(self):
        IP_map = TileMap("assets/room_maps/island_potters_map.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list[self.name].add_room_plot("IP_1_1", Plot(self.name, 1, 1, IP_map.return_map(), self.gc_input, self.gd_input, None))
        self.gd_input.room_list[self.name].activate_plot("IP_1_1")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("island_potters_to_ringside_1", Door("island_potters", "Ringside", 2, 4, 39, 64, "island_potters_to_ringside_1"))
        self.gd_input.room_list[self.name].add_room_door("island_potters_to_ringside_2", Door("island_potters", "Ringside", 4, 4, 41, 64, "island_potters_to_ringside_2"))

    def add_room_characters(self):
        self.gd_input.add_character("IP_Guy1", GenericNPC(5, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40), "IP_Guy1", self.name, "I never understood this pottery stuff, now whittling, that I like", "stay_front", Facing.FRONT))

    def add_room_props(self):
        self.gd_input.add_prop("IP_counter_1", Counter(4, 2, "IP_counter_1", self.gc_input, self.gd_input, self.name))

class BikeShop(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)

        self.terrain_map = None
        self.obstacle_map = None

        self.name = "bike_shop"
        self.room_width = 4
        self.room_height = 5
        self.left_edge_x = 1
        self.top_edge_y = 2

        self.right_edge_x = self.left_edge_x + self.room_width - 1
        self.bottom_edge_y = self.top_edge_y + self.room_height - 1

        self.map_style = "image"

        self.total_plots_x = 1
        self.total_plots_y = 1
        self.plot_size_x = int(self.room_width/self.total_plots_x)
        self.plot_size_y = int(self.room_height/self.total_plots_y)

    def add_room_and_plots(self):
        BS_map = TileMap("assets/room_maps/bike_shop_map.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list[self.name].add_room_plot("BS_1_1", Plot(self.name, 1, 1, BS_map.return_map(), self.gc_input, self.gd_input, None))
        self.gd_input.room_list[self.name].activate_plot("BS_1_1")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("bike_shop_to_ringside", Door("bike_sho", "Ringside", 2, 7, 40, 92, "bike_shop_to_ringside"))

    def add_room_characters(self):
        self.gd_input.add_character("BS_Guy1", GenericNPC(2, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40), "BS_Guy1", self.name, "You don't look like you'd know how to ride a bike...", "stay_front", Facing.FRONT))


    def add_room_props(self):
        self.gd_input.add_prop("BS_counter_1", Counter(1, 3, "BS_counter_1", self.gc_input, self.gd_input, self.name))
        self.gd_input.add_prop("BS_counter_2", Counter(2, 3, "BS_counter_2", self.gc_input, self.gd_input, self.name))
