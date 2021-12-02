from random import randrange

import pygame, csv, os

from TileMap import TileMap
from features import GenericNPC, Spritesheet
from prop_page import GenericProp, Tree, Decoration
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

        self.terrain_map = None
        self.obstacle_map = None

    def add_room_plots(self, img, terrain_file):
        for plots_x in range(self.total_plots_x):
            for plots_y in range(self.total_plots_y):
                #print(plots_x + 1, plots_y + 1)
                print((self.name + "_" + str(plots_x+1) + "_" + str(plots_y+1)))
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
            print(self.name)

        if self.terrain_map is not None:
            self.gd_input.positioner[self.name].fill_terrain(self.terrain_map, self.name)
            print(self.name)

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
        self.gd_input.room_list[self.name].add_room_door("room1_door1", Door(self.name, "Coop", 2, 2, 1, 56, "room1_door1"))
        self.gd_input.room_list[self.name].add_room_door("room1_door2", Door(self.name, "room4", 5, 1, 2, 4, "room1_door2"))

    def add_room_characters(self):
        self.gd_input.add_character("Shuma", GenericNPC(2, 4, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Shuma.png", 32, 40), "Shuma", self.name, "Your dad have manure for sale? I'd really love to get my hands on a couple bags of it. It's great for the turnips and the kale! Though I think I might get some nitrogen fixed stuff from the co-op for the lettuce..."))
        self.gd_input.add_character("Maggie", GenericNPC(5, 5, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Maggie.png", 32, 40), "Maggie", self.name, "This outfit makes me feel really cool and powerful, so I've decided I'm going to wear it everywhere."))
        self.gd_input.add_character("Laurie", GenericNPC(4, 3, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Laurie.png", 32, 40), "Laurie", self.name, "Have you seen my drink anywhere?"))

    def add_room_props(self):
        self.gd_input.add_prop("trunk", GenericProp(3, 2, self.gc_input, self.gd_input, 32, 40, Spritesheet("assets/prop_sprites/trunk.png", 32, 40), "trunk", 1, 1, self.name))
        self.gd_input.add_prop("lamp", GenericProp(1, 5, self.gc_input, self.gd_input, 32, 40, Spritesheet("assets/prop_sprites/lamp.png", 32, 40), "lamp", 1, 1, self.name))

class Room2(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)

        self.terrain_map = "assets/csv_maps/room2.csv"
        self.obstacle_map = "assets/csv_maps/room2.csv"

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
        self.gd_input.room_list[self.name].add_room_plot("room2_1_1", Plot(self.name, 1, 1, TileMap("assets/csv_maps/csv_tiles/lake.csv", self.gd_input.tiles_img_dict).return_map(), self.gc_input, self.gd_input, "assets/csv_maps/room2.csv"))
        self.gd_input.room_list[self.name].activate_plot("room2_1_1")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("room2_door1", Door(self.name, "room1", 1, 14, 2, 3, "room2_door1"))
        self.gd_input.room_list[self.name].add_room_door("room2_door2", Door(self.name, "room3", 8, 12, 2, 4, "room2_door2"))
        self.gd_input.room_list[self.name].add_room_door("room2_door3", Door(self.name, "Coop", 13, 12, 1, 56, "room2_door3"))
        self.gd_input.room_list[self.name].add_room_door("room2_door4", Door(self.name, "room6", 14, 8, 7, 4, "room2_door4"))

    def add_room_characters(self):
        self.gd_input.add_character("Deb", GenericNPC(4, 4, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Deb.png", 32, 40), "Deb", self.name, "Hey Shuma, so nice to see you again!, I should probably be in the studio, but when I'm low on inspiration I like to come out here and walk by the water. "))
        self.gd_input.add_character("Alex", GenericNPC(9, 9, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/alex_lamont_CS.png", 32, 40), "Alex", self.name, "Hey Shuma, nice to see you! Stop by later and I'll sling you some free icecream! haha... I'm just kidding it's $5.00 a cone."))
        self.gd_input.add_character("Jamara", GenericNPC(6, 8, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Jamara_CS.png", 32, 40), "Jamara", self.name, "What do you think the greatest joy in life is? I haven't figured it out yet... I enjoy a whole lot of stuff, but I feel like nothing I've done so far is quite it."))
        self.gd_input.add_character("Donna", GenericNPC(3, 11, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Donna_Tuelle_CS.png", 32, 40), "Donna", self.name, "You know, Jennessa does such a good job, I'm almost considering retiring... not quite, but a very strong almost."))

    def add_room_props(self):
        self.gd_input.add_prop("house", GenericProp(5, 10, self.gc_input, self.gd_input, 160, 128, Spritesheet("assets/prop_sprites/House.png", 160, 128), "house", 5, 3, self.name))
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
        self.gd_input.add_character("Pixie", GenericNPC(2, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/sprite_sheet.png", 32, 40), "Pixie", "room3", "Hi!"))
        self.gd_input.add_character("Pixie_b", GenericNPC(3, 4, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/sprite2_sheet.png", 32, 40), "Pixie_b", "room3", "Hi!"))
        self.gd_input.add_character("Ian", GenericNPC(3, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Ian.png", 32, 40), "Ian", "room3", "Damnit, the cows got out again... If you see Kleyo can you ask her to give me a call? I should be back at the house by five."))

    def add_room_props(self):
        pass

class Room4(Room):
    def __init__(self, gc_input, gd_input):
            super().__init__(gc_input, gd_input)
            self.terrain_map = None
            self.obstacle_map = "assets/csv_maps/big_map.csv"

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
        big_map = TileMap("assets/csv_maps/csv_tiles/big_map2.0.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list[self.name].add_room_plot("room4_1_1", Plot(self.name, 1, 1, big_map.return_map(), self.gc_input, self.gd_input, "assets/csv_maps/big_map.csv"))
        self.gd_input.room_list[self.name].add_room_plot("room4_1_2", Plot(self.name, 2, 1, big_map.return_map(), self.gc_input, self.gd_input, "assets/csv_maps/big_map.csv"))
        self.gd_input.room_list[self.name].activate_plot("room4_1_1")
        self.gd_input.room_list[self.name].activate_plot("room4_1_2")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("room4_door1", Door(self.name, "room1", 2, 3, 5, 2, "room4_door1"))

    def add_room_characters(self):
        for name in range(50):
            rand_x = randrange(1, 100)
            rand_y = randrange(1, 50)
            self.gd_input.add_character(("Sheep" + str(name)), GenericNPC(rand_x, rand_y, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/sheep.png", 32, 40), ("Sheep" + str(name)), "room4", "Baaaahhhh"))

    def add_room_props(self):
        pass

class Room5(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.terrain_map = "assets/csv_maps/Coop_allowance.csv"
        self.obstacle_map = "assets/csv_maps/Coop_allowance.csv"

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
        coop_map = TileMap("assets/csv_maps/Co-op_area.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list["Coop"].add_room_plot("Coop_1_1", Plot("Coop", 1, 1, coop_map.return_map(), self.gc_input, self.gd_input, "assets/csv_maps/Coop_allowance.csv"))
        self.gd_input.room_list[self.name].activate_plot("Coop_1_1")

    def add_room_doors(self):
        self.gd_input.room_list["Coop"].add_room_door("Coop_door1", Door("Coop", "room2", 1, 57, 13, 11, "Coop_door1"))

    def add_room_characters(self):
        pass

    def add_room_props(self):
        self.gd_input.add_prop("Coop_Building", GenericProp(2, 2, self.gc_input, self.gd_input, 832, 1632, Spritesheet("assets/prop_sprites/Coop_Building.png", 832, 1632), "Coop_Building", 6, 3, self.name))
        self.gd_input.add_prop("Computer_Centre", GenericProp(25, 50, self.gc_input, self.gd_input, 192, 98, Spritesheet("assets/prop_sprites/computer_centre.png", 192, 128), "Computer_Centre", 6, 2, self.name))
        self.gd_input.add_prop("Hornby_Creative", GenericProp(25, 45, self.gc_input, self.gd_input, 192, 98, Spritesheet("assets/prop_sprites/hornby_creative.png", 192, 128), "Hornby_Creative", 6, 2, self.name))
        self.gd_input.add_prop("Island_Potters", GenericProp(25, 55, self.gc_input, self.gd_input, 160, 96, Spritesheet("assets/prop_sprites/island_potters.png", 160, 96), "Island_Potters", 5, 2, self.name))
        self.gd_input.add_prop("Lix", GenericProp(5, 52, self.gc_input, self.gd_input, (8*32), (5*32), Spritesheet("assets/prop_sprites/lix.png", (8*32), (5*32)), "Lix", 7, 3, self.name))


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
        room6_map = TileMap("assets/csv_maps/room6.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list[self.name].add_room_plot("room6_1_1", Plot("room6", 1, 1, room6_map.return_map(), self.gc_input, self.gd_input, None))
        self.gd_input.room_list[self.name].activate_plot("room6_1_1")
    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("room6_door1", Door(self.name, "room2", 7, 5, 14, 9, "room6_door1"))
    def add_room_characters(self):
        pass
    def add_room_props(self):
        pass