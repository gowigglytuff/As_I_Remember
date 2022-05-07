from TileMap import *
from features import *
from keyboards import *
from mapClasses import *
from prop_page import *


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
        self.gd_input.positioner_list[self.name].fill_tiles(self.name)
        self.gd_input.positioner_list[self.name].fill_doors(self.name)
        # activate the timers for animation and actions for the NPCs (make this apply to all that are in room)
        for character in self.gd_input.room_list[self.name].character_list:
            self.gd_input.character_list[character].activate_timers()

        #TODO: make this uses the plots csv instead of the rooms
        if self.obstacle_map is not None:
            self.gd_input.positioner_list[self.name].fill_obstacles(self.obstacle_map, self.name)


        if self.terrain_map is not None:
            self.gd_input.positioner_list[self.name].fill_terrain(self.terrain_map, self.name)


class Sandpiper(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.terrain_map = None
        self.obstacle_map = "assets/room_maps/sandpiper_fill_1_1.csv"

        self.name = "Sandpiper"
        self.room_width = 106
        self.room_height = 106
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
        sandpiper_map = TileMap("assets/room_maps/sandpiper_map_1_1.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list["Sandpiper"].add_room_plot("Sandpiper_1_1", Plot("Sandpiper_1_1", 1, 1, sandpiper_map.return_map(), self.gc_input, self.gd_input, "assets/room_maps/sandpiper_fill_1_1.csv"))
        self.gd_input.room_list[self.name].activate_plot("Sandpiper_1_1")

    def add_room_doors(self):
        pass

    def add_room_characters(self):
        self.gd_input.add_character("Ian_2", GenericNPC(70, 49, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Ian_CS.png", 32, 40), "Ian_2", self.name, "Where the heck is my house?", "stay_front", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/IanFace.png", 150, 150)))
        pass

    def add_room_props(self):
            # self.gd_input.add_prop(AppleTree.assign_dict_key(), AppleTree(38+55, 69, self.gc_input, self.gd_input, self.name))
            # self.gd_input.add_prop(PicnicTable.assign_dict_key(), PicnicTable(13+55, 69, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(StopSign.assign_dict_key(), StopSign(27, 72, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(PineTree.assign_dict_key(), PineTree(40, 20, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(SignPost.assign_dict_key(), SignPost(28, 14, self.gc_input, self.gd_input, self.name, "1025 Sandpipder Rd."))
            self.gd_input.add_prop(SignPost.assign_dict_key(), SignPost(72, 65, self.gc_input, self.gd_input, self.name, "1025 Sandpipder Rd."))
            self.gd_input.add_prop(SignPost.assign_dict_key(), SignPost(28, 82, self.gc_input, self.gd_input, self.name, "---- Sandpipder Rd."))
            self.gd_input.add_prop(SignPost.assign_dict_key(), SignPost(20, 29, self.gc_input, self.gd_input, self.name, "---- Sandpipder Rd."))
            self.gd_input.add_prop(SignPost.assign_dict_key(), SignPost(20, 6, self.gc_input, self.gd_input, self.name, "---- Sandpipder Rd."))
            self.gd_input.add_prop(SignPost.assign_dict_key(), SignPost(28, 6, self.gc_input, self.gd_input, self.name, "---- Sandpipder Rd."))
            self.gd_input.add_prop(SignPost.assign_dict_key(), SignPost(92, 65, self.gc_input, self.gd_input, self.name, "---- Sandpipder Rd."))

class Ringside(Room):
    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.terrain_map = None
        self.obstacle_map = None

        self.name = "Ringside"
        self.room_width = 55* 2
        self.room_height = 106
        self.left_edge_x = 1
        self.top_edge_y = 1

        self.right_edge_x = self.left_edge_x + self.room_width - 1
        self.bottom_edge_y = self.top_edge_y + self.room_height - 1

        self.map_style = "image"

        self.total_plots_x = 2
        self.total_plots_y = 1
        self.plot_size_x = int(self.room_width / self.total_plots_x)
        self.plot_size_y = int(self.room_height / self.total_plots_y)

    def add_room_and_plots(self):
        ringside_map = TileMap("assets/room_maps/ringside_map_1_1.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list["Ringside"].add_room_plot("Ringside_1_1", Plot("Coop", 1, 1, ringside_map.return_map(), self.gc_input, self.gd_input, "assets/room_maps/ringside_map_1_1.csv"))
        self.gd_input.room_list[self.name].activate_plot("Ringside_1_1")

        ringside_map_2 = TileMap("assets/room_maps/ringside_map_tester.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list[self.name].add_room_plot("Ringside_1_2", Plot("Coop", 2, 1, ringside_map_2.return_map(), self.gc_input, self.gd_input, "assets/room_maps/ringside_map_tester.csv"))
        self.gd_input.room_list[self.name].activate_plot("Ringside_1_2")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("ringside_to_computer_centre", Door("Ringside", "computer_centre", 11+55, 84, 3, 3, "ringside_to_computer_centre", [Direction.UP]))
        self.gd_input.room_list[self.name].add_room_door("ringside_to_hornby_creative", Door("Ringside", "hornby_creative", 12+55, 76, 4, 3, "ringside_to_hornby_creative", [Direction.UP]))
        self.gd_input.room_list[self.name].add_room_door("ringside_to_to_the_moon", Door("Ringside", "to_the_moon", 41+55, 81, 2, 3, "ringside_to_to_the_moon", [Direction.UP]))
        self.gd_input.room_list[self.name].add_room_door("ringside_to_hornby_realestate", Door("Ringside", "hornby_realestate", 39+55, 75, 1, 3, "ringside_to_hornby_realestate", [Direction.UP]))
        self.gd_input.room_list[self.name].add_room_door("ringside_to_island_potters_1", Door("Ringside", "island_potters", 39+55, 63, 2, 3,  "ringside_to_island_potters_1", [Direction.UP]))
        self.gd_input.room_list[self.name].add_room_door("ringside_to_island_potters_2", Door("Ringside", "island_potters", 41+55, 63, 4, 3, "ringside_to_island_potters_2", [Direction.UP]))
        self.gd_input.room_list[self.name].add_room_door("ringside_to_bike_shop", Door("Ringside", "bike_shop", 40+55, 91, 2, 6, "ringside_to_bike_shop", [Direction.UP]))

    def add_room_characters(self):
        self.gd_input.add_character("Deb", GenericNPC(30+55, 76, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Deb_CS.png", 32, 40), "Deb", self.name, "Something strange is going on around here, have you heard about the children disapearing? Their parents couldn't even remember their names...", "stay_left", Direction.LEFT, Spritesheet("assets/NPC_sprites/faces/DebFace.png", 150, 150)))
        self.gd_input.add_character("Alex", GenericNPC(17+55, 70, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/alex_lamont_CS.png", 32, 40), "Alex", self.name, "Hey Shuma, I feel like I haven't seen you in a long time... but didn't we just go to the beach togther on Friday? I seem to be losing track of time so much recently...", "square", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/AlexFace.png", 150, 150)))
        self.gd_input.add_character("Jamara", GenericNPC(31+55, 90, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Jamara_CS.png", 32, 40), "Jamara", self.name, "What do you think the greatest joy in life is? I haven't figured it out yet... I enjoy a whole lot of stuff, but I feel like nothing I've done so far is quite it.", "pace", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/JamaraFace.png", 150, 150)))
        self.gd_input.add_character("Donna", GenericNPC(39+55, 78, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Donna_Tuelle_CS.png", 32, 40), "Donna", self.name, "You know, it's the strangest thing, my daughter Alex showed up the other day to ask me to watch her kids... but I don't remember having grandkids. I watched them anyway, but I swear I've never met them...", "left_right", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/DonnaFace.png", 150, 150)))
        self.gd_input.add_character("Clair", GenericNPC(30+55, 60, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Clair_CS.png", 32, 40), "Clair", self.name, "I love this place but sometimes I feel like I should just pack everything up and run far away...", "square", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/ClairFace.png", 150, 150)))
        self.gd_input.add_character("Clayton", GenericNPC(23+55, 72, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Clayton_CS.png", 32, 40), "Clayton", self.name, "Nyah! Why is everybody on this island so weird?? And have you seen the cost of icecream??? Of all the days to forget my boomerang at home...", "spin", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/ClaytonFace.png", 150, 150)))
        self.gd_input.add_character("Marilyn", GenericNPC(29+55, 76, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Marilyn_CS.png", 32, 40), "Marilyn", self.name, "Have you seen my son around? He's always running off and getting up to mischief", "stay_right", Direction.RIGHT, Spritesheet("assets/NPC_sprites/faces/MarilynFace.png", 150, 150)))
        self.gd_input.add_character("Maggie", GenericNPC(21+55, 82, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Maggie.png", 32, 40), "Maggie", self.name, "This outfit makes me feel really cool and powerful, so I've decided I'm going to wear it everywhere.", "stand_still", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/MaggieFace.png", 150, 150)))
        self.gd_input.add_character("Laurie", GenericNPC(32+55, 101, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Laurie.png", 32, 40), "Laurie", self.name, "Have you seen my drink anywhere?", "square", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/LaurieFace.png", 150, 150)))
        self.gd_input.add_character("Ian", GenericNPC(23+55, 59, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Ian_CS.png", 32, 40), "Ian", self.name, "Shoot, I left my wallet in the farm truck, guess I'll be paying in charm again...", "stay_front", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/IanFace.png", 150, 150)))
        self.gd_input.add_character("Grandma", GameMaster(28+55, 70, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Grandma_CS.png", 32, 40), "Grandma", self.name, "Hi squirt, how's it going?", "stay_front", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/GrandmaFace.png", 150, 150)))

    def add_room_props(self):
            self.gd_input.add_prop("Coop_Building", Building(10+55, 8, self.gc_input, self.gd_input, 832, 1632, "assets/prop_sprites/Buildings/Coop_Building.png", "Coop_Building", 26, 51, self.name, "assets/prop_sprites/Buildings/building_csv/coop_fill_csv.csv"))
            self.gd_input.add_prop("Computer_Centre", Building(9+55, 82, self.gc_input, self.gd_input, 192, 128, "assets/prop_sprites/Buildings/computer_centre.png", "Computer_Centre", 6, 4, self.name, "assets/prop_sprites/Buildings/building_csv/computer_centre_fill_map.csv"))
            self.gd_input.add_prop("Hornby_Creative", Building(9+55, 74, self.gc_input, self.gd_input, 192, 128, "assets/prop_sprites/Buildings/hornby_creative.png", "Hornby_Creative", 6, 4, self.name, "assets/prop_sprites/Buildings/building_csv/hornby_creative_fill_map.csv"))
            self.gd_input.add_prop("Island_Potters", Building(38+55, 61, self.gc_input, self.gd_input, 160, 96, "assets/prop_sprites/Buildings/island_potters.png", "Island_Potters", 5, 3, self.name, "assets/prop_sprites/Buildings/building_csv/island_potters_fill_map.csv"))
            self.gd_input.add_prop("Lix", Building(15+55, 63, self.gc_input, self.gd_input, (8 * 32), (5 * 32), "assets/prop_sprites/Buildings/lix.png", "Lix", 8, 5, self.name, "assets/prop_sprites/Buildings/building_csv/lix_fill_map.csv"))
            self.gd_input.add_prop("Real_Estate", Building(38+55, 72, self.gc_input, self.gd_input, (5 * 32), (5 * 32), "assets/prop_sprites/Buildings/real_estate_2.png", "Real_Estate", 5, 5, self.name, "assets/prop_sprites/Buildings/building_csv/real_estate_csv.csv"))
            self.gd_input.add_prop("To_The_Moon", Building(39+55, 78, self.gc_input, self.gd_input, (5 * 32), (5 * 32), "assets/prop_sprites/Buildings/to_the_moon.png", "To_The_Moon", 5, 5, self.name, "assets/prop_sprites/Buildings/building_csv/to_the_moon_fill_map.csv"))
            self.gd_input.add_prop("Fibres", Building(31+55, 60, self.gc_input, self.gd_input, (5 * 32), (5 * 32), "assets/prop_sprites/Buildings/Fibres.png", "Fibres", 5, 5, self.name, "assets/prop_sprites/Buildings/building_csv/fibres_fill_map.csv"))
            self.gd_input.add_prop("Vorizo", Building(27+55, 93, self.gc_input, self.gd_input, (3 * 32), (3 * 32), "assets/prop_sprites/Buildings/vorizo.png", "Vorizo", 3, 3, self.name, "assets/prop_sprites/Buildings/building_csv/vorizo_fill_map.csv"))
            self.gd_input.add_prop("Bike_Shop", Building(39+55, 85, self.gc_input, self.gd_input, (4 * 32), (7 * 32), "assets/prop_sprites/Buildings/bike_shop.png", "Bike_Shop", 4, 7, self.name, "assets/prop_sprites/Buildings/building_csv/bike_shop_fill_map.csv"))

            self.gd_input.add_prop(AppleTree.assign_dict_key(), AppleTree(38+55, 69, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(BenchHorizontal.assign_dict_key(), BenchHorizontal(28+55, 78, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(BenchHorizontal.assign_dict_key(), BenchHorizontal(29+55, 70, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(BenchVertical.assign_dict_key(), BenchVertical(26+55, 73, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(BenchVertical.assign_dict_key(), BenchVertical(33+55, 73, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(BenchVertical.assign_dict_key(), BenchVertical(22+55, 69, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(BenchVertical.assign_dict_key(), BenchVertical(21+55, 79, self.gc_input, self.gd_input, self.name))

            self.gd_input.add_prop(BenchVertical.assign_dict_key(), BenchVertical(26+55, 84, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(BenchVertical.assign_dict_key(), BenchVertical(32+55, 84, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(BenchVertical.assign_dict_key(), BenchVertical(26+55, 87, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(BenchVertical.assign_dict_key(), BenchVertical(32+55, 87, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(BenchHorizontal.assign_dict_key(), BenchHorizontal(26+55, 83, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(BenchHorizontal.assign_dict_key(), BenchHorizontal(29+55, 83, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(BenchHorizontal.assign_dict_key(), BenchHorizontal(27+55, 89, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(LargeStone.assign_dict_key(), LargeStone(31+55, 89, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(LargeStone.assign_dict_key(), LargeStone(30+55, 89, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(LargeStone.assign_dict_key(), LargeStone(41+55, 83, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(Planter.assign_dict_key(), Planter(32+55,77, self.gc_input, self.gd_input, self.name))

            #self.gd_input.add_prop(Tree.assign_dict_key(), Tree(37, 69, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(PlumTree.assign_dict_key(), PlumTree(29+55, 74, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(BenchHorizontal.assign_dict_key(), BenchHorizontal(37+55, 70, self.gc_input, self.gd_input, self.name))

            self.gd_input.add_prop(PicnicTable.assign_dict_key(), PicnicTable(17+55, 82, self.gc_input, self.gd_input, self.name))

            self.gd_input.add_prop(PicnicTable.assign_dict_key(), PicnicTable(9+55, 65, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(PicnicTable.assign_dict_key(), PicnicTable(9+55, 69, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(PicnicTable.assign_dict_key(), PicnicTable(13+55, 65, self.gc_input, self.gd_input, self.name))
            self.gd_input.add_prop(PicnicTable.assign_dict_key(), PicnicTable(13+55, 69, self.gc_input, self.gd_input, self.name))


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
        self.gd_input.room_list[self.name].add_room_door("computer_centre_to_ringside", Door("computer_centre", "Ringside",  3, 4, 11+55, 85, "computer_centre_to_ringside", [Direction.DOWN]))

    def add_room_characters(self):
        self.gd_input.add_character("CC_Guy2", GenericNPC(2, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40), "CC_Guy2", self.name, "You have such strange customs here, what in the world is a yurt?", "stay_left", Direction.LEFT, Spritesheet("assets/NPC_sprites/faces/NeutralFace.png", 150, 150)))
        self.gd_input.add_character("CC_Guy3", GenericNPC(4, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40), "CC_Guy3", self.name, "Leave me alone human!.. I mean... dude", "stay_left", Direction.LEFT, Spritesheet("assets/NPC_sprites/faces/NeutralFace.png", 150, 150)))
        self.gd_input.add_character("CC_Guy1", GenericNPC(6, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40), "CC_Guy1", self.name, "Do you know what this strange box is?", "stay_front", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/NeutralFace.png", 150, 150)))

    def add_room_props(self):
        self.gd_input.add_prop(ComputerRight.assign_dict_key(), ComputerRight(3, 2, self.gc_input, self.gd_input, "computer_centre"))
        self.gd_input.add_prop(ComputerRight.assign_dict_key(), ComputerRight(1, 2, self.gc_input, self.gd_input, "computer_centre"))
        self.gd_input.add_prop(ComputerBack.assign_dict_key(), ComputerBack(6, 3, self.gc_input, self.gd_input, "computer_centre"))


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
        self.gd_input.room_list[self.name].add_room_door("hornby_creative_to_ringside", Door("hornby_creative", "Ringside", 4, 4, 12+55, 77, "hornby_creative_to_ringside", [Direction.DOWN]))

    def add_room_characters(self):
        self.gd_input.add_character("Tamma", ShopKeeperTamma(1, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Tamma_CS.png", 32, 40), "Tamma", self.name, "Hi, welcome to my store, what would you like to do?", "stay_front", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/TammaFace.png", 150, 150)))

    def add_room_props(self):
        self.gd_input.add_prop(Counter.assign_dict_key(), Counter(2, 2, self.gc_input, self.gd_input, self.name))
        self.gd_input.add_prop(Dress.assign_dict_key(), Dress(5, 2, self.gc_input, self.gd_input, self.name, "assets/prop_sprites/pink_dress_stand.png"))
        self.gd_input.add_prop(Dress.assign_dict_key(), Dress(6, 2, self.gc_input, self.gd_input, self.name, "assets/prop_sprites/green_dress_stand.png"))
        self.gd_input.add_prop(Dress.assign_dict_key(), Dress(6, 3, self.gc_input, self.gd_input, self.name, "assets/prop_sprites/blue_dress_stand.png"))


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
        self.gd_input.room_list[self.name].add_room_door("to_the_moon_to_ringside", Door("to_the_moon", "Ringside", 2, 4, 41+55, 82, "to_the_moon_to_ringside", [Direction.DOWN]))

    def add_room_characters(self):
        self.gd_input.add_character("Cheryl", ShopKeeperCheryl(1, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/cheryl_muir_CS.png", 32, 40), "Cheryl", self.name, "Hi, welcome to my store, what would you like to do?", "stay_front", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/CherylFace.png", 150, 150)))

    def add_room_props(self):
        self.gd_input.add_prop(Bookcase.assign_dict_key(), Bookcase(3, 2, self.gc_input, self.gd_input, self.name))
        self.gd_input.add_prop(Bookcase.assign_dict_key(), Bookcase(3, 3, self.gc_input, self.gd_input, self.name))
        self.gd_input.add_prop(Counter.assign_dict_key(), Counter(1, 3, self.gc_input, self.gd_input, self.name))


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
        self.gd_input.room_list[self.name].add_room_door("hornby_realestate_to_ringside", Door("hornby_realestate", "Ringside", 1, 4, 39+55, 76, "hornby_realestate_to_ringside", [Direction.DOWN]))

    def add_room_characters(self):
        self.gd_input.add_character("Guy4", GenericNPC(2, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40), "Guy4", self.name, "Sorry, Jenessa's out for the day.", "stay_left", Direction.LEFT, Spritesheet("assets/NPC_sprites/faces/NeutralFace.png", 150, 150)))
        self.gd_input.add_character("Guy5", GenericNPC(4, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40), "Guy5", self.name, "Sorry, Donna's out for the day.", "stay_front", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/NeutralFace.png", 150, 150)))
    def add_room_props(self):
        self.gd_input.add_prop(ComputerRight.assign_dict_key(), ComputerRight(1, 2, self.gc_input, self.gd_input, self.name))
        self.gd_input.add_prop(ComputerBack.assign_dict_key(), ComputerBack(4, 3, self.gc_input, self.gd_input, self.name))


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
        self.gd_input.room_list[self.name].add_room_door("island_potters_to_ringside_1", Door("island_potters", "Ringside", 2, 4, 39+55, 64, "island_potters_to_ringside_1", [Direction.DOWN]))
        self.gd_input.room_list[self.name].add_room_door("island_potters_to_ringside_2", Door("island_potters", "Ringside", 4, 4, 41+55, 64, "island_potters_to_ringside_2", [Direction.DOWN]))

    def add_room_characters(self):
        self.gd_input.add_character("IP_Guy1", GenericNPC(5, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40), "IP_Guy1", self.name, "I never understood this pottery stuff, now whittling, that I like", "stay_front", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/NeutralFace.png", 150, 150)))

    def add_room_props(self):
        self.gd_input.add_prop(Counter.assign_dict_key(), Counter(4, 2, self.gc_input, self.gd_input, self.name))


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
        self.gd_input.room_list[self.name].add_room_door("bike_shop_to_ringside", Door("bike_sho", "Ringside", 2, 7, 40+55, 92, "bike_shop_to_ringside", [Direction.DOWN]))

    def add_room_characters(self):
        self.gd_input.add_character("BS_Guy1", GenericNPC(2, 2, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40), "BS_Guy1", self.name, "You don't look like you'd know how to ride a bike...", "stay_front", Direction.DOWN, Spritesheet("assets/NPC_sprites/faces/NeutralFace.png", 150, 150)))


    def add_room_props(self):
        self.gd_input.add_prop(Counter.assign_dict_key(), Counter(1, 3, self.gc_input, self.gd_input, self.name))
        self.gd_input.add_prop(Counter.assign_dict_key(), Counter(2, 3, self.gc_input, self.gd_input, self.name))
