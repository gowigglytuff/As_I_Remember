import pygame


class Room(object):
    def __init__(self, name, left_edge_x, top_edge_y, width, height, doors_list, images_list):
        self.name = name
        self.left_edge_x = left_edge_x
        self.right_edge_x = left_edge_x + width - 1
        self.top_edge_y = top_edge_y
        self.bottom_edge_y = top_edge_y + height - 1

        self.width = width
        self.height = height
        self.doors_list = doors_list
        self.images_list = images_list
        self.tiles_array = []
        self.tiles_list = []
        self.BG_list = {}
        self.character_list = []
        self.prop_list = []


    def generate_room_grid(self):
        for section in range(self.width + 3):
            section_name = []
            self.tiles_array.append(section_name)

        for letter in range(self.width + 2):
            for number in range(self.height + 3):
                spot_name = Tile(letter, number, False, "None", "None")
                self.tiles_array[letter].append(spot_name)
                self.tiles_list.append(spot_name)

    def add_room_BG(self, bg_name, bg_object):
        self.BG_list[bg_name] = bg_object

    def add_room_character(self, character_name):
        self.character_list.append(character_name)

    def add_room_prop(self, prop_name):
        self.prop_list.append(prop_name)

class Tile(object):
    def __init__(self, x, y, full, object_filling, filling_type, item = None):
        self.x = x
        self.y = y
        self.full = full
        self.object_filling = object_filling
        self.filling_type = filling_type
        self.item = item

class Door(object):
    def __init__(self, room_from, room_to, x, y, exit_x, exit_y):
        self.room_from = room_from
        self.room_to = room_to
        self.x = x
        self.y = y
        self.exit_x = exit_x
        self.exit_y = exit_y

class BG(object):
    def __init__(self, x, y, name, img_file_name_list):
        self.x = x
        self.y = y
        self.img_file_name_list = img_file_name_list
        self.camera = None
        self.img_list = [file_name for file_name in
                        img_file_name_list]

        self.cur_img = 0
        self.img = self.img_list[self.cur_img]
        self.name = name

    def draw(self, screen):
        screen.blit(pygame.image.load(self.img).convert_alpha(), ((self.x) * 32, (self.y) * 40))


class Camera(object):
    def __init__(self, coordinates, anchor):
        self.anchor = anchor
        self.coordinates = [5 - self.anchor.x, 5 - self.anchor.y]

class Position_Manager(object):
    def __init__(self, name, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def parse_map(self):
        self.GameController.get_current_drawables()

    def fill_tiles(self):
        for tile_list in self.GameData.room[self.GameController.room].tiles_array:
            for tile in tile_list:
                drawable_list = self.GameController.get_current_drawables()
                for drawable in drawable_list:
                    if drawable.x == tile.x and drawable.y == tile.y:
                        tile.object_filling = drawable.name
                        tile.filling_type = drawable.name
                        tile.full = True

    def can_move(self, mover):
        move = False
        facing_tile = mover.get_facing_tile()
        if mover.facing == "left":
            if mover.x <= self.GameData.room[self.GameController.room].left_edge_x:
                move = False
            else:
                if not facing_tile.full:
                    move = True
                else:
                    move = False
        elif mover.facing == "right":
            if mover.x >= self.GameData.room[self.GameController.room].right_edge_x:
                move = False
            else:
                if not facing_tile.full:
                    move = True
                else:
                    move = False
        elif mover.facing == "front":
            if mover.y >= self.GameData.room[self.GameController.room].bottom_edge_y:
                move = False
            else:
                if not facing_tile.full:
                    move = True
                else:
                    move = False
        if mover.facing == "back":
            if mover.y <= self.GameData.room[self.GameController.room].top_edge_y:
                move = False
            else:
                if not facing_tile.full:
                    move = True
                else:
                    move = False

        return move

    def empty_tile(self, mover):
        self.GameData.room[self.GameController.room].tiles_array[mover.x][mover.y].full = False
        self.GameData.room[self.GameController.room].tiles_array[mover.x][mover.y].object_filling = "None"
        self.GameData.room[self.GameController.room].tiles_array[mover.x][mover.y].filling_type = "None"
    def fill_tile(self, mover):
        self.GameData.room[self.GameController.room].tiles_array[mover.x][mover.y].full = True
        self.GameData.room[self.GameController.room].tiles_array[mover.x][mover.y].object_filling = mover.name
        self.GameData.room[self.GameController.room].tiles_array[mover.x][mover.y].filling_type = mover.type

        # if mover.facing == "left":
        #     self.GameData.room[self.GameController.room].tiles_array[mover.x-1][mover.y].full = True
        # if mover.facing == "right":
        #     self.GameData.room[self.GameController.room].tiles_array[mover.x+1][mover.y].full = True
        # if mover.facing == "front":
        #     self.GameData.room[self.GameController.room].tiles_array[mover.x][mover.y+1].full = True
        # if mover.facing == "back":
        #     self.GameData.room[self.GameController.room].tiles_array[mover.x][mover.y-1].full = True
