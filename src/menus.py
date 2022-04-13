import textwrap

from keyboards import *
from spritesheet import *


class MenuManager(object):
    def __init__(self, gd_input, gc_input):
        self.gd_input = gd_input
        self.gc_input = gc_input
        self.static_menus = [StatsMenu.NAME, GameActionDialogue.NAME]
        self.active_menu = []
        self.menu_stack = []
        self.visible_menus = []

    def add_menu_to_stack(self, menu_to_add):
        self.menu_stack.insert(0, menu_to_add)
        self.add_menu_to_visible(menu_to_add)

    def add_menu_to_visible(self, menu_to_add):
        self.visible_menus.insert(0, menu_to_add)
        if self.gd_input.menu_list[menu_to_add].menu_type == "base":
            for menu in self.visible_menus:
                if (menu != menu_to_add) and (self.gd_input.menu_list[menu_to_add].menu_type == "base"):
                    self.visible_menus.remove(menu)

    def deactivate_menu(self, menu_to_deactivate):
        self.menu_stack.remove(menu_to_deactivate)
        if menu_to_deactivate in self.visible_menus:
            self.visible_menus.remove(menu_to_deactivate)

        if len(self.menu_stack) == 0:
            self.gc_input.set_keyboard_manager(
                InGame.ID)


class Overlay(object):
    def __init__(self, gc_input, gd_input, name, x, y, image):
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.screen = self.gc_input.screen
        self.x = x
        self.y = y
        self.name = name
        self.image = image.get_image(0, 0)

    def display_overlay(self):
        self.screen.blit(self.image, (self.x, self.y))


class TextBox(Overlay):
    def __init__(self, gc_input, gd_input, name, x, y, image):
        super().__init__(gc_input, gd_input, name, x, y, image)

    def display_phrase(self, character):
        # prints the speakers name
        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render(self.gd_input.character_list[character].name + ":", True, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.gd_input.overlay_list["text_box"].x + 150, self.gd_input.overlay_list["text_box"].y + 20))

        # prints phrases to be spoke
        text_line = 0
        for line in self.gd_input.character_list[character].speaking_queue:
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(line, True, (0, 0, 0))
            self.gc_input.screen.blit(item, (self.gd_input.overlay_list["text_box"].x + 150, self.gd_input.overlay_list["text_box"].y + 50 + 25 * text_line))
            text_line += 1


# Static Menus
class GameActionDialogue(object):
    NAME = "game_action_dialogue_menu_2"
    OVERLAYNAME = "game_dialogue_box_2"

    def __init__(self, gc_input, gd_input):
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.screen = self.gc_input.screen
        gd_input.add_overlay(self.OVERLAYNAME, Overlay(gc_input, gd_input, self.OVERLAYNAME, 680, 680, Spritesheet("assets/menu_images/testing_menu2.png", 300, 100)))
        self.overlay = self.OVERLAYNAME
        self.offset_x = 10
        self.offset_y = 20
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.name = self.NAME
        self.menu_item_list = ["This is the game dialouge box!"]
        self.menu_spread = 17
        self.cursor_at = 0
        self.y_spacing = 0
        self.menu_type = "static"

    @property
    def size(self):
        return len(self.menu_item_list)

    def show_dialogue(self, phrase):
        if len(self.menu_item_list) >= 4:
            del self.menu_item_list[0]
        self.menu_item_list.append(phrase)
        # self.display_menu()

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.gc_input.font, 7)
            item = my_font.render(self.menu_item_list[option], True, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))


class StatsMenu(object):
    NAME = "Stats Menu"
    OVERLAYNAME = "stats_overlay2"

    def __init__(self, gc_input, gd_input):
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.screen = self.gc_input.screen
        gd_input.add_overlay(self.OVERLAYNAME, Overlay(gc_input, gd_input, self.OVERLAYNAME, 830, 20, Spritesheet("assets/menu_images/stats_menu.png", 150, 100)))
        self.overlay = self.OVERLAYNAME
        self.offset_x = 20
        self.offset_y = 15
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.name = self.NAME
        self.menu_item_list = [("Coins: ", str(self.gc_input.your_coins)), ("Day: ", str(self.gc_input.day_of_summer)), ("Time: ", str(self.gc_input.time_of_day)+":00"), ("Seeds:", str(self.gc_input.your_seeds))]
        self.menu_spread = 15
        self.cursor_at = 0
        self.y_spacing = 0
        self.menu_type = "static"

    @property
    def size(self):
        return len(self.menu_item_list)

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.gc_input.font, 7)
            item = my_font.render(self.menu_item_list[option][0], True, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))

        for quantitity in range(self.size):
            my_font = pygame.font.Font(self.gc_input.font, 7)
            item = my_font.render(self.menu_item_list[quantitity][1], True, (0, 0, 0))
            self.screen.blit(item, (self.x + 112 - (7 * len(self.menu_item_list[quantitity][1])), self.y + (quantitity * self.menu_spread)))

    def update_menu_items_list(self):
        self.menu_item_list = [("Coins: ", str(self.gc_input.your_coins)), ("Day: ", str(self.gc_input.day_of_summer)), ("Time: ", str(self.gc_input.time_of_day)+":00"), ("Friends:", str(self.gc_input.your_seeds)), ("Seeds:", str(1))]


# Base Menus            
class MenuTemporary(object):
    NAME = None

    def __init__(self, gc_input, gd_input):
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.screen = self.gc_input.screen
        self.overlay = None
        self.x = None
        self.y = None
        self.offset_x = 30
        self.offset_y = 20
        self.name = None
        self.menu_item_list = []
        self.menu_spread = 25
        self.cursor_at = 0
        self.y_spacing = 0
        self.name = self.NAME
        self.menu_type = "base"

    # Same for most menus
    def cursor_down(self):
        if self.cursor_at == len(self.menu_item_list) -1:
            self.cursor_at = 0
        else:
            self.cursor_at += 1

    def cursor_up(self):
        if self.cursor_at == 0:
            self.cursor_at = len(self.menu_item_list) -1
        else:
            self.cursor_at -= 1

    def cursor_left(self):
        pass

    def cursor_right(self):
        pass

    def update_menu_items_list(self):
        pass

    def reset_cursor(self):
        self.cursor_at = 0

    def display_cursor(self):
        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render("-", True, (0, 0, 0))
        self.screen.blit(item, (self.x - 12, (self.y+2 + self.y_spacing) + (self.cursor_at * self.menu_spread)))

    def get_current_menu_item(self):
        menu_selection = self.menu_item_list[self.cursor_at]
        return menu_selection

    # each menu needs its own
    def set_menu(self):
        self.update_menu_items_list()
        self.gc_input.set_keyboard_manager(InMenu.ID)
        self.gc_input.menu_manager.add_menu_to_stack(self.name)

    def exit_menu(self):
        self.reset_cursor()
        self.gc_input.menu_manager.deactivate_menu(self.name)


    @property
    def size(self):
        return len(self.menu_item_list)

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(self.menu_item_list[option], True, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))
        self.display_cursor()

    def choose_option(self):
        self.do_option()

    def do_option(self):
        pass

    def try_to_exit(self):
        pass

    def exit_all_menus(self):
        self.exit_menu()
        if len(self.gc_input.menu_manager.menu_stack) > 0:
            self.gd_input.menu_list[self.gc_input.menu_manager.menu_stack[0]].exit_all_menus()


class StartMenu(MenuTemporary):
    NAME = "start_menu"
    OVERLAYNAME = "start_menu"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.menu_item_list = ["Bag", "Outfits", "Map", "Chore List", "Profile", "Save", "Options", "Vibes"]
        self.menu_item_list.append("Exit")
        self.menu_type = "base"
        gd_input.add_overlay(self.OVERLAYNAME, Overlay(gc_input, gd_input, self.OVERLAYNAME, 700, 200, Spritesheet("assets/menu_images/start_menu.png", 150, 400)))
        self.overlay = self.OVERLAYNAME
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"

    def do_option(self):
        menu_selection = self.get_current_menu_item()

        if menu_selection == "Bag":
            self.gd_input.menu_list[InventoryMenu.NAME].set_menu()

        elif menu_selection == "Key Items":
            self.gd_input.menu_list[KeyInventoryMenu.NAME].set_menu()

        elif menu_selection == "Chore List":
            self.gd_input.menu_list[ToDoListMenu.NAME].set_menu()

        elif menu_selection == "Profile":
            self.gd_input.menu_list[ProfileMenu.NAME].set_menu()

        elif menu_selection == "Map":
            self.gd_input.menu_list[MapMenu.NAME].set_menu()

        elif menu_selection == "Exit":
            self.exit_all_menus()

        elif menu_selection == "Outfits":
            self.gd_input.menu_list["outfits_menu"].set_menu()

        elif menu_selection == "Save":
            self.gc_input.update_game_dialogue("You saved the game!")
            self.exit_menu()

        else:
            self.exit_all_menus()

    def choose_option(self):
        self.do_option()


# Menus' from Start Menu
class InventoryMenu(MenuTemporary):
    NAME = "inventory_menu"
    OVERLAYNAME = "inventory_menu_overlay"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.menu_item_list = self.gc_input.inventory.current_items
        self.y_spacing = 20
        self.max_length = 14
        gd_input.add_overlay(self.OVERLAYNAME, Overlay(gc_input, gd_input, self.OVERLAYNAME, 700, 200, Spritesheet("assets/menu_images/inventory_menu.png", 200, 400)))
        self.overlay = self.OVERLAYNAME
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"
        self.currently_displayed_items = None
        self.list_shifts = 0


    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render("<    ITEMS    >", True, (0, 0, 0))
        self.screen.blit(item, (self.x, self.y))

        menu_length_calc = 0
        if self.size >= self.max_length:
            menu_length_calc = self.max_length
        elif self.size < self.max_length:
            menu_length_calc = self.size

        for option in range(menu_length_calc):
            if self.currently_displayed_items[option] == "Exit":
                item = my_font.render(self.currently_displayed_items[option], True, (0, 0, 0))
                self.screen.blit(item, (self.x, self.y + self.y_spacing + (option * self.menu_spread)))

            else:
                item = my_font.render(self.currently_displayed_items[option], True, (0, 0, 0))
                self.screen.blit(item, (self.x, self.y + self.y_spacing + (option * self.menu_spread)))

                spacing = 0
                if len(str(self.gd_input.item_list[self.currently_displayed_items[option]].quantity)) == 3:
                    spacing = 110
                elif len(str(self.gd_input.item_list[self.currently_displayed_items[option]].quantity)) == 2:
                    spacing = 120
                else:
                    spacing = 130

                item = my_font.render("x" + str(self.gd_input.item_list[self.currently_displayed_items[option]].quantity), True, (0, 0, 0))
                self.screen.blit(item, (self.x + spacing, self.y + self.y_spacing + (option * self.menu_spread)))

        self.display_cursor()

    def choose_option(self):
        chosen_item = self.get_current_menu_item()
        if chosen_item == "Exit":
            self.exit_all_menus()
        else:
            self.gd_input.menu_list[UseMenu.NAME].set_menu()

    def do_option(self, choice=None):
        menu_selection = choice

        if menu_selection == "Use":
            self.gd_input.item_list[self.get_current_menu_item()].use_item()
            self.exit_all_menus()

        elif menu_selection == "Toss":
            self.gc_input.update_game_dialogue("You tossed 1 " + str(self.get_current_menu_item()))
            self.gc_input.inventory.unget_item(self.get_current_menu_item(), 1)
            self.exit_all_menus()

        elif menu_selection == "Exit":
            self.exit_all_menus()

    def cursor_left(self):
        self.exit_menu()
        self.gd_input.menu_list[KeyInventoryMenu.NAME].set_menu()

    def cursor_right(self):
        self.exit_menu()
        self.gd_input.menu_list[KeyInventoryMenu.NAME].set_menu()

    def exit_menu(self):
        self.gc_input.inventory.reset_bag_slot()
        self.reset_cursor()
        self.gc_input.menu_manager.deactivate_menu(self.name)

    def update_menu_items_list(self):
        self.menu_item_list = sorted(self.gc_input.inventory.current_items)
        self.menu_item_list.append("Exit")
        self.update_currently_displayed()

    def update_currently_displayed(self):
        self.currently_displayed_items = []
        if self.size <= self.max_length:
            for item in range(self.size):
                self.currently_displayed_items.append(self.menu_item_list[item + self.list_shifts])
        else:
            for item in range(self.max_length):
                self.currently_displayed_items.append(self.menu_item_list[item + self.list_shifts])

    def cursor_down(self):

        if self.size > 1:
            if (self.cursor_at + self.list_shifts) < self.size - 1:
                if self.size > self.max_length:
                    if self.cursor_at == self.max_length - 1:
                        self.list_shifts += 1
                        self.update_currently_displayed()
                    elif self.cursor_at < self.max_length - 1:
                        self.cursor_at += 1
                    else:
                        pass

                elif self.max_length >= self.size > self.cursor_at:
                    self.cursor_at += 1

    def cursor_up(self):
        if (self.cursor_at + self.list_shifts) > 0:
            if self.cursor_at == 0 and self.list_shifts > 0:
                self.list_shifts -= 1
                self.update_currently_displayed()
            elif self.cursor_at > 0:
                self.cursor_at -= 1
            else:
                pass

    def get_current_menu_item(self):
        menu_selection = self.currently_displayed_items[self.cursor_at]
        return menu_selection

    def reset_cursor(self):
        self.cursor_at = 0
        self.list_shifts = 0


class KeyInventoryMenu(MenuTemporary):
    NAME = "key_inventory_menu"
    OVERLAYNAME = "key_inventory_menu_overlay"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.menu_item_list = self.gc_input.inventory.current_key_items
        self.y_spacing = 20
        gd_input.add_overlay(self.OVERLAYNAME, Overlay(gc_input, gd_input, self.OVERLAYNAME, 700, 200, Spritesheet("assets/menu_images/inventory_menu.png", 200, 400)))
        self.overlay = self.OVERLAYNAME
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"

        self.currently_displayed_items = None
        self.list_shifts = 0
        self.max_length = 14

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render("<  KEY ITEMS  >", True, (0, 0, 0))
        self.screen.blit(item, (self.x, self.y))

        menu_length_calc = 0
        if self.size >= self.max_length:
            menu_length_calc = self.max_length
        elif self.size < self.max_length:
            menu_length_calc = self.size

        for option in range(menu_length_calc):
            item = my_font.render(self.currently_displayed_items[option], True, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + self.y_spacing + (option * self.menu_spread)))

        self.display_cursor()

    def choose_option(self):
        chosen_item = self.get_current_menu_item()
        if chosen_item == "Exit":
            self.exit_all_menus()
        else:
            self.gd_input.menu_list[UseMenu.NAME].set_menu()

    def do_option(self, choice=None):
        menu_selection = choice

        if menu_selection == "Use":
            self.gd_input.key_item_list[self.get_current_menu_item()].use_item()
            self.exit_all_menus()

        elif menu_selection == "Toss":
            self.gc_input.update_game_dialogue("You cannot toss a Key Item")
            self.gc_input.update_game_dialogue("Then why is it an option..?")
            self.exit_all_menus()

        elif menu_selection == "Exit":
            self.exit_all_menus()

    def cursor_left(self):
        self.exit_menu()
        self.gd_input.menu_list[InventoryMenu.NAME].set_menu()

    def cursor_right(self):
        self.exit_menu()
        self.gd_input.menu_list[InventoryMenu.NAME].set_menu()

    def exit_menu(self):
        self.gc_input.inventory.reset_bag_slot()
        self.reset_cursor()
        self.gc_input.menu_manager.deactivate_menu(self.name)

    def update_menu_items_list(self):
        self.menu_item_list = sorted(self.gc_input.inventory.current_key_items)
        self.menu_item_list.append("Exit")
        self.update_currently_displayed()

    def update_currently_displayed(self):
        self.currently_displayed_items = []
        if self.size <= self.max_length:
            for item in range(self.size):
                self.currently_displayed_items.append(self.menu_item_list[item + self.list_shifts])
        else:
            for item in range(self.max_length):
                self.currently_displayed_items.append(self.menu_item_list[item + self.list_shifts])

    def cursor_down(self):

        if self.size > 1:
            if (self.cursor_at + self.list_shifts) < self.size - 1:
                if self.size > self.max_length:
                    if self.cursor_at == self.max_length - 1:
                        self.list_shifts += 1
                        self.update_currently_displayed()
                    elif self.cursor_at < self.max_length - 1:
                        self.cursor_at += 1
                    else:
                        pass

                elif self.max_length >= self.size > self.cursor_at:
                    self.cursor_at += 1

    def cursor_up(self):
        if (self.cursor_at + self.list_shifts) > 0:
            if self.cursor_at == 0 and self.list_shifts > 0:
                self.list_shifts -= 1
                self.update_currently_displayed()
            elif self.cursor_at > 0:
                self.cursor_at -= 1
            else:
                pass

    def get_current_menu_item(self):
        menu_selection = self.currently_displayed_items[self.cursor_at]
        return menu_selection

    def reset_cursor(self):
        self.cursor_at = 0
        self.list_shifts = 0


class ToDoListMenu(MenuTemporary):
    NAME = "to_do_list_menu"
    OVERLAYNAME = "to_do_list_menu_overlay"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.menu_item_list = ["say hi to your mom", "kiss your cat", "eat a pear", "say hi to your mom", "kiss your cat", "eat a pear", "say hi to your mom", "kiss your cat", "eat a pear", "say hi to your mom", "kiss your cat", "eat a pear"]
        gd_input.add_overlay(self.OVERLAYNAME, Overlay(gc_input, gd_input, self.OVERLAYNAME, 350, 200, Spritesheet("assets/misc_sprites/to_do_list.png", 300, 400)))
        self.overlay = self.OVERLAYNAME
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(self.menu_item_list[option], True, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))
        self.display_cursor()

    def do_option(self):
        self.exit_all_menus()

    def choose_option(self):
        self.do_option()

        
class ProfileMenu(MenuTemporary):
    NAME = "profile_menu_2"
    OVERLAYNAME = "profile_menu_overlay"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        gd_input.add_overlay(self.OVERLAYNAME, Overlay(gc_input, gd_input, self.OVERLAYNAME, 350, 300, Spritesheet("assets/misc_sprites/ID.png", 300, 200)))
        self.overlay = self.OVERLAYNAME
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()
        self.screen.blit(self.gd_input.player["Player"].spritesheet.get_image(0, 0), (self.x + 27, self.y + 30))

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render("Name: Shuma", True, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.x +125, self.y + 40))

        item2 = my_font.render("Reputation: ", True, (0, 0, 0))
        self.gc_input.screen.blit(item2, (self.x + 125, self.y + 60))

    def do_option(self):
        self.exit_all_menus()

    def choose_option(self):
        self.do_option()


class MapMenu(MenuTemporary):
    NAME = "map_menu"
    OVERLAYNAME = "map_menu_overlay"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        gd_input.add_overlay(self.OVERLAYNAME, Overlay(gc_input, gd_input, self.OVERLAYNAME, 250, 200, Spritesheet("assets/menu_images/hornby_map.png", 500, 400)))
        self.overlay = self.OVERLAYNAME
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()

    def do_option(self):
        self.exit_all_menus()

    def choose_option(self):
        self.do_option()


# Additional Type Menus
class UseMenu(MenuTemporary):
    NAME = "use_menu"
    OVERLAYNAME = "use_menu"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.menu_item_list = ["Use", "Toss"]
        self.menu_item_list.append("Exit")
        gd_input.add_overlay(self.OVERLAYNAME, Overlay(gc_input, gd_input, self.OVERLAYNAME, 590, 200, Spritesheet("assets/menu_images/use_menu.png", 100, 100)))
        self.overlay = self.OVERLAYNAME
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "additional"

    def set_menu(self):
        self.update_menu_items_list()
        self.gc_input.set_keyboard_manager(InMenu.ID)
        self.gc_input.menu_manager.add_menu_to_stack(self.name)

    def choose_option(self):
        menu_selection = self.gd_input.menu_list[self.name].get_current_menu_item()

        if menu_selection == "Use":
            self.gd_input.menu_list[YesNoMenu.NAME].set_menu()

        elif menu_selection == "Toss":
            self.gd_input.menu_list[YesNoMenu.NAME].set_menu()

        elif menu_selection == "Exit":
            self.exit_all_menus()

    def do_option(self):
        menu_selection = self.gd_input.menu_list[self.name].get_current_menu_item()

        if menu_selection == "Use":
            self.exit_menu()
            self.gd_input.menu_list[self.gc_input.menu_manager.menu_stack[0]].do_option(menu_selection)

        elif menu_selection == "Toss":
            self.exit_menu()
            self.gd_input.menu_list[self.gc_input.menu_manager.menu_stack[0]].do_option(menu_selection)


class YesNoMenu(MenuTemporary):
    NAME = "yes_no_menu"
    OVERLAYNAME = "yes_no_menu"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.menu_item_list = ["Yes", "No"]
        gd_input.add_overlay(self.OVERLAYNAME, Overlay(gc_input, gd_input, self.OVERLAYNAME, 490, 200, Spritesheet("assets/menu_images/yes_no_menu.png", 90, 76)))
        self.overlay = self.OVERLAYNAME
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "additional"

    def set_menu(self):
        self.update_menu_items_list()
        self.gc_input.set_keyboard_manager(InMenu.ID)
        self.gc_input.menu_manager.add_menu_to_stack(self.name)

    def choose_option(self):
        menu_selection = self.gd_input.menu_list[self.name].get_current_menu_item()

        if menu_selection == "Yes":
            self.exit_menu()
            self.gd_input.menu_list[self.gc_input.menu_manager.menu_stack[0]].do_option()

        elif menu_selection == "No":
            self.exit_menu()
            self.gd_input.menu_list[self.gc_input.menu_manager.menu_stack[0]].exit_all_menus()


# Character Interaction Menus
class ConversationOptionsMenu(MenuTemporary):
    NAME = "conversation_options_menu_2"
    OVERLAYNAME = "conversation_options_text_box"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.menu_item_list = ["Talk", "Give Gift"]
        gd_input.add_overlay(self.OVERLAYNAME, TextBox(gc_input, gd_input, self.OVERLAYNAME, 250, 525, Spritesheet("assets/menu_images/text_box.png", 500, 150)))
        self.overlay = self.OVERLAYNAME
        self.talking_to = None
        self.menu_item_list.append("Exit")
        self.offset_x = 150
        self.offset_y = 25
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.y_spacing = 25
        self.menu_type = "base"

    def set_talking_to(self, talking_to):
        self.talking_to = talking_to

    def unset_talking_to(self):
        self.talking_to = None

    def display_menu(self):
        # Display Overlay
        self.gd_input.overlay_list[self.overlay].display_overlay()

        # Display speakers name
        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render(self.gd_input.character_list[self.talking_to].name + ":", True, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.x, self.y))

        # Display Dialogue Options
        text_line = 1
        for option in range(self.size):
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(self.menu_item_list[option], True, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + self.y_spacing * text_line))
            text_line += 1
        self.display_cursor()
        text_line = 1

        # Displays characters photo
        self.gc_input.screen.blit(self.gd_input.character_list[self.talking_to].face_image, (self.gd_input.overlay_list[self.overlay].x,  self.gd_input.overlay_list[self.overlay].y+2))

    def do_option(self):
        menu_selection = self.gd_input.menu_list[self.name].get_current_menu_item()
        if menu_selection == "Talk":
            self.gd_input.menu_list[CharacterDialogue.NAME].set_menu(self.talking_to, self.gd_input.character_list[self.talking_to].phrase)

        elif menu_selection == "Give Gift":
            self.gd_input.menu_list[GiftingMenu.NAME].set_menu()

        elif menu_selection == "Exit":
            self.exit_all_menus()

    def set_menu(self, person_talking_to):
        self.update_menu_items_list()
        self.gc_input.set_keyboard_manager(InMenu.ID)

        self.gc_input.menu_manager.add_menu_to_stack(self.name)
        self.set_talking_to(person_talking_to)

    def give_item(self, item):
        self.gc_input.inventory.unget_item(item, 1)
        self.gc_input.update_game_dialogue("You gave " + self.talking_to + " 1 " + item)
        self.gd_input.menu_list[CharacterDialogue.NAME].set_menu(self.talking_to, self.gd_input.character_list[self.talking_to].phrase_thanks)

    def exit_menu(self):
        self.gd_input.character_list[self.talking_to].set_state("idle")
        self.unset_talking_to()
        self.reset_cursor()
        self.gc_input.menu_manager.deactivate_menu(self.name)


class CharacterDialogue(MenuTemporary):
    NAME = "character_dialogue"
    OVERLAYNAME = "dialogue_text_box"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        gd_input.add_overlay(self.OVERLAYNAME, TextBox(gc_input, gd_input, self.OVERLAYNAME, 250, 525, Spritesheet("assets/menu_images/text_box.png", 500, 150)))
        self.overlay = self.OVERLAYNAME
        self.offset_x = 150
        self.offset_y = 25
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_item_list = "Something strange is going on around here, have you heard about the children disapearing? Their parents couldn't even remember their names..."
        self.current_phrase = []
        self.speaking_queue = []
        self.menu_photo = Spritesheet("assets/NPC_sprites/faces/DonnaFace.png", 150, 150).get_image(0, 0)
        self.menu_go = True
        self.y_spacing = 25

        self.set_current_phrase()
        self.talking_to = None
        self.menu_type = "base"

    def update_menu_items_list(self, phrases):
        self.menu_item_list = phrases

    def set_current_phrase(self):
        self.current_phrase = textwrap.wrap(self.menu_item_list, width=30)

    def set_speaking_queue(self):
        phrase_counter = 0
        self.speaking_queue = []

        if len(self.current_phrase) > 2:
            for line in range(3):
                self.speaking_queue.append(self.current_phrase[0])
                self.current_phrase.pop(0)

        elif (len(self.current_phrase) <= 2) and (len(self.current_phrase) > 0):
            for line in range(len(self.current_phrase)):
                self.speaking_queue.append(self.current_phrase[0])
                self.current_phrase.pop(0)

        elif len(self.current_phrase) == 0:
            self.exit_all_menus()

    @property
    def size(self):
        return len(self.menu_item_list)

    def display_menu(self):
        # prints the dialgue text box
        self.gd_input.overlay_list[self.overlay].display_overlay()

        # Display characters name
        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render(self.gd_input.character_list[self.talking_to].name + ":", True, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.x,  self.y))

        # Displays characters dialogue
        text_line = 1
        for line in self.speaking_queue:
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(line, True, (0, 0, 0))
            self.gc_input.screen.blit(item, (self.x,  self.y + self.y_spacing * text_line))
            text_line += 1

        # Displays characters photo
        self.gc_input.screen.blit(self.gd_input.character_list[self.talking_to].face_image, (self.gd_input.overlay_list[self.overlay].x, self.gd_input.overlay_list[self.overlay].y+2))

    def exit_menu(self):
        self.gc_input.menu_manager.deactivate_menu(self.name)

    def set_menu(self, talking_to, phrase):
        self.talking_to = talking_to
        self.update_menu_items_list(phrase)
        self.set_current_phrase()
        self.set_speaking_queue()
        self.gc_input.menu_manager.add_menu_to_stack(self.name)
        self.gc_input.set_keyboard_manager(InMenu.ID)

    def cursor_down(self):
        pass

    def cursor_up(self):
        pass

    def choose_option(self):
        self.do_option()

    def do_option(self):
        self.set_speaking_queue()


class GiftingMenu(MenuTemporary):
    NAME = "gift_menu_2"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.y_spacing = 20
        self.max_length = 14
        self.menu_item_list = gc_input.inventory.current_items
        gd_input.add_overlay("gifting_menu_overlay", Overlay(gc_input, gd_input, "gifting_menu_overlay", 700, 200, Spritesheet("assets/menu_images/inventory_menu.png", 200, 400)))
        self.overlay = "gifting_menu_overlay"
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"
        self.currently_displayed_items = None
        self.list_shifts = 0

    def update_menu_items_list(self):
        self.menu_item_list = sorted(self.gc_input.inventory.current_items)
        self.menu_item_list.append("Exit")
        self.update_currently_displayed()

    def update_currently_displayed(self):
        self.currently_displayed_items = []
        if self.size <= self.max_length:
            for item in range(self.size):
                self.currently_displayed_items.append(self.menu_item_list[item + self.list_shifts])
        else:
            for item in range(self.max_length):
                self.currently_displayed_items.append(self.menu_item_list[item + self.list_shifts])

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render("     ITEMS     ", True, (0, 0, 0))
        self.screen.blit(item, (self.x, self.y))

        menu_length_calc = 0
        if self.size >= self.max_length:
            menu_length_calc = self.max_length
        elif self.size < self.max_length:
            menu_length_calc = self.size

        for option in range(menu_length_calc):
            if self.currently_displayed_items[option] == "Exit":
                item = my_font.render(self.currently_displayed_items[option], True, (0, 0, 0))
                self.screen.blit(item, (self.x, self.y + self.y_spacing + (option * self.menu_spread)))

            else:
                item = my_font.render(self.currently_displayed_items[option], True, (0, 0, 0))
                self.screen.blit(item, (self.x, self.y + self.y_spacing + (option * self.menu_spread)))

                spacing = 0
                if len(str(self.gd_input.item_list[self.currently_displayed_items[option]].quantity)) == 3:
                    spacing = 110
                elif len(str(self.gd_input.item_list[self.currently_displayed_items[option]].quantity)) == 2:
                    spacing = 120
                else:
                    spacing = 130

                item = my_font.render("x" + str(self.gd_input.item_list[self.currently_displayed_items[option]].quantity), True, (0, 0, 0))
                self.screen.blit(item, (self.x + spacing, self.y + self.y_spacing + (option * self.menu_spread)))

        self.display_cursor()

    def choose_option(self):
        chosen_item = self.get_current_menu_item()
        if chosen_item == "Exit":
            self.exit_all_menus()
        else:
            self.gd_input.menu_list[YesNoMenu.NAME].set_menu()

    def do_option(self):
        chosen_item = self.get_current_menu_item()
        self.exit_menu()
        self.gd_input.menu_list[self.gc_input.menu_manager.menu_stack[0]].give_item(chosen_item)

    def cursor_down(self):

        if self.size > 1:
            if (self.cursor_at + self.list_shifts) < self.size -1:
                if self.size > self.max_length:
                    if self.cursor_at == self.max_length - 1:
                        self.list_shifts += 1
                        self.update_currently_displayed()
                    elif self.cursor_at < self.max_length - 1:
                        self.cursor_at += 1
                    else:
                        pass

                elif self.max_length >= self.size > self.cursor_at:
                    self.cursor_at += 1

    def cursor_up(self):
        if (self.cursor_at + self.list_shifts) > 0:
            if self.cursor_at == 0 and self.list_shifts > 0:
                self.list_shifts -= 1
                self.update_currently_displayed()
            elif self.cursor_at > 0:
                self.cursor_at -= 1
            else:
                pass
        
    def get_current_menu_item(self):
        menu_selection = self.currently_displayed_items[self.cursor_at]
        return menu_selection

    def reset_cursor(self):
        self.cursor_at = 0
        self.list_shifts = 0


class ShopkeeperDialogue(CharacterDialogue):
    NAME = "shopkeeper_dialogue"
    OVERLAYNAME = "shopkeeper_dialogue_text_box"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)

    def set_speaking_queue(self):
        phrase_counter = 0
        self.speaking_queue = []

        if len(self.current_phrase) > 2:
            for line in range(3):
                self.speaking_queue.append(self.current_phrase[0])
                self.current_phrase.pop(0)

        elif (len(self.current_phrase) <= 2) and (len(self.current_phrase) > 0):
            for line in range(len(self.current_phrase)):
                self.speaking_queue.append(self.current_phrase[0])
                self.current_phrase.pop(0)

        elif len(self.current_phrase) == 0:
            self.gd_input.menu_list[ShopKeeperInteractMenu.NAME].set_menu(self.talking_to)


    def exit_menu(self):
        self.gc_input.menu_manager.deactivate_menu(self.name)

    def set_menu(self, talking_to, phrase):
        self.talking_to = talking_to
        self.update_menu_items_list(phrase)
        self.set_current_phrase()
        self.set_speaking_queue()
        self.gc_input.menu_manager.add_menu_to_stack(self.name)
        self.gc_input.set_keyboard_manager(InMenu.ID)

    def cursor_down(self):
        pass

    def cursor_up(self):
        pass

    def choose_option(self):
        self.do_option()

    def do_option(self):
        self.set_speaking_queue()


class ShopKeeperInteractMenu(MenuTemporary):
    NAME = "shopkeeper_interact_menu"
    OVERLAYNAME = "shopkeeper_interact_menu_text_box"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.menu_item_list = ["Buy", "Sell"]
        self.talking_to = None
        self.menu_item_list.append("Exit")
        self.offset_x = 150
        self.offset_y = 25
        gd_input.add_overlay(self.OVERLAYNAME, TextBox(gc_input, gd_input, self.OVERLAYNAME, 250, 525, Spritesheet("assets/menu_images/text_box.png", 500, 150)))
        self.overlay = self.OVERLAYNAME
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.y_spacing = 25
        self.menu_type = "base"

    def set_talking_to(self, talking_to):
        self.talking_to = talking_to

    def set_menu(self, person_talking_to):
        self.update_menu_items_list()
        self.gc_input.set_keyboard_manager(InMenu.ID)
        self.gc_input.menu_manager.add_menu_to_stack(self.name)
        self.set_talking_to(person_talking_to)

    def display_menu(self):
        # Display Overlay
        self.gd_input.overlay_list[self.overlay].display_overlay()

        # Display speakers name
        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render(self.gd_input.character_list[self.talking_to].name + ":", True, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.x, self.y))

        # Display Dialogue Options
        text_line = 1
        for option in range(self.size):
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(self.menu_item_list[option], True, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + self.y_spacing * text_line))
            text_line += 1
        self.display_cursor()
        text_line = 1

        # Displays characters photo
        self.gc_input.screen.blit(self.gd_input.character_list[self.talking_to].face_image, (self.gd_input.overlay_list[self.overlay].x,  self.gd_input.overlay_list[self.overlay].y+2))

    def choose_option(self):
        self.do_option()

    def do_option(self):
        menu_selection = self.get_current_menu_item()

        if menu_selection == "Buy":
            self.gd_input.menu_list[BuyingMenu.NAME].set_menu(self.talking_to)

        elif menu_selection == "Sell":
            self.gd_input.menu_list[SellingMenu.NAME].set_menu(self.talking_to)

        elif menu_selection == "Exit":
            self.gd_input.character_list[self.talking_to].set_state("idle")
            self.exit_menu()

    def unset_talking_to(self):
        self.talking_to = None

    def exit_menu(self):
        self.gd_input.character_list[self.talking_to].set_state("idle")
        self.unset_talking_to()
        self.reset_cursor()
        self.gc_input.menu_manager.deactivate_menu(self.name)


class BuyingMenu(MenuTemporary):
    NAME = "buying_menu"
    OVERLAYNAME = "buying_menu_overlay"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        gd_input.add_overlay(self.OVERLAYNAME, Overlay(gc_input, gd_input, self.OVERLAYNAME, 700, 200, Spritesheet("assets/menu_images/inventory_menu.png", 200, 400)))
        self.overlay = self.OVERLAYNAME
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"
        self.talking_to = None

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render("$    SHOP    $", True, (0, 0, 0))
        self.screen.blit(item, (self.x, self.y))

        for option in range(self.size-1):
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(self.menu_item_list[option][0], True, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + 20 + (option * self.menu_spread)))

            item = my_font.render("$" + str(self.menu_item_list[option][1]), True, (0, 0, 0))
            self.screen.blit(item, (self.x + 140 - (10 * len(str(self.menu_item_list[option][1]))), self.y +20 + (option * self.menu_spread)))

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render(self.menu_item_list[self.size-1][0], True, (0, 0, 0))
        self.screen.blit(item, (self.x, self.y + 20 + ((self.size-1) * self.menu_spread)))

        self.display_cursor()

    def choose_option(self):
        self.do_option()

    def do_option(self):
        if self.try_buy_item():
            self.exit_all_menus()
        else:
            self.exit_all_menus()

    def display_cursor(self):
        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render("-", True, (0, 0, 0))
        self.screen.blit(item, (self.x - 15, (self.y + 2 + 20) + (self.cursor_at * self.menu_spread)))

    def try_buy_item(self):
        success = False
        menu_selection = self.gd_input.menu_list[self.name].get_current_menu_item()
        if menu_selection[0] == "Exit":
            self.exit_all_menus()

        elif self.gc_input.your_coins >= menu_selection[1]:
            try_buy = self.gc_input.try_use_coins(menu_selection[1])
            if try_buy:
                self.gc_input.inventory.get_item(menu_selection[0], 1)
                self.gc_input.update_game_dialogue("You bought 1 " + menu_selection[0])
                success = True
            else:
                success = False
                self.gc_input.update_game_dialogue("You can't afford 1 " + menu_selection[0])
        else:
            success = False
            self.gc_input.update_game_dialogue("You can't afford 1 " + menu_selection[0])
        return success

    def set_menu(self, person_talking_to):
        self.talking_to = person_talking_to
        self.update_menu_items_list()
        self.gc_input.set_keyboard_manager(InMenu.ID)
        self.gc_input.menu_manager.add_menu_to_stack(self.name)

    def update_menu_items_list(self):
        self.menu_item_list = self.gd_input.character_list[self.talking_to].items_list.copy()
        self.menu_item_list.append(("Exit", "-"))

    def unset_talking_to(self):
        self.talking_to = None

    def exit_menu(self):
        self.unset_talking_to()
        self.reset_cursor()
        self.gc_input.menu_manager.deactivate_menu(self.name)


class SellingMenu(MenuTemporary):
    NAME = "selling_menu_2"
    OVERLAYNAME = "selling_menu_overlay"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        self.menu_item_list = gc_input.inventory.current_items
        self.talking_to = None
        self.y_spacing = 20
        self.max_length = 14
        gd_input.add_overlay(self.OVERLAYNAME, Overlay(gc_input, gd_input, self.OVERLAYNAME, 700, 200, Spritesheet("assets/menu_images/inventory_menu.png", 200, 400)))
        self.overlay = self.OVERLAYNAME
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"

    def set_talking_to(self, talking_to):
        self.talking_to = talking_to

    def set_menu(self, person_talking_to):
        self.update_menu_items_list()
        self.gc_input.set_keyboard_manager(InMenu.ID)
        self.gc_input.menu_manager.add_menu_to_stack(self.name)
        self.set_talking_to(person_talking_to)

    def update_menu_items_list(self):
        self.menu_item_list = sorted(self.gc_input.inventory.current_items)
        # TODO: Add exit to menu

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render("     ITEMS     ", True, (0, 0, 0))
        self.screen.blit(item, (self.x, self.y))

        menu_length_calc = 0
        if self.size >= self.max_length:
            menu_length_calc = self.max_length
        elif self.size < self.max_length:
            menu_length_calc = self.size

        for option in range(menu_length_calc):
            item = my_font.render(self.menu_item_list[option], True, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + self.y_spacing + (option * self.menu_spread)))

            spacing = 0
            if len(str(self.gd_input.item_list[self.menu_item_list[option]].sell_price)) == 3:
                spacing = 110
            elif len(str(self.gd_input.item_list[self.menu_item_list[option]].sell_price)) == 2:
                spacing = 120
            else:
                spacing = 130

            cost = my_font.render("$" + str(self.gd_input.item_list[self.menu_item_list[option]].sell_price), True, (0, 0, 0))
            self.screen.blit(cost, (self.x + spacing, self.y + self.y_spacing + (option * self.menu_spread)))
        self.display_cursor()

    def choose_option(self):
        self.gd_input.menu_list[YesNoMenu.NAME].set_menu()

    def do_option(self):
        current_item = self.get_current_menu_item()
        self.process_item_selection(current_item)
        self.exit_all_menus()

    def cursor_down(self):
        menu_length_calc = 0
        if self.size >= self.max_length:
            menu_length_calc = self.max_length
        elif self.size < self.max_length:
            menu_length_calc = self.size

        if self.size > self.max_length and self.cursor_at == self.max_length - 1 and self.size > 1:
            self.menu_item_list.append(self.menu_item_list.pop(0))

        elif self.cursor_at == menu_length_calc - 1:
            pass

        elif self.size > 1:
            self.cursor_at += 1

        else:
            pass

    def cursor_up(self):

        if self.cursor_at == 0 and self.size > 1:
            self.menu_item_list.insert(0, self.menu_item_list.pop(self.max_length - 1))

        elif self.size > 1:
            self.cursor_at -= 1

        else:
            pass

    def process_item_selection(self, item):
        self.gc_input.inventory.unget_item(item, 1)
        self.gc_input.get_coins(self.gd_input.item_list[item].sell_price)
        self.gc_input.update_game_dialogue("You sold 1 " + item + " for $" + str(self.gd_input.item_list[item].sell_price))

    def unset_talking_to(self):
        self.talking_to = None

    def exit_menu(self):
        self.unset_talking_to()
        self.reset_cursor()
        self.gc_input.menu_manager.deactivate_menu(self.name)


class OutfitsMenu(MenuTemporary):
    NAME = "outfits_menu"
    OVERLAYNAME = "outfits_menu_overlay"

    def __init__(self, gc_input, gd_input):
        super().__init__(gc_input, gd_input)
        gd_input.add_overlay(self.OVERLAYNAME, Overlay(gc_input, gd_input, self.OVERLAYNAME, 350, 300, Spritesheet("assets/menu_images/testing_menu2.png", 300, 100)))
        self.overlay = self.OVERLAYNAME
        self.offset_x = 150
        self.offset_y = 25
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_item_list = []
        self.menu_type = "base"
        self.all_outfits = []
        self.current_outfits =[]
        self.display_size = 3
        self.currently_selected_outfit = None
        self.current_outfit_number = 0
        self.currently_wearing = "Normal Outfit"

    def get_outfits(self):
        for image in self.gd_input.outfit_list:
            self.all_outfits.append(self.gd_input.outfit_list[image].name)
        self.currently_selected_outfit = self.currently_wearing
        self.current_outfit_number = self.all_outfits.index(self.currently_selected_outfit)
        self.get_current_outfits(self.current_outfit_number)

    def get_current_outfits(self, current_outfit_number):
        self.current_outfit_number = current_outfit_number
        self.current_outfits.clear()
        if self.current_outfit_number == 0:
            left_outfit = self.all_outfits[len(self.all_outfits)-1]
            center_outfit = self.all_outfits[self.current_outfit_number]
            right_outfit = self.all_outfits[self.current_outfit_number + 1]

        elif self.current_outfit_number == len(self.all_outfits)-1:
            left_outfit = self.all_outfits[self.current_outfit_number - 1]
            center_outfit = self.all_outfits[self.current_outfit_number]
            right_outfit = self.all_outfits[0]

        else:
            left_outfit = self.all_outfits[self.current_outfit_number - 1]
            center_outfit = self.all_outfits[self.current_outfit_number]
            right_outfit = self.all_outfits[self.current_outfit_number + 1]

        self.current_outfits.append(left_outfit)
        self.current_outfits.append(center_outfit)
        self.current_outfits.append(right_outfit)
        self.currently_selected_outfit = center_outfit

    @property
    def size(self):
        return len(self.menu_item_list)

    def display_menu(self):
        # prints the dialgue text box
        self.gd_input.overlay_list[self.overlay].display_overlay()

        # Display outfit title
        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render("Outfits", True, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.x-35,  self.y-15))

        my_font = pygame.font.Font(self.gc_input.font, 8)
        item = my_font.render("<                                >", True, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.x - 135, self.y + 25))

        my_font = pygame.font.Font(self.gc_input.font, 8)
        item = my_font.render("^", True, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.x - 3 , self.y + 58))

        step = 0
        for image in self.current_outfits:
            self.gc_input.screen.blit(self.gd_input.outfit_list[image].display_pic, ((self.x - 100) + step * 85, self.y + 10))
            step += 1
            if step == 4:
                step = 0

    def exit_menu(self):
        self.gc_input.menu_manager.deactivate_menu(self.name)

    def set_menu(self):
        self.update_menu_items_list()
        self.gc_input.set_keyboard_manager(InMenu.ID)
        self.gc_input.menu_manager.add_menu_to_stack(self.name)
        self.get_outfits()


    def cursor_down(self):
        pass

    def cursor_up(self):
        pass

    def cursor_left(self):
        if self.current_outfit_number == 0:
            self.current_outfit_number = len(self.all_outfits) -1
        else:
            self.current_outfit_number -= 1
        self.get_current_outfits(self.current_outfit_number)

    def cursor_right(self):
        if self.current_outfit_number == len(self.all_outfits) -1:
            self.current_outfit_number = 0
        else:
            self.current_outfit_number += 1
        self.get_current_outfits(self.current_outfit_number)

    def choose_option(self):
        self.do_option()

    def do_option(self):
        self.currently_wearing = self.currently_selected_outfit
        self.gd_input.outfit_list[self.currently_selected_outfit].wear_outfit()
        self.exit_all_menus()
