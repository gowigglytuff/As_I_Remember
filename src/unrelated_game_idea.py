import random

import randomword
# from math import sin, cos, sqrt
# import pygame
#
# class Cube(object):
#     def __init__(self, x, y, z, word):
#         self.ID = (x, y, z)
#         self.depth = x
#         self.height = y
#         self.width = z
#         self.word = word
#
# class WorldInfo(object):
#     def __init__(self):
#         self.cube_list = []
#         self.cube_matrix = {}
#         self.world_width = 10
#         self.world_height = 10
#         self.world_depth = 10
#         self.populate_matrix()
#         self.print_matrix()
#
#     def populate_cube_list(self):
#         depths = []
#         for x in range(self.world_depth):
#             self.cube_list.append([])
#             heights = []
#             for y in range(self.world_height):
#                 widths = []
#                 for z in range(self.world_width):
#                     widths.append((x, y, z))
#                 print(widths)
#                 heights.append(widths)
#             print("")
#             depths.append(heights)
#         self.cube_list = depths
#
#     def populate_matrix(self):
#         cubes = {}
#         for x in range(self.world_depth):
#             for y in range(self.world_height):
#                 for z in range(self.world_width):
#                     cubes[(x, y, z)] = Cube(x, y, z, randomword.get_random_word())
#
#         self.cube_matrix = cubes
#         # print(self.cube_matrix)
#
#     def print_matrix(self):
#         list = []
#
#         for x in range(self.world_depth):
#             for y in range(self.world_height):
#                 # row = []
#                 for z in range(self.world_width):
#                     # item = ((self.cube_matrix[(x, y, z)].depth, self.cube_matrix[(x, y, z)].height, self.cube_matrix[(x, y, z)].width))
#                     item = self.cube_matrix[(x, y, z)].word
#                     print(item, end=", ")
#                 print("")
#             print("")
#
# # WI = WorldInfo()
#
# class Window:
#     def __init__(self, width, height, title):
#         self.width = width
#         self.height = height
#         self.title = title
#
#         self.screen = pygame.display.set_mode((self.width, self.height))
#         pygame.display.set_caption(self.title)
#
#     def key_check(self, key):
#         keys = pygame.key.get_pressed()
#
#         if (keys[key]):
#             return True
#
#     def update(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#
#         pygame.display.update()
#
#
# class Mesh:
#     def __init__(self, verts, edges, x, y, z, rotX, rotY, rotZ, scale):
#         self.verts = verts
#         self.edges = edges
#         self.x = x
#         self.y = y
#         self.z = z
#         self.rotX = rotX
#         self.rotY = rotY
#         self.rotZ = rotZ
#         self.scale = scale
#
#     def project_and_rotate(self, x, y, z):
#         px = (((x * cos(self.rotZ) - sin(self.rotZ) * y) * cos(self.rotY) - z * sin(self.rotY)) * (200 / ((((z * cos(self.rotY) + (x * cos(self.rotZ) - sin(self.rotZ) * y) * sin(self.rotY)) * cos(self.rotX) + (y * cos(self.rotZ) + x * sin(self.rotZ)) * sin(self.rotX))) + self.z))) * self.scale + self.x
#         py = (((y * cos(self.rotZ) + x * sin(self.rotZ))
#                * cos(self.rotX) -
#                (z * cos(self.rotY) + (x * cos(self.rotZ) - sin(self.rotZ) * y) * sin(self.rotY))
#                * sin(self.rotX)) *
#               (200 / ((((z * cos(self.rotY) + (x * cos(self.rotZ) - sin(self.rotZ) * y) * sin(self.rotY))
#                         * cos(self.rotX) + (y * cos(self.rotZ) + x * sin(self.rotZ)) * sin(self.rotX)))
#                       + self.z))) * self.scale + self.y
#
#
#         return (int(px), int(py))
#
#     def render(self, window):
#
#
#         # for vert in self.verts:
#         #     point = self.project_and_rotate(vert[0], vert[1], vert[2])
#         #
#         #     pygame.draw.circle(window.screen, (0, 0, 0), point, 6)
#
#         for edge in self.edges:
#             point1 = self.project_and_rotate(self.verts[edge[0]][0], self.verts[edge[0]][1], self.verts[edge[0]][2])
#             point2 = self.project_and_rotate(self.verts[edge[1]][0], self.verts[edge[1]][1], self.verts[edge[1]][2])
#
#             point1 = self.project_and_rotate(self.verts[edge[0]][0], self.verts[edge[0]][1], self.verts[edge[0]][2])
#             point2 = self.project_and_rotate(self.verts[edge[1]][0], self.verts[edge[1]][1], self.verts[edge[1]][2])
#
#             print(point1)
#
#             pygame.draw.line(window.screen, (0, 0, 0), point1, point2, 5)
#
# def generate_points():
#     start_point_x = 100
#     start_point_y = 100
#     w = 100
#     h = 100
#     d = 100
#
#     point1 = (start_point_x, start_point_y)
#     point2 = (start_point_x + w, start_point_y)
#     point4 = (start_point_x, start_point_y + h)
#     point3 = (start_point_x + w, start_point_y + h)
#
#     list = [point1, point2, point3, point4]
#
#
#
# window = Window(500, 500, "Cube")
# cube = Mesh([(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0), (0, 0, -1), (0, 1, -1), (1, 1, -1), (1, 0, -1)],
#             [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)],
#             100, 100, 5, 1, 1, 1, 5)
# # cube2 = Mesh([(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0), (0, 0, -1), (0, 1, -1), (1, 1, -1), (1, 0, -1)], [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)], cube.x +300, cube.y + 0, 5, 0, 0, 0, 5)
#
# while True:
#     # cube.rotX += 0.001
#     # cube.rotY += 0.01
#     # cube.rotZ += 0.001
#     generate_points()
#
#     window.screen.fill((255, 255, 255))
#     # cube2.render(window)
#     # cube.render(window)
#
#
#
#     x = 25
#     y = 50
#     z = 50
#
#     angle_x = 1
#     angle_y = 1
#     angle_z = 1
#
#     origin = 200
#     spread_x = 100
#     spread_y = 100
#     spread_w = 100
#
#     cross = sqrt(spread_x**2 + spread_y**2)
#     print(cross)
#
#     a = (origin, origin)
#     b = (origin, origin + spread_y)
#     c = (origin + spread_x, origin)
#     d = (origin + spread_x, origin + spread_y)
#
#     ax = (a[0] + spread_w, a[1])
#     bx = (b[0] + spread_w, b[1])
#     cx = (c[0] + spread_w, c[1])
#     dx = (d[0] + spread_w, d[1])
#
#     pygame.draw.line(window.screen, (0, 0, 0), a, b, 5)
#     pygame.draw.line(window.screen, (0, 0, 0), b, d, 5)
#     pygame.draw.line(window.screen, (0, 0, 0), a, c, 5)
#     pygame.draw.line(window.screen, (0, 0, 0), c, d, 5)
#
#     pygame.draw.line(window.screen, (0, 0, 0), ax, bx, 5)
#     pygame.draw.line(window.screen, (0, 0, 0), bx, dx, 5)
#     pygame.draw.line(window.screen, (0, 0, 0), ax, cx, 5)
#     pygame.draw.line(window.screen, (0, 0, 0), cx, dx, 5)
#
#     pygame.draw.line(window.screen, (0, 0, 0), a, ax, 5)
#     pygame.draw.line(window.screen, (0, 0, 0), b, bx, 5)
#     pygame.draw.line(window.screen, (0, 0, 0), c, cx, 5)
#     pygame.draw.line(window.screen, (0, 0, 0), d, dx, 5)
#
#     window.update()

random_word = randomword.get_random_word()


class Cube(object):
    COLOURS = ["red", "blue", "yellow"]
    def __init__(self, x, y, z, word):
        self.ID = (x, y, z)
        self.depth = x
        self.height = y
        self.width = z
        self.word = word
        self.colour = random.choice(self.COLOURS)
        self.active = None



    def assign_active(self):
        if self.height == 0:
            result = random.choices([True, False], weights=[100, 0], k=1)
        # elif:
        #     pass
        else:
            result = random.choices([True, False], weights=[1, 5], k=1)

        self.active = result[0]


class WorldInfo(object):
    def __init__(self):
        self.cube_list = []
        self.cube_matrix = {}
        self.world_width = 3
        self.world_height = 3
        self.world_depth = 3
        self.populate_matrix()

    def check_cube_to_left(self, current_cube):
        result = True
        try:
            left_cube = self.cube_matrix[(current_cube[0]-1, current_cube[1], current_cube[2])]
            result = False
        except:
            pass

        return result

    def check_cube_to_front(self, current_cube):
        result = False
        try:
            left_cube = self.cube_matrix[(current_cube[0], current_cube[1], current_cube[2]-1)]
            result = True
        except:
            pass

        return result

    def check_cube_to_below(self, current_cube):
        result = False
        try:
            left_cube = self.cube_matrix[(current_cube[0], current_cube[1]-1, current_cube[2])]
            result = True
        except:
            pass

        return result

    def assign_active_to_each_cube(self):
        for x in range(self.world_depth):
            for z in range(self.world_width):
                # row = []
                for y in range(self.world_height):
                    self.assign_active((y, x, z))

                    self.check_cube_to_front((y, x, z))
                    self.check_cube_to_below((y, x, z))

    def assign_active(self, cube):
        left = self.check_cube_to_left(self.cube_matrix[cube].ID)
        front = self.check_cube_to_front(self.cube_matrix[cube].ID)
        below = self.check_cube_to_below(self.cube_matrix[cube].ID)

        chance_of_active = 1
        if left:
            chance_of_active += 3
        if below:
            chance_of_active += 1
        if front:
            chance_of_active += 3

        if self.cube_matrix[cube].height == 0:
            result = random.choices([True, False], weights=[100, 0], k=1)
        # elif:
        #     pass
        else:
            result = random.choices([True, False], weights=[chance_of_active, 10], k=1)

        self.cube_matrix[cube].active = result[0]


    def populate_cube_list(self):
        depths = []
        for x in range(self.world_depth):
            self.cube_list.append([])
            heights = []
            for y in range(self.world_height):
                widths = []
                for z in range(self.world_width):
                    widths.append((x, y, z))
                print(widths)
                heights.append(widths)
            print("")
            depths.append(heights)
        self.cube_list = depths

    def populate_matrix(self):
        cubes = {}
        for x in range(self.world_depth):
            for y in range(self.world_height):
                for z in range(self.world_width):
                    cubes[(x, y, z)] = Cube(x, y, z, randomword.get_random_word())
                    # print(cubes[(x, y, z)].width, cubes[(x, y, z)].height, cubes[(x, y, z)].depth)

        self.cube_matrix = cubes
        # print(self.cube_matrix)

    def print_matrix(self):
        list = []

        for x in range(self.world_depth):
            for y in range(self.world_height):
                # row = []
                for z in range(self.world_width):
                    # item = ((self.cube_matrix[(x, y, z)].depth, self.cube_matrix[(x, y, z)].height, self.cube_matrix[(x, y, z)].width))
                    item = self.cube_matrix[(x, y, z)].word
                    print(item, end=", ")
                print("")
            print("")

    def print_matrix_colour(self):
        list = []

        for x in range(self.world_depth):
            for y in range(self.world_height):
                # row = []
                for z in range(self.world_width):
                    # item = ((self.cube_matrix[(x, y, z)].depth, self.cube_matrix[(x, y, z)].height, self.cube_matrix[(x, y, z)].width))
                    item = self.cube_matrix[(x, y, z)].colour
                    print(item, end=", ")
                print("")
            print("")

    def print_matrix_active_front_view(self):
        list = []

        for x in range(self.world_depth):
            print("Front view, layer: " + str(x))
            for y in reversed(range(self.world_height)):
                # row = []
                for z in range(self.world_width):
                    item = ((self.cube_matrix[(x, y, z)].depth, self.cube_matrix[(x, y, z)].height, self.cube_matrix[(x, y, z)].width))
                    active = self.cube_matrix[(x, y, z)].active
                    # item = "[|]"
                    # if not active:
                    #     item = "[-]"
                    print(item, end=", ")
                print("")
            print("")

    def print_matrix_active_top_view(self):
        list = []

        for x in range(self.world_depth):
            print("Top view, layer: " + str(x))
            for y in reversed(range(self.world_height)):
                # row = []
                for z in range(self.world_width):
                    item = ((self.cube_matrix[(x, y, z)].depth, self.cube_matrix[(x, y, z)].height, self.cube_matrix[(x, y, z)].width))
                    active = self.cube_matrix[(y, x, z)].active
                    # item = "[|]"
                    # if not active:
                    #     item = "[-]"
                    print(item, end=", ")
                print("")

            print("")

WI = WorldInfo()
WI.assign_active_to_each_cube()

WI.print_matrix_active_front_view()
WI.print_matrix_active_top_view()