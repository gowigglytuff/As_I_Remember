import pygame

class Overlay(object):
    def __init__(self, GameController, GameData, name, x, y, image):
        self.GameController = GameController
        self. GameData = GameData
        self.screen = self.GameController.screen
        self.x = x
        self.y = y
        self.name = name
        self.image = image.get_image(0, 0)

    def print_overlay(self):
        self.screen.blit(self.image, (self.x, self.y))



class Menu(object):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay, offset_x=30, offset_y = 20):
        self.GameController = GameController
        self.GameData = GameData
        self.screen = self.GameController.screen
        self.overlay = overlay
        self.x = self.GameData.overlay_list[self.overlay].x + offset_x
        self.y = self.GameData.overlay_list[self.overlay].y + offset_y
        self.name = name
        self.menu_item_list = menu_item_list
        self.menu_item_list.append("Exit")
        self.menu_spread = 25
        self.menu_go = menu_go
        self.cursor_at = 0

    @property
    def size(self):
        return len(self.menu_item_list)
    def print_cursor(self):
        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render("-", 1, (0, 0, 0))
        self.screen.blit(item, (self.x - 15, (self.y+2) + (self.cursor_at * self.menu_spread)))

    def print_menu(self):
        self.GameData.overlay_list[self.overlay].print_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))
        self.print_cursor()

    def cursor_down(self):
        if self.cursor_at == len(self.menu_item_list) -1:
            self.cursor_at = 0
        else:
            self.cursor_at += 1

    def cursor_up(self):
        print("yay")
        if self.cursor_at == 0:
            self.cursor_at = len(self.menu_item_list) -1
        else:
            self.cursor_at -= 1

    def get_current_menu_item(self):
        menu_selection = self.menu_item_list[self.cursor_at]
        return menu_selection
