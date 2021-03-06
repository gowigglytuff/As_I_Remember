import csv
import os

from features import Feature
from spritesheet import Spritesheet


class Decoration(Feature):
    def __init__(self, x, y, gc_input, gd_input, width, height, spritesheet, name, size_x, size_y, location_list, room):
        super().__init__(x, y, gc_input, gd_input)
        self.location_list = location_list
        self.offset_y = 3
        self.width = width
        self.height = height
        self.spritesheet = spritesheet
        self.img = self.spritesheet.get_image(0, 0)
        self.name = name
        self.size_x = size_x
        self.size_y = size_y
        self.room = room
        self.drawing_priority = 1

        self.gd_input.room_list[self.room].add_room_decoration(self.name)

    def draw(self, screen):
        for location in self.location_list:
            screen.blit(self.img, [((location[0] + self.gc_input.camera[0]) * self.gd_input.square_size[
                            0]) + self.gd_input.base_locator_x, (((location[1] + self.gc_input.camera[1]) *
                                                                  self.gd_input.square_size[1]) - self.offset_y) + self.gd_input.base_locator_y])


class Prop(Feature):
    _TYPENAME = "generic"
    _serial_number = 109

    def __init__(self, x, y, gc_input, gd_input):
        super().__init__(x, y, gc_input, gd_input)
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.type_name = None
        self.imagey = y
        self.imagex = x
        self.drawing_priority = 1
        self.feature_type = "Prop"
        self.img_location = None
        self.spritesheet = None
        self.size_x = None
        self.size_y = None
        self.width = None
        self.height = None
        self.img = None
        self.name = None
        self.offset_y = 0
        self.offset_x = 0
        self.room = None

        try:
            self.gd_input.room_list[self.room].add_room_prop(self.name)
        except:
            pass

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0] - self.offset_x) + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1]) * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])

    def get_interacted_with(self):
        self.gc_input.update_game_dialogue("Why, seems to be a simple " + self._TYPENAME + ".")

    @classmethod
    def assign_dict_key(cls):
        key = cls._TYPENAME + "_" + str(cls._serial_number)
        return key

    @classmethod
    def up_serial_number(cls):
        cls._serial_number += 1

    def assign_name(self):
        self.name = self._TYPENAME + "_" + str(self._serial_number)
        self.up_serial_number()


    def fill_out_initiation(self, room_name):
        self.assign_name()
        self.spritesheet = Spritesheet(self.img_location, self.width, self.height)
        self.img = self.spritesheet.get_image(0, 0)
        self.cur_img = 0
        self.room = room_name
        self.gd_input.room_list[self.room].add_room_prop(self.name)


    def dissolve(self):
        # self.gd_input.prop_list
        self.gd_input.room_list[self.room].prop_list.remove(self.name)
        self.gd_input.positioner_list[self.room].empty_tile(self)


class GenericProp(Feature):
    _TYPENAME = "generic"

    def __init__(self, x, y, gc_input, gd_input):
        super().__init__(x, y, gc_input, gd_input)
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.type_name = None
        self.imagey = y
        self.imagex = x
        self.drawing_priority = 1
        self.feature_type = "Prop"
        self.img_location = None
        self.spritesheet = None
        self.size_x = None
        self.size_y = None
        self.width = None
        self.height = None
        self.img = None
        self.name = None
        self.offset_y = 12
        self.offset_x = 0
        self.room = None

        try:
            self.gd_input.room_list[self.room].add_room_prop(self.name)
        except:
            pass

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0] - self.offset_x) + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1]) * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])

    def get_interacted_with(self):
        self.gc_input.update_game_dialogue("Why, seems to be a simple " + self._TYPENAME + ".")


    def fill_out_initiation(self, room_name):
        self.spritesheet = Spritesheet(self.img_location, self.width, self.height)
        self.img = self.spritesheet.get_image(0, 0)
        self.cur_img = 0
        self.room = room_name
        self.gd_input.room_list[self.room].add_room_prop(self.name)


    def dissolve(self):
        # self.gd_input.prop_list
        self.gd_input.room_list[self.room].prop_list.remove(self.name)
        self.gd_input.positioner_list[self.room].empty_tile(self)


class Building(GenericProp):
    def __init__(self, x, y, gc_input, gd_input, width, height, img_location, name, size_x, size_y, room_name, fill_csv):
        super().__init__(x, y, gc_input, gd_input)
        self.size_x = size_x
        self.size_y = size_y
        self.width = width
        self.height = height
        self.img_location = img_location
        self.name = name
        self.offset_y = -10
        self.fill_out_initiation(room_name)

        # TODO: use this to make people walk behind buildings
        self.building_height = 1

        self.fill_csv = fill_csv
        self.feature_type = "Building"
        self.fill_map = self.read_csv(self.fill_csv)

        self.image_list = []
        for item in range(self.size_y):
            self.image_list.append(self.spritesheet.get_strip(item))
            if self.name == "Coop_Building":
                pass

        try:
            self.gd_input.room_list[self.room].add_room_prop(self.name)
        except:
            pass

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])

    def draw_strip(self, screen, strip):
        screen.blit(self.image_list[strip-1], [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y+((int(strip-1))*32)])

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map


class BuildingComplex(Building):
    def __init__(self, x, y, gc_input, gd_input, width, height, img_location, name, size_x, size_y, room_name, fill_csv, priority_csv):
        super().__init__(x, y, gc_input, gd_input, width, height, img_location, name, size_x, size_y, room_name, fill_csv)
        self.priority_csv = self.read_priority_csv(priority_csv)

    def set_priority(self):
        player_location = [self.gd_input.player["Player"].x, self.gd_input.player["Player"].y]
        building_location = [self.x, self.y]
        player_on_building = [(player_location[0]-building_location[0]), (player_location[1]-building_location[1])]

        print(self.priority_csv[player_on_building[1]][player_on_building[0]])

        if self.priority_csv[player_on_building[1]][player_on_building[0]] == "1":
            self.drawing_priority = 1
        elif self.priority_csv[player_on_building[1]][player_on_building[0]] == "0":
            self.drawing_priority = 3


        print(self.drawing_priority)
        print(self.gd_input.player["Player"].drawing_priority)




    def read_priority_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map


class AppleTree(Prop):
    _TYPENAME = "apple tree"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = 64
        self.height = (3*32)+8
        self.offset_y = 12 + (32*2)
        self.img_location = "assets/prop_sprites/apple_tree.png"
        self.size_x = 2
        self.size_y = 1
        self.fill_out_initiation(room_name)


class PlumTree(Prop):
    _TYPENAME = "plum tree"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = 64
        self.height = (3*32)+8
        self.offset_y = 8 + (32*2)
        self.img_location = "assets/prop_sprites/plum_tree.png"
        self.size_x = 2
        self.size_y = 1
        self.fill_out_initiation(room_name)


class PicnicTable(Prop):
    _TYPENAME = "picnic table"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = 64
        self.height = (2*32)+8
        self.offset_y = 8
        self.img_location = "assets/prop_sprites/picnic_table.png"
        self.size_x = 2
        self.size_y = 2
        self.fill_out_initiation(room_name)


class BenchHorizontal(Prop):
    _TYPENAME = "wide bench"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (3*32)
        self.height = (1*40)
        self.offset_y = 12
        self.img_location = "assets/prop_sprites/bench_horizontal.png"
        self.size_x = 3
        self.size_y = 1
        self.fill_out_initiation(room_name)

class BenchVertical(Prop):
    _TYPENAME = "tall bench"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (3*32)+8
        self.offset_y = 8
        self.img_location = "assets/prop_sprites/bench_vertical.png"
        self.size_x = 1
        self.size_y = 3
        self.fill_out_initiation(room_name)

class ComputerRight(Prop):
    _TYPENAME = "right computer"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (1*32)+8
        self.offset_y = 9
        self.img_location = "assets/prop_sprites/computer.png"
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)

class ComputerBack(Prop):
    _TYPENAME = "back computer"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (1*32) + 8
        self.offset_y = 9
        self.img_location = "assets/prop_sprites/computer_back.png"
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)

class Bookcase(Prop):
    _TYPENAME = "bookcase"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (1*32) + 8
        self.offset_y = 12
        self.img_location = "assets/prop_sprites/book_case.png"
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)

class Counter(Prop):
    _TYPENAME = "counter"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (1*32)+8
        self.offset_y = 12
        self.img_location = "assets/prop_sprites/counter.png"
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)

class Dress(Prop):
    _TYPENAME = "dress"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name, img_location):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (1*32)+8
        self.offset_y = 16
        self.img_location = img_location
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)

class LargeStone(Prop):
    _TYPENAME = "large stone"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (1*32)+8
        self.offset_y = 12
        self.img_location = "assets/prop_sprites/rock.png"
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)

    def get_interacted_with(self):
        self.gc_input.update_game_dialogue("Maybe if you give it a good whack...")

class Planter(Prop):
    _TYPENAME = "planter"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (1*32)+8
        self.offset_y = 8
        self.img_location = "assets/prop_sprites/empty_planter_3.png"
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)

    def get_interacted_with(self):
        self.gc_input.update_game_dialogue("Could use a nice plant!")

class StopSign(Prop):
    _TYPENAME = "stop sign"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (1*32)+8
        self.offset_y = 8
        self.img_location = "assets/prop_sprites/stopsign_quarter.png"
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)

    def get_interacted_with(self):
        self.gc_input.update_game_dialogue("STOP!")

class PineTree(Prop):
    _TYPENAME = "pine tree"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = 64
        self.height = (2*32)+8
        self.offset_y = (32*2)-16
        self.img_location = "assets/prop_sprites/pine_tree.png"
        self.size_x = 2
        self.size_y = 1
        self.fill_out_initiation(room_name)

class SignPost(Prop):
    _TYPENAME = "sign post"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name, address):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (1*32)+8
        self.offset_y = 16
        self.img_location = "assets/prop_sprites/signpost.png"
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)
        self.address = address
    def get_interacted_with(self):
        self.gc_input.update_game_dialogue("Address: " + self.address)

class Hole(Prop):
    _TYPENAME = "hole"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (1*32)
        self.offset_y = 0
        self.img_location = "assets/prop_sprites/ground_hole.png"
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)

    def get_interacted_with(self):
        self.gc_input.update_game_dialogue("It's an empty hole...")