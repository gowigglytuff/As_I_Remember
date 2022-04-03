import csv
import os

from features import Feature
from spritesheet import Spritesheet


class Prop(Feature):
    def __init__(self, x, y, gc_input, gd_input):
        super().__init__(x, y, gc_input, gd_input)
        self.imagey = y
        self.imagex = x
        self.drawing_priority = 1
        self.size_x = None
        self.size_y = None
        self.feature_type = "Prop"
        self.width = None
        self.height = None
        self.spritesheet = Spritesheet("assets/prop_sprites/image_error.png", 32, 32)
        self.img = self.spritesheet.get_image(0, 0)
        self.name = None
        self.offset_y = 16
        self.room = None

        try:
            self.gd_input.room_list[self.room].add_room_prop(self.name)
        except:
            pass

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])

    def get_interacted_with(self):
        print("I'm a " + self.name + "!")

class GenericProp(Prop):
    def __init__(self, x, y, gc_input, gd_input, width, height, spritesheet, name, size_x, size_y, room):
        super().__init__(x, y, gc_input, gd_input)
        self.imagey = y
        self.imagex = x
        self.drawing_priority = 1
        self.size_x = size_x
        self.size_y = size_y
        self.feature_type = "Prop"
        self.width = width
        self.height = height
        self.spritesheet = spritesheet
        self.img = self.spritesheet.get_image(0, 0)
        self.name = name
        self.offset_y = 20
        self.room = room

        try:
            self.gd_input.room_list[self.room].add_room_prop(self.name)
        except:
            pass

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])

    #TODO: Fix this!
    def get_interacted_with(self):
        print("I'm a " + self.name + "!")

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

class Building(Prop):
    def __init__(self, x, y, gc_input, gd_input, width, height, spritesheet, name, size_x, size_y, room, fill_csv):
        super().__init__(x, y, gc_input, gd_input)
        self.imagey = y
        self.imagex = x
        self.drawing_priority = 1
        self.size_x = size_x
        self.size_y = size_y
        self.width = width
        self.height = height
        self.spritesheet = Spritesheet(spritesheet, self.width, self.height)
        self.img = self.spritesheet.get_image(0, 0)
        self.name = name
        self.offset_y = -10
        self.room = room
        # TODO: use this to make people walk behind buildings
        self.building_height = 1

        self.fill_csv = fill_csv
        self.feature_type = "Building"
        self.fill_map = self.read_csv(self.fill_csv)

        self.image_list = []
        for item in range(self.size_y):
            self.image_list.append(self.spritesheet.get_strip(item))
            if self.name == "Coop_Building":
                # print(self.spritesheet.get_strip(item))
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


class Prop2(Feature):
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

    @classmethod
    def assign_dict_key(cls):
        key = cls._TYPENAME + "_" + str(cls._serial_number)
        print(cls._serial_number)
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

class AppleTree(Prop2):
    _TYPENAME = "apple tree"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = 64
        self.height = 96
        self.offset_y = self.height - 40
        self.img_location = "assets/prop_sprites/tree.png"
        self.size_x = 2
        self.size_y = 1
        self.fill_out_initiation(room_name)

class PlumTree(Prop2):
    _TYPENAME = "plum tree"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = 96
        self.height = 128
        self.offset_y = self.height - 32
        self.offset_x = 32
        self.img_location = "assets/prop_sprites/ringside_tree.png"
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)
        # TODO: when walk alongside tree image mis-aligns through tree

class PicnicTable(Prop2):
    _TYPENAME = "picnic table"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = 64
        self.height = 64
        self.offset_y = 0
        self.img_location = "assets/prop_sprites/picnic_table.png"
        self.size_x = 2
        self.size_y = 2
        self.fill_out_initiation(room_name)



class BenchHorizontal(Prop2):
    _TYPENAME = "wide bench"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (3*32)
        self.height = (1*32)
        self.offset_y = 0
        self.img_location = "assets/prop_sprites/bench_horizontal.png"
        self.size_x = 3
        self.size_y = 1
        self.fill_out_initiation(room_name)

class BenchVertical(Prop2):
    _TYPENAME = "tall bench"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (3*32)
        self.offset_y = 0
        self.img_location = "assets/prop_sprites/bench_vertical.png"
        self.size_x = 1
        self.size_y = 3
        self.fill_out_initiation(room_name)

class ComputerRight(Prop2):
    _TYPENAME = "right computer"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (2*32)
        self.offset_y = 35
        self.img_location = "assets/prop_sprites/computer.png"
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)

class ComputerBack(Prop2):
    _TYPENAME = "back computer"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (2*32)
        self.offset_y = 32
        self.img_location = "assets/prop_sprites/computer_back.png"
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)

class Bookcase(Prop2):
    _TYPENAME = "bookcase"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (2*32)
        self.offset_y = 36
        self.img_location = "assets/prop_sprites/book_case.png"
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)

class Counter(Prop2):
    _TYPENAME = "counter"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (1*32)
        self.offset_y = 2
        self.img_location = "assets/prop_sprites/counter.png"
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)

class Dress(Prop2):
    _TYPENAME = "dress"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name, img_location):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (1*32)
        self.offset_y = 11
        self.img_location = img_location
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)

class LargeStone(Prop2):
    _TYPENAME = "large stone"
    _serial_number = 1

    def __init__(self, x, y, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.width = (1*32)
        self.height = (1*32)
        self.offset_y = 2
        self.img_location = "assets/prop_sprites/rock.png"
        self.size_x = 1
        self.size_y = 1
        self.fill_out_initiation(room_name)

    def get_interacted_with(self):
        self.gc_input.update_game_dialogue("Maybe if you give it a good whack...")