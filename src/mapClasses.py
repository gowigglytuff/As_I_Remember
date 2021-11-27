from random import randrange

import pygame, csv, os

from TileMap import TileMap
from features import GenericNPC, Spritesheet, GenericProp, Tree, Decoration
from keyboards import Direction, Facing


class Room(object):
    def __init__(self, name, left_edge_x, top_edge_y, room_width, room_height, total_plots_x, total_plots_y, gc_input, gd_input, map_style="image"):
        self.gc_input = gc_input
        self.gd_input = gd_input

        self.name = name
        self.left_edge_x = left_edge_x
        self.right_edge_x = left_edge_x + room_width - 1
        self.top_edge_y = top_edge_y
        self.bottom_edge_y = top_edge_y + room_height - 1
        self.room_width = room_width
        self.room_height = room_height
        self.map_style = map_style

        self.plot_list = {}
        self.total_plots_x = total_plots_x
        self.total_plots_y = total_plots_y
        self.plot_size_x = int(room_width/total_plots_x)
        self.plot_size_y = int(room_height/total_plots_y)
        self.active_plots = []

        self.tiles_array = []
        self.active_tiles = []

        self.door_list = {}
        self.character_list = []
        self.decoration_list = []
        self.prop_list = []

    def compose_room(self):
        self.gd_input.room_list[self.name].generate_room_grid()

        #self.gd_input.add_positioner(self.name, Position_Manager(self.name, self.gc_input, self.gd_input))

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

class Room1(Room):
    def __init__(self, name, left_edge_x, top_edge_y, room_width, room_height, total_plots_x, total_plots_y, gc_input, gd_input, map_style="image"):
        super().__init__(name, left_edge_x, top_edge_y, room_width, room_height, total_plots_x, total_plots_y, gc_input, gd_input, map_style="image")

    def add_room_and_plots(self):
        self.gd_input.room_list[self.name].add_room_plot("room1_1_1", Plot("room1", 1, 1, pygame.image.load("assets/backgrounds/room_1_background.png"), self.gc_input, self.gd_input, None))
        self.gd_input.room_list[self.name].activate_plot("room1_1_1")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("room1_door1", Door(self.name, "room2", 2, 2, 1, 15, "room1_door1"))
        self.gd_input.room_list[self.name].add_room_door("room1_door2", Door(self.name, "room4", 5, 1, 2, 4, "room1_door2"))

    def add_room_characters(self):
        self.gd_input.add_character("Shuma", GenericNPC(2, 4, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Shuma.png", 32, 40), "Shuma", self.name, "Your dad have manure for sale? I'd really love to get my hands on a couple bags of it. It's great for the turnips and the kale! Though I think I might get some nitrogen fixed stuff from the co-op for the lettuce..."))
        self.gd_input.add_character("Maggie", GenericNPC(5, 5, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Maggie.png", 32, 40), "Maggie", self.name, "This outfit makes me feel really cool and powerful, so I've decided I'm going to wear it everywhere."))
        self.gd_input.add_character("Laurie", GenericNPC(4, 3, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Laurie.png", 32, 40), "Laurie", self.name, "Have you seen my drink anywhere?"))

    def add_room_props(self):
        self.gd_input.add_prop("trunk", GenericProp(3, 2, self.gc_input, self.gd_input, 32, 40, Spritesheet("assets/prop_sprites/trunk.png", 32, 40), "trunk", 1, 1, self.name))
        self.gd_input.add_prop("lamp", GenericProp(1, 5, self.gc_input, self.gd_input, 32, 40, Spritesheet("assets/prop_sprites/lamp.png", 32, 40), "lamp", 1, 1, self.name))

class Room2(Room):
    def add_room_and_plots(self):
        self.gd_input.room_list[self.name].add_room_plot("room2_1_1", Plot(self.name, 1, 1, TileMap("assets/csv_maps/csv_tiles/lake.csv", self.gd_input.tiles_img_dict).return_map(), self.gc_input, self.gd_input, "assets/csv_maps/room2.csv"))
        self.gd_input.room_list[self.name].activate_plot("room2_1_1")

    def add_room_doors(self):
        self.gd_input.room_list[self.name].add_room_door("room2_door1", Door(self.name, "room1", 1, 14, 2, 3, "room2_door1"))
        self.gd_input.room_list[self.name].add_room_door("room2_door2", Door(self.name, "room3", 8, 12, 2, 4, "room2_door2"))
        self.gd_input.room_list[self.name].add_room_door("room2_door3", Door(self.name, "Coop", 13, 12, 1, 56, "room2_door3"))

    def add_room_characters(self):
        self.gd_input.add_character("Deb", GenericNPC(4, 4, self.gc_input, self.gd_input, Spritesheet("assets/NPC_sprites/Deb.png", 32, 40), "Deb", self.name, "Hey Shuma, so nice to see you again!, I should probably be in the studio, but when I'm low on inspiration I like to come out here and walk by the water. "))

    def add_room_props(self):
        self.gd_input.add_prop("house", GenericProp(5, 10, self.gc_input, self.gd_input, 160, 128, Spritesheet("assets/prop_sprites/House.png", 160, 128), "house", 5, 3, self.name))
        self.gd_input.add_prop("tree1", Tree(3, 6, "tree1", self.gc_input, self.gd_input, self.name))
        self.gd_input.add_prop("tree2", Tree(6, 6, "tree2", self.gc_input, self.gd_input, self.name))
        self.gd_input.add_prop("tree3", Tree(9, 6, "tree3", self.gc_input, self.gd_input, self.name))

        self.gd_input.add_decoration("Grass", Decoration(0, 0, self.gc_input, self.gd_input, 32, 32, Spritesheet("assets/decoration_sprites/grass5.png", 32, 32), "Grass", 1, 1, [[2, 11], [2, 12], [2, 13], [2, 14], [3, 11], [3, 12], [3, 13], [3, 14]], self.name))

class Room3(Room):

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
    def add_room_and_plots(self):
        coop_map = TileMap("assets/csv_maps/Co-op_area.csv", self.gd_input.tiles_img_dict)
        self.gd_input.room_list["Coop"].add_room_plot("Coop_1_1", Plot("Coop", 1, 1, coop_map.return_map(), self.gc_input, self.gd_input, "assets/csv_maps/Co-op_area.csv"))
        self.gd_input.room_list[self.name].activate_plot("Coop_1_1")
    def add_room_doors(self):
        self.gd_input.room_list["Coop"].add_room_door("Coop_door1", Door("Coop", "room2", 1, 57, 13, 11, "Coop_door1"))
        pass
    def add_room_characters(self):
        pass
    def add_room_props(self):
        self.gd_input.add_prop("Coop_Building", GenericProp(2, 2, self.gc_input, self.gd_input, 832, 1632, Spritesheet("assets/prop_sprites/Coop_Building.png", 832, 1632), "Coop_Building", 6, 3, self.name))


class Plot(object):
    '''
    each room will be made up of a specified number of plots
    '''
    def __init__(self, room, plot_x, plot_y, plot_img, GameController, GameData, terrain_csv_file):
        self.GameController = GameController
        self.GameData = GameData

        self.room = room
        self.plot_x = plot_x
        self.plot_y = plot_y
        self.name = self.room + "_" + str(plot_x) + "_"+ str(plot_y)
        self.plot_img = plot_img
        self.terrain_csv_file = terrain_csv_file
        self.prop_list = []
        self.character_list = []
        self.decoration_list = []


class Tile(object):

    DOOR = "Door"
    NPC = "NPC"
    PIXIE = "Pixie"
    PLAYER = "Player"
    NONE = "None"
    PROP = "Prop"
    OBSTACLE = "Obstacle"
    TILE_TYPE_LIST = [DOOR, NPC, PLAYER, PIXIE, PROP, NONE, OBSTACLE]

    def __init__(self, x, y, full, object_filling, filling_type, item=None):
        assert filling_type in self.TILE_TYPE_LIST
        self.x = x
        self.y = y
        self.full = full
        self.object_filling = object_filling
        self.filling_type = filling_type
        self.item = item
        self.name = "tile" + str(x) + "_" + str(y)
        self.elevation = 1
        self.terrain = None


class Door(object):
    def __init__(self, room_from, room_to, x, y, exit_x, exit_y, name):
        self.room_from = room_from
        self.room_to = room_to
        self.x = x
        self.y = y
        self.exit_x = exit_x
        self.exit_y = exit_y
        self.name = name

class BG(object):
    def __init__(self, x, y, name, img_file_name_list, GameController, GameData):
        self.x = x
        self.y = y
        self.img_file_name_list = img_file_name_list
        self.img_list = [file_name for file_name in
                        img_file_name_list]

        self.cur_img = 0
        self.img = self.img_list[self.cur_img]
        self.name = name
        self.GameController = GameController
        self.GameData = GameData

    def draw(self, screen):
        screen.blit(self.img,
                    (((self.x + self.GameController.camera[0]) * self.GameData.square_size[0]) + self.GameData.base_locator_x,
                    ((self.y + self.GameController.camera[1]) * self.GameData.square_size[1]) + self.GameData.base_locator_y))


class Position_Manager(object):
    def __init__(self, name, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData
        self.name = name

    def fill_tiles(self, fillable_room):
        for tile_list in self.GameData.room_list[fillable_room].tiles_array:
            for tile in tile_list:
                drawable_list = self.GameController.get_current_drawables(fillable_room)
                for drawable in drawable_list:
                    if drawable.feature_type == "Prop" and drawable.x == tile.x and drawable.y == tile.y:
                        for size_x in range(drawable.size_x):
                            for size_y in range(drawable.size_y):
                                    self.GameData.room_list[fillable_room].tiles_array[drawable.x + size_x][drawable.y + size_y].object_filling = drawable.name
                                    self.GameData.room_list[fillable_room].tiles_array[drawable.x + size_x][drawable.y + size_y].filling_type = drawable.feature_type
                                    self.GameData.room_list[fillable_room].tiles_array[drawable.x + size_x][drawable.y + size_y].full = True

                    elif drawable.feature_type != "Prop" and drawable.x == tile.x and drawable.y == tile.y:
                        tile.object_filling = drawable.name
                        tile.filling_type = drawable.feature_type
                        tile.full = True

    # TODO make the obstacles have types, water, trees, etc.
    def fill_obstacles(self, filename, fillable_room):
        for plot in self.GameData.room_list[fillable_room].active_plots:
            current_plot = self.GameData.room_list[fillable_room].plot_list[plot]
            map = self.read_csv(filename)
            x, y = (current_plot.plot_x-1) * self.GameData.room_list[fillable_room].plot_size_x, (current_plot.plot_y-1) * self.GameData.room_list[fillable_room].plot_size_y
            for row in map:
                x = (current_plot.plot_x-1) * self.GameData.room_list[fillable_room].plot_size_x
                for tile in row:
                    if tile == "0":
                        pass
                    elif tile == "1":
                        filling_tile = self.GameData.room_list[fillable_room].tiles_array[x+1][y+1]
                        filling_tile.object_filling = "Obstacle"
                        filling_tile.filling_type = "Obstacle"
                        filling_tile.full = True
                    x += 1
                y += 1

    def fill_terrain(self, filename, fillable_room):
        for plot in self.GameData.room_list[fillable_room].active_plots:
            current_plot = self.GameData.room_list[fillable_room].plot_list[plot]
            map = self.read_csv(filename)
            x, y = (current_plot.plot_x-1) * self.GameData.room_list[fillable_room].plot_size_x, (current_plot.plot_y-1) * self.GameData.room_list[fillable_room].plot_size_y

            for row in map:
                x = (current_plot.plot_x-1) * self.GameData.room_list[fillable_room].plot_size_x
                for tile in row:
                    if tile == "0":
                        filling_tile = self.GameData.room_list[fillable_room].tiles_array[x + 1][y + 1]
                        filling_tile.terrain = "Ground"
                    elif tile == "1":
                        filling_tile = self.GameData.room_list[fillable_room].tiles_array[x + 1][y + 1]
                        filling_tile.terrain = "Water"

                    elif tile == "3":
                        filling_tile = self.GameData.room_list[fillable_room].tiles_array[x + 1][y + 1]
                        filling_tile.terrain = "Floor"
                    x += 1
                y += 1

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def fill_doors(self, fillable_room):
        for tile_list in self.GameData.room_list[fillable_room].tiles_array:
            for tile in tile_list:
                for door in self.GameData.room_list[fillable_room].door_list:
                    if self.GameData.room_list[fillable_room].door_list[door].x == tile.x and self.GameData.room_list[fillable_room].door_list[door].y == tile.y:
                        tile.object_filling = self.GameData.room_list[fillable_room].door_list[door].name
                        tile.filling_type = "Door"
                        tile.full = True

    def through_door(self, door):
        self.empty_tile(self.GameData.player["Player"])
        x_change = self.GameData.player["Player"].x - door.exit_x
        y_change = self.GameData.player["Player"].y - door.exit_y
        self.GameData.player["Player"].turn_player(Direction.DOWN)
        self.GameData.player["Player"].x = door.exit_x
        self.GameData.player["Player"].y = door.exit_y
        self.GameController.camera[0] += x_change
        self.GameController.camera[1] += y_change
        self.GameController.set_room(door.room_to)
        self.empty_tiles(door.room_to)
        #TODO: Make all maps in CSV Style?
        if self.GameData.room_list[door.room_to].map_style == "csv":
            for plot in self.GameData.room_list[door.room_to].plot_list:
                self.fill_obstacles(self.GameData.room_list[door.room_to].plot_list[plot].terrain_csv_file, door.room_to)
        self.fill_tiles(door.room_to)
        self.fill_doors(door.room_to)
        self.fill_tile(self.GameData.player["Player"])
        self.GameController.current_keyboard_manager.current_direction_key = None
        self.GameData.player["Player"].set_state("idle")


    def empty_tiles(self, fillable_room):
        #FIXME: dum dum
        for tile_list in self.GameData.room_list[fillable_room].tiles_array:
            for tile in tile_list:
                tile.object_filling = "None"
                tile.filling_type = "None"
                tile.full = False

    def can_move_NPC(self, mover):
        move = False
        facing_tile = mover.get_facing_tile()
        if mover.facing == Facing.LEFT:
            if mover.x <= self.GameData.room_list[self.GameController.current_room].left_edge_x:
                move = False
            else:
                if not facing_tile.full:
                    move = True
                else:
                    move = False
        elif mover.facing == Facing.RIGHT:
            if mover.x >= self.GameData.room_list[self.GameController.current_room].right_edge_x:
                move = False
            else:
                if not facing_tile.full:
                    move = True
                else:
                    move = False
        elif mover.facing == Facing.FRONT:
            if mover.y >= self.GameData.room_list[self.GameController.current_room].bottom_edge_y:
                move = False
            else:
                if not facing_tile.full:
                    move = True
                else:
                    move = False
        if mover.facing == Facing.BACK:
            if mover.y <= self.GameData.room_list[self.GameController.current_room].top_edge_y:
                move = False
            else:
                if not facing_tile.full:
                    move = True
                else:
                    move = False

        return move

    def check_adj_square_full(self, mover, direction):
        full = False
        check_tile = mover.check_adj_tile(direction)
        if direction == Direction.LEFT:
            if mover.x <= self.GameData.room_list[self.GameController.current_room].left_edge_x:
                full = False
            else:
                if not check_tile.full:
                    full = True
                else:
                    full = False
        elif direction == Direction.RIGHT:
            if mover.x >= self.GameData.room_list[self.GameController.current_room].right_edge_x:
                full = False
            else:
                if not check_tile.full:
                    full = True
                else:
                    full = False
        elif direction == Direction.DOWN:
            if mover.y >= self.GameData.room_list[self.GameController.current_room].bottom_edge_y:
                full = False
            else:
                if not check_tile.full:
                    full = True
                else:
                    full = False
        if direction == Direction.UP:
            if mover.y <= self.GameData.room_list[self.GameController.current_room].top_edge_y:
                full = False
            else:
                if not check_tile.full:
                    full = True
                else:
                    full = False
        #print(str(direction) + str(full))
        return full

    def check_door(self, mover, direction):
        self.direction = direction
        is_door = False
        facing_tile = mover.check_adj_tile(self.direction)
        if facing_tile.filling_type == "Door":
            is_door = True
        else:
            is_door = False
        return is_door

    def empty_tile(self, mover):
        self.GameData.room_list[self.GameController.current_room].tiles_array[mover.x][mover.y].full = False
        self.GameData.room_list[self.GameController.current_room].tiles_array[mover.x][mover.y].object_filling = "None"
        self.GameData.room_list[self.GameController.current_room].tiles_array[mover.x][mover.y].filling_type = "None"
    def fill_tile(self, mover):
        self.GameData.room_list[self.GameController.current_room].tiles_array[mover.x][mover.y].full = True
        self.GameData.room_list[self.GameController.current_room].tiles_array[mover.x][mover.y].object_filling = mover.name
        self.GameData.room_list[self.GameController.current_room].tiles_array[mover.x][mover.y].filling_type = mover.feature_type



