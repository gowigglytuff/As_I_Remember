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
        self.offset_y = 20
        self.room = None

        try:
            self.gd_input.room_list[self.room].add_room_prop(self.name)
        except:
            pass

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])

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

class Tree(Prop):
    def __init__(self, x, y, name, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.drawing_priority = 1
        self.imagex = x
        self.imagey = y
        self.width = 64
        self.height = 96
        self.spritesheet = Spritesheet("assets/prop_sprites/tree.png", 64, 96)
        self.name = name
        self.size_x = 2
        self.size_y = 1
        self.offset_y = 64
        self.feature_type = "Prop"
        self.cur_img = 0
        self.img = self.spritesheet.get_image(0, 0)
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.room = room_name

        self.gd_input.room_list[self.room].add_room_prop(self.name)

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])


    #TODO: Fix this!
    def get_interacted_with(self):
        print("I'm a " + self.name + "!")