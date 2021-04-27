import pygame

class Overlay(object):
    def __init__(self, GameController, GameData, name, size, x, y, image):
        self.GameController = GameController
        self. GameData = GameData
        self.screen = self.GameController.screen
        self.x = x
        self.y = y
        self.name = name
        self.size = size
        self.image = image

    def print_overlay(self):
        self.screen.blit(self.image, (self.x, self.y))



class Menu(object):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, cursor, overlay):
        self.GameController = GameController
        self.GameData = GameData
        self.screen = self.GameController.screen
        self.overlay = overlay
        self.x = self.GameData.overlay_list[self.overlay].x
        self.y = self.GameData.overlay_list[self.overlay].y
        self.name = name
        self.menu_item_list = menu_item_list
        self.menu_go = menu_go
        self.cursor = cursor

    @property
    def size(self):
        return len(self.menu_item_list)

    def print_menu(self):
        self.GameData.overlay_list[self.overlay].print_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 10)
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))

            self.screen.blit(item, (self.x +20, self.y +20 + (option*25)))