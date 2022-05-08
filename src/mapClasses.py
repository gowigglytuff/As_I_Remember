import csv, os

from keyboards import Direction, Facing

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
    def __init__(self, room_from, room_to, x, y, exit_x, exit_y, name, entrance):
        self.room_from = room_from
        self.room_to = room_to
        self.x = x
        self.y = y
        self.exit_x = exit_x
        self.exit_y = exit_y
        self.name = name
        self.entrance = entrance

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
                    #TODO make buildings fill themselves out based on a csv
                    if drawable.feature_type == "Building" and drawable.x == tile.x and drawable.y == tile.y:
                        for size_x in range(drawable.size_x):
                            for size_y in range(drawable.size_y):
                                if drawable.fill_map[size_y][size_x] == '0':
                                    pass
                                elif drawable.fill_map[size_y][size_x] == '1':
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
        if self.GameData.player["Player"].facing in door.entrance:
            self.empty_tile(self.GameData.player["Player"])
            x_change = self.GameData.player["Player"].x - door.exit_x
            y_change = self.GameData.player["Player"].y - door.exit_y
            # if self.GameData.player["Player"].facing == Direction.DOWN:
            #     self.GameData.player["Player"].turn_player(Direction.DOWN)
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
        else:
            pass

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
        if mover.facing == Direction.LEFT:
            if mover.x <= self.GameData.room_list[self.GameController.current_room].left_edge_x:
                move = False
            else:
                if not facing_tile.full:
                    move = True
                else:
                    move = False
        elif mover.facing == Direction.RIGHT:
            if mover.x >= self.GameData.room_list[self.GameController.current_room].right_edge_x:
                move = False
            else:
                if not facing_tile.full:
                    move = True
                else:
                    move = False
        elif mover.facing == Direction.DOWN:
            if mover.y >= self.GameData.room_list[self.GameController.current_room].bottom_edge_y:
                move = False
            else:
                if not facing_tile.full:
                    move = True
                else:
                    move = False
        if mover.facing == Direction.UP:
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


