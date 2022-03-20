import textwrap

import pygame

from keyboards import InGame, InMenu
from spritesheet import Spritesheet


class SubMenuManager(object):
    def __init__(self, gd_input, gc_input):
        self.gd_input = gd_input
        self.gc_input = gc_input
        self.static_menus = ["stats_menu2", "game_action_dialogue_menu_2"]
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
            self.gc_input.set_keyboard_manager(InGame.ID)

class Overlay2(object):
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

class TextBox2(Overlay2):
    def __init__(self, gc_input, gd_input, name, x, y, image):
        super().__init__(gc_input, gd_input, name, x, y, image)

    def display_phrase(self, character):
    # prints the speakers name
        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render(self.gd_input.character_list[character].name + ":", 1, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.gd_input.overlay_list["text_box"].x + 150, self.gd_input.overlay_list["text_box"].y + 20))

        # prints phrases to be spoke
        text_line = 0
        for line in self.gd_input.character_list[character].speaking_queue:
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(line, 1, (0, 0, 0))
            self.gc_input.screen.blit(item, (self.gd_input.overlay_list["text_box"].x + 150, self.gd_input.overlay_list["text_box"].y + 50 + 25 * text_line))
            text_line += 1

# Static Menus

class GameActionDialogue2(object):
    def __init__(self, gc_input, gd_input):
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.screen = self.gc_input.screen
        gd_input.add_overlay("game_dialogue_box_2", Overlay2(gc_input, gd_input, "game_dialogue_box_2", 780, 680, Spritesheet("assets/menu_images/testing_menu.png", 200, 100)))
        self.overlay = "game_dialogue_box_2"
        self.offset_x = 10
        self.offset_y = 20
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.name = "game_action_dialogue_menu_2"
        self.menu_item_list = ["This is the game dialouge box!"]
        self.menu_spread = 15
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
        print(self.menu_item_list)
        # self.display_menu()

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.gc_input.font, 6)
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))

class StaticMenu2(object):
    def __init__(self, gc_input, gd_input):
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.screen = self.gc_input.screen
        gd_input.add_overlay("stats_overlay2", Overlay2(gc_input, gd_input, "stats_overlay2", 800, 50, Spritesheet("assets/menu_images/use_menu.png", 100, 100)))
        self.overlay = "stats_overlay2"
        self.offset_x = 10
        self.offset_y = 20
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.name = "stats_menu2"
        self.menu_item_list = [("Coins: ", str(gc_input.your_coins)), ("Seeds:", str(gc_input.your_seeds)), ("Love: ", "100")]
        self.menu_spread = 25
        self.cursor_at = 0
        self.y_spacing = 0
        self.menu_type = "static"

    @property
    def size(self):
        return len(self.menu_item_list)

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(self.menu_item_list[option][0], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))

        for quantitity in range(self.size):
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(self.menu_item_list[quantitity][1], 1, (0, 0, 0))
            self.screen.blit(item, (self.x + 80 - (10 * len(self.menu_item_list[quantitity][1])), self.y + (quantitity * self.menu_spread)))
            
            
# Base Menus            
class NewMenu2(object):
    def __init__(self, gc_input, gd_input, name, menu_item_list):
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.screen = self.gc_input.screen
        self.overlay = None
        self.x = None
        self.y = None
        self.offset_x = 30
        self.offset_y = 20
        self.name = name
        self.menu_item_list = menu_item_list
        self.menu_spread = 25
        self.cursor_at = 0
        self.y_spacing = 0

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
        item = my_font.render("-", 1, (0, 0, 0))
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
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))
        self.display_cursor()

    def choose_option(self):
        self.do_option()

    def do_option(self):
        pass

    def try_to_exit(self):
        pass
    
        
class StartMenu2(NewMenu2):
    def __init__(self, gc_input, gd_input, name, menu_item_list):
        super().__init__(gc_input, gd_input, name, menu_item_list)
        self.menu_item_list.append("Exit")
        self.menu_type = "base"
        gd_input.add_overlay("start_menu_2", Overlay2(gc_input, gd_input, "start_menu_2", 700, 200, Spritesheet("assets/menu_images/start_menu.png", 150, 400)))
        self.overlay = "start_menu_2"
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"

    def do_option(self):
        menu_selection = self.get_current_menu_item()

        if menu_selection == "Bag":
            self.gd_input.menu_list["inventory_menu_2"].set_menu()

        elif menu_selection == "Key Items":
            self.gd_input.menu_list["key_inventory_menu"].set_menu()

        elif menu_selection == "Chore List":
            self.gd_input.menu_list["to_do_list_menu_2"].set_menu()

        elif menu_selection == "Profile":
            self.gd_input.menu_list["profile_menu_2"].set_menu()

        elif menu_selection == "Exit":
            self.exit_menu()

        elif menu_selection == "Outfits":
            # TODO: Add outfit selection
            self.gc_input.update_game_dialogue("You have no other outfits")
            self.exit_menu()

        elif menu_selection == "Save":
            self.gc_input.update_game_dialogue("You saved the game!")
            self.exit_menu()

        else:
            self.exit_menu()
        self.exit_menu()

    def choose_option(self):
        self.do_option()


# Menus' from Start Menu
class InventoryMenu2(NewMenu2):
    def __init__(self, gc_input, gd_input, name, menu_item_list):
        super().__init__(gc_input, gd_input, name, menu_item_list)
        self.y_spacing = 20
        self.max_length = 14
        gd_input.add_overlay("inventory_menu_2", Overlay2(gc_input, gd_input, "inventory_menu_2", 700, 200, Spritesheet("assets/menu_images/inventory_menu.png", 200, 400)))
        self.overlay = "inventory_menu_2"
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"

    def update_menu_items_list(self):
        self.menu_item_list = sorted(self.gc_input.inventory.current_items)
        # TODO: Add exit to menu

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render("<    ITEMS    >", 1, (0, 0, 0))
        self.screen.blit(item, (self.x, self.y))

        menu_length_calc = 0
        if self.size >= self.max_length:
            menu_length_calc = self.max_length
        elif self.size < self.max_length:
            menu_length_calc = self.size

        for option in range(menu_length_calc):
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + self.y_spacing + (option * self.menu_spread)))

            spacing = 0
            if len(str(self.gd_input.item_list[self.menu_item_list[option]].quantity)) == 3:
                spacing = 110
            elif len(str(self.gd_input.item_list[self.menu_item_list[option]].quantity)) == 2:
                spacing = 120
            else:
                spacing = 130

            item = my_font.render("x" + str(self.gd_input.item_list[self.menu_item_list[option]].quantity), 1, (0, 0, 0))
            self.screen.blit(item, (self.x + spacing, self.y + self.y_spacing + (option * self.menu_spread)))
        self.display_cursor()

    def choose_option(self):
        self.gd_input.menu_list["use_menu_2"].set_menu()

    def do_option(self, choice=None):
        menu_selection = choice
        print("menu_selection")

        if menu_selection == "Use":
            self.gd_input.item_list[self.get_current_menu_item()].use_item()
            self.gc_input.inventory.reset_bag_slot()
            self.exit_menu()

        elif menu_selection == "Toss":
            print("You tossed out the " + str(self.get_current_menu_item()) + "!")
            self.gc_input.inventory.reset_bag_slot()
            self.exit_menu()

        elif menu_selection == "Exit":
            self.gc_input.inventory.reset_bag_slot()
            self.exit_menu()

    def do_not_do_option(self):
        self.gc_input.inventory.reset_bag_slot()
        self.exit_menu()

    def cursor_down(self):
        menu_length_calc = 0
        if self.size >= self.max_length:
            menu_length_calc = self.max_length
        elif self.size < self.max_length:
            menu_length_calc = self.size

        if self.size > self.max_length and self.cursor_at == self.max_length -1 and self.size > 1:
            self.menu_item_list.append(self.menu_item_list.pop(0))

        elif self.cursor_at == menu_length_calc - 1:
            pass

        elif self.size > 1:
            self.cursor_at += 1

        else:
            pass

    def cursor_up(self):
        menu_length_calc = 0
        if self.size >= self.max_length:
            menu_length_calc = self.max_length
        elif self.size < self.max_length:
            menu_length_calc = self.size

        if self.cursor_at == 0 and self.size > 1:
            self.menu_item_list.insert(0, self.menu_item_list.pop(self.max_length-1))

        elif self.size > 1:
            self.cursor_at -= 1

        else:
            pass

    def cursor_left(self):
        self.reset_cursor()
        self.update_menu_items_list()
        self.gc_input.inventory.bag_slot_left()

    def cursor_right(self):
        self.reset_cursor()
        self.update_menu_items_list()
        self.gc_input.inventory.bag_slot_right()


class KeyInventoryMenu2(NewMenu2):
    def __init__(self, gc_input, gd_input, name, menu_item_list):
        super().__init__(gc_input, gd_input, name, menu_item_list)
        self.y_spacing = 20
        gd_input.add_overlay("key_inventory_menu_2", Overlay2(gc_input, gd_input, "key_inventory_menu_2", 700, 200, Spritesheet("assets/menu_images/inventory_menu.png", 200, 400)))
        self.overlay = "key_inventory_menu_2"
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render("<  KEY ITEMS  >", 1, (0, 0, 0))
        self.screen.blit(item, (self.x, self.y))

        for option in range(self.size):
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + self.y_spacing + (option * self.menu_spread)))

        self.display_cursor()

    def choose_option(self):
        self.gd_input.menu_list["use_menu_2"].set_menu()

    def do_option(self, choice=None):
        menu_selection = choice

        if menu_selection == "Use":
            self.gd_input.key_item_list[self.get_current_menu_item()].use_key_item()
            self.gc_input.inventory.reset_bag_slot()
            self.exit_menu()

        elif menu_selection == "Toss":
            print("You tossed put the item")
            self.gc_input.inventory.reset_bag_slot()
            self.exit_menu()

        elif menu_selection == "Exit":
            self.gc_input.inventory.reset_bag_slot()
            self.exit_menu()

    def do_not_do_option(self):
        self.gc_input.inventory.reset_bag_slot()
        self.exit_menu()

    def cursor_left(self):
        self.reset_cursor()
        self.update_menu_items_list()
        self.gc_input.inventory.bag_slot_left()
        print("left")

    def cursor_right(self):
        self.reset_cursor()
        self.update_menu_items_list()
        self.gc_input.inventory.bag_slot_right()
        
        
class ToDoListMenu2(NewMenu2):
    def __init__(self, gc_input, gd_input, name, menu_item_list):
        super().__init__(gc_input, gd_input, name, menu_item_list)
        gd_input.add_overlay("to_do_list_menu_overlay_2", Overlay2(gc_input, gd_input, "to_do_list_menu_overlay_2", 350, 200, Spritesheet("assets/misc_sprites/to_do_list.png", 300, 400)))
        self.overlay = "to_do_list_menu_overlay_2"
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))
        self.display_cursor()

    def do_option(self):
        self.exit_menu()

    def choose_option(self):
        self.do_option()

        
class ProfileMenu2(NewMenu2):
    def __init__(self, gc_input, gd_input, name, menu_item_list):
        super().__init__(gc_input, gd_input, name, menu_item_list)
        gd_input.add_overlay("profile_menu_overlay_2", Overlay2(gc_input, gd_input, "profile_menu_overlay_2", 350, 300, Spritesheet("assets/misc_sprites/ID.png", 300, 200)))
        self.overlay = "profile_menu_overlay_2"
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()
        self.screen.blit(self.gd_input.player["Player"].spritesheet.get_image(0, 0),( self.x + 27, self.y + 30))

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render("Name: Shuma", 1, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.x +125, self.y + 40))

        item2 = my_font.render("Reputation: ", 1, (0, 0, 0))
        self.gc_input.screen.blit(item2, (self.x + 125, self.y + 60))

    def do_option(self):
        self.exit_menu()

    def choose_option(self):
        self.do_option()


# Additional Type Menus
class UseMenu2(NewMenu2):
    def __init__(self, gc_input, gd_input, name, menu_item_list):
        super().__init__(gc_input, gd_input, name, menu_item_list)
        self.menu_item_list.append("Exit")
        gd_input.add_overlay("use_menu_2", Overlay2(gc_input, gd_input, "use_menu_2", 590, 200, Spritesheet("assets/menu_images/use_menu.png", 100, 100)))
        self.overlay = "use_menu_2"
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
            self.gd_input.menu_list["yes_no_menu_2"].set_menu()

        elif menu_selection == "Toss":
            self.gd_input.menu_list["yes_no_menu_2"].set_menu()


        elif menu_selection == "Exit":
            self.exit_menu()
            self.gd_input.menu_list[self.gc_input.menu_manager.menu_stack[0]].do_not_do_option()


    def do_option(self):
        menu_selection = self.gd_input.menu_list[self.name].get_current_menu_item()

        if menu_selection == "Use":
            self.exit_menu()
            self.gd_input.menu_list[self.gc_input.menu_manager.menu_stack[0]].do_option(menu_selection)

        elif menu_selection == "Toss":
            self.exit_menu()
            self.gd_input.menu_list[self.gc_input.menu_manager.menu_stack[0]].do_option(menu_selection)

    def do_not_do_option(self):
        self.exit_menu()
        self.gd_input.menu_list[self.gc_input.menu_manager.menu_stack[0]].do_not_do_option()


class YesNoMenu2(NewMenu2):
    def __init__(self, gc_input, gd_input, name, menu_item_list):
        super().__init__(gc_input, gd_input, name, menu_item_list)
        gd_input.add_overlay("yes_no_menu_2", Overlay2(gc_input, gd_input, "yes_no_menu_2", 490, 200, Spritesheet("assets/menu_images/yes_no_menu.png", 90, 76)))
        self.overlay = "yes_no_menu_2"
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
            self.gd_input.menu_list[self.gc_input.menu_manager.menu_stack[0]].do_not_do_option()


# Character Interaction Menus
class ConversationOptionsMenu2(NewMenu2):
    def __init__(self, gc_input, gd_input, name, menu_item_list):
        super().__init__(gc_input, gd_input, name, menu_item_list)
        gd_input.add_overlay("conversation_options_text_box", TextBox2(gc_input, gd_input, "conversation_options_text_box", 250, 550, Spritesheet("assets/menu_images/text_box.png", 500, 150)))
        self.overlay = "conversation_options_text_box"
        self.talking_to = None
        self.menu_item_list.append("Exit")
        self.offset_x = 150
        self.offset_y = 25
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.y_spacing = 25
        self.menu_photo = Spritesheet("assets/NPC_sprites/faces/DonnaFace.png", 150, 150).get_image(0, 0)
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
        item = my_font.render(self.gd_input.character_list[self.talking_to].name + ":", 1, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.x, self.y))

        # Display Dialogue Options
        text_line = 1
        for option in range(self.size):
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + self.y_spacing * text_line))
            text_line += 1
        self.display_cursor()
        text_line = 1

        # Displays characters photo
        self.gc_input.screen.blit(self.gd_input.character_list[self.talking_to].face_image, (self.gd_input.overlay_list[self.overlay].x,  self.gd_input.overlay_list[self.overlay].y+2))

    def do_option(self):
        menu_selection = self.gd_input.menu_list[self.name].get_current_menu_item()
        if menu_selection == "Talk":
            self.exit_menu()
            self.gd_input.menu_list["character_dialogue_menu_2"].set_menu(self.talking_to, self.gd_input.character_list[self.talking_to].phrase)
            self.gd_input.menu_list[self.name].unset_talking_to()


        elif menu_selection == "Give Gift":

            self.gd_input.menu_list["gift_menu_2"].set_menu()

        elif menu_selection == "Exit":
            self.gd_input.character_list[self.talking_to].set_state("idle")
            self.gd_input.menu_list[self.name].unset_talking_to()
            self.gd_input.character_list[self.gd_input.player["Player"].check_adj_tile(self.gd_input.player["Player"].get_direct(self.gd_input.player["Player"].facing)).object_filling].set_state("idle")
            self.exit_menu()

    def do_not_do_option(self):
        self.gd_input.character_list[self.talking_to].set_state("idle")
        self.gd_input.menu_list[self.name].set_talking_to(None)
        self.exit_menu()

    def set_menu(self, person_talking_to):
        self.update_menu_items_list()
        self.gc_input.set_keyboard_manager(InMenu.ID)
        self.gc_input.menu_manager.add_menu_to_stack(self.name)
        self.set_talking_to(person_talking_to)


    def give_item(self, item):
        self.exit_menu()
        self.gc_input.inventory.unget_item(item, 1)
        self.gc_input.update_game_dialogue("You gave " + self.talking_to + " 1 " + item)
        self.gd_input.menu_list["character_dialogue_menu_2"].set_menu(self.talking_to, self.gd_input.character_list[self.talking_to].phrase_thanks)
        self.set_talking_to(None)


class CharacterDialogue2(object):
    def __init__(self, gc_input, gd_input):
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.screen = self.gc_input.screen
        gd_input.add_overlay("dialogue_text_box_2", TextBox2(gc_input, gd_input, "dialogue_text_box_2", 250, 550, Spritesheet("assets/menu_images/text_box.png", 500, 150)))
        self.overlay = "dialogue_text_box_2"
        self.offset_x = 150
        self.offset_y = 25
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.name = "character_dialogue_menu_2"
        self.menu_item_list = "Something strange is going on around here, have you heard about the children disapearing? Their parents couldn't even remember their names..."
        self.current_phrase = []
        self.speaking_queue = []
        self.menu_photo = Spritesheet("assets/NPC_sprites/faces/DonnaFace.png", 150, 150).get_image(0, 0)
        self.menu_go = True
        self.cursor_at = 0
        self.y_spacing = 25

        self.origin = None
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
            self.exit_menu()

    @property
    def size(self):
        return len(self.menu_item_list)

    def display_menu(self):
        # prints the dialgue text box
        self.gd_input.overlay_list[self.overlay].display_overlay()

        # Display characters name
        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render(self.gd_input.character_list[self.talking_to].name + ":", 1, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.x,  self.y))

        # Displays characters dialogue
        text_line = 1
        for line in self.speaking_queue:
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(line, 1, (0, 0, 0))
            self.gc_input.screen.blit(item, (self.x,  self.y + self.y_spacing * text_line))
            text_line += 1

        # Displays characters photo
        self.gc_input.screen.blit(self.gd_input.character_list[self.talking_to].face_image, (self.gd_input.overlay_list[self.overlay].x, self.gd_input.overlay_list[self.overlay].y+2))

    def exit_menu(self):
        self.gd_input.character_list[self.talking_to].set_state("idle")
        self.gc_input.set_speaker(None)
        self.gc_input.menu_manager.deactivate_menu(self.name)
        self.gc_input.set_keyboard_manager(InGame.ID)

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

    def cursor_left(self):
        pass

    def cursor_right(self):
        pass

    def choose_option(self):
        self.do_option()

    def do_option(self):
        self.set_speaking_queue()



class GiftingMenu2(NewMenu2):
    def __init__(self, gc_input, gd_input, name, menu_item_list):
        super().__init__(gc_input, gd_input, name, menu_item_list)
        self.y_spacing = 20
        self.max_length = 14
        gd_input.add_overlay("gifting_menu_overlay", Overlay2(gc_input, gd_input, "gifting_menu_overlay", 700, 200, Spritesheet("assets/menu_images/inventory_menu.png", 200, 400)))
        self.overlay = "gifting_menu_overlay"
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"

    def update_menu_items_list(self):
        self.menu_item_list = sorted(self.gc_input.inventory.current_items)
        # TODO: Add exit to menu

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render("     ITEMS     ", 1, (0, 0, 0))
        self.screen.blit(item, (self.x, self.y))

        menu_length_calc = 0
        if self.size >= self.max_length:
            menu_length_calc = self.max_length
        elif self.size < self.max_length:
            menu_length_calc = self.size

        for option in range(menu_length_calc):
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + self.y_spacing + (option * self.menu_spread)))

            spacing = 0
            if len(str(self.gd_input.item_list[self.menu_item_list[option]].quantity)) == 3:
                spacing = 110
            elif len(str(self.gd_input.item_list[self.menu_item_list[option]].quantity)) == 2:
                spacing = 120
            else:
                spacing = 130

            item = my_font.render("x" + str(self.gd_input.item_list[self.menu_item_list[option]].quantity), 1, (0, 0, 0))
            self.screen.blit(item, (self.x + spacing, self.y + self.y_spacing + (option * self.menu_spread)))
        self.display_cursor()

    def choose_option(self):
        self.gd_input.menu_list["yes_no_menu_2"].set_menu()

    def do_option(self):
        chosen_item = self.get_current_menu_item()
        self.exit_menu()
        self.gd_input.menu_list[self.gc_input.menu_manager.menu_stack[0]].give_item(chosen_item)

    def do_not_do_option(self):
        self.exit_menu()
        self.gd_input.menu_list[self.gc_input.menu_manager.menu_stack[0]].do_not_do_option()


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
        menu_length_calc = 0
        if self.size >= self.max_length:
            menu_length_calc = self.max_length
        elif self.size < self.max_length:
            menu_length_calc = self.size

        if self.cursor_at == 0 and self.size > 1:
            self.menu_item_list.insert(0, self.menu_item_list.pop(self.max_length - 1))

        elif self.size > 1:
            self.cursor_at -= 1

        else:
            pass

    def exit_menu(self):
        self.reset_cursor()
        self.gc_input.menu_manager.deactivate_menu(self.name)
        
        
class ShopKeeperInteractMenu2(NewMenu2):
    def __init__(self, gc_input, gd_input, name, menu_item_list):
        super().__init__(gc_input, gd_input, name, menu_item_list)
        self.talking_to = None
        self.menu_item_list.append("Exit")
        self.offset_y = 50
        self.offset_x = 150
        gd_input.add_overlay("shopkeeper_conversation_options_text_box", TextBox2(gc_input, gd_input, "shopkeeper_conversation_options_text_box", 250, 550, Spritesheet("assets/menu_images/text_box.png", 500, 150)))
        self.overlay = "shopkeeper_conversation_options_text_box"
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

    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))
        self.display_cursor()

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render(self.gd_input.character_list[self.talking_to].name + ":", 1, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.gd_input.overlay_list["text_box"].x + 150, self.gd_input.overlay_list["text_box"].y + 20))

        # Displays characters photo
        self.gc_input.screen.blit(self.gd_input.character_list[self.talking_to].face_image, (self.gd_input.overlay_list[self.overlay].x,  self.gd_input.overlay_list[self.overlay].y+2))


    def choose_option(self):
        self.do_option()

    def do_option(self):
        menu_selection = self.get_current_menu_item()

        if menu_selection == "Buy":
            self.gd_input.menu_list["buying_menu_2"].set_menu(self.talking_to)
            self.exit_menu()

        elif menu_selection == "Sell":
            self.gd_input.menu_list["inventory_select_menu"].set_menu()
            self.exit_menu()

        elif menu_selection == "Exit":
            self.gd_input.character_list[self.talking_to].set_state("idle")
            self.exit_menu()

    def process_item_selection(self, item):
        print("You sold 1 " + str(item))
        self.gc_input.inventory.unget_item(item, 1)
        self.gc_input.get_coins(self.gd_input.item_list[item].sell_price)
        
class BuyingMenu2(NewMenu2):
    def __init__(self, gc_input, gd_input, name, menu_item_list):
        super().__init__(gc_input, gd_input, name, menu_item_list)
        gd_input.add_overlay("buying_menu_overlay", Overlay2(gc_input, gd_input, "buying_menu_overlay", 700, 200, Spritesheet("assets/menu_images/inventory_menu.png", 200, 400)))
        self.overlay = "buying_menu_overlay"
        self.x = self.gd_input.overlay_list[self.overlay].x + self.offset_x
        self.y = self.gd_input.overlay_list[self.overlay].y + self.offset_y
        self.menu_type = "base"
        self.talking_to = None


    def display_menu(self):
        self.gd_input.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render("$    SHOP    $", 1, (0, 0, 0))
        self.screen.blit(item, (self.x, self.y))


        for option in range(self.size-1):
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(self.menu_item_list[option][0], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + 20 + (option * self.menu_spread)))

            item = my_font.render("$" + str(self.menu_item_list[option][1]), 1, (0, 0, 0))
            self.screen.blit(item, (self.x + 140 - (10 * len(str(self.menu_item_list[option][1]))), self.y +20 + (option * self.menu_spread)))

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render(self.menu_item_list[self.size-1][0], 1, (0, 0, 0))
        self.screen.blit(item, (self.x, self.y + 20 + ((self.size-1) * self.menu_spread)))

        self.display_cursor()

    def choose_option(self):
        self.do_option()

    def do_option(self):
        if self.try_buy_item():
            self.gd_input.character_list[self.talking_to].set_state("idle")
            self.talking_to = None
            self.exit_menu()
        else:
            pass

    def display_cursor(self):
        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render("-", 1, (0, 0, 0))
        self.screen.blit(item, (self.x - 15, (self.y + 2 + 20) + (self.cursor_at * self.menu_spread)))

    def try_buy_item(self):
        success = False
        menu_selection = self.gd_input.menu_list[self.name].get_current_menu_item()
        if menu_selection[0] == "Exit":
            self.gd_input.character_list[self.talking_to].set_state("idle")
            self.talking_to = None
            self.exit_menu()

        elif self.gc_input.your_coins >= menu_selection[1]:
            try_buy = self.gc_input.try_use_coins(menu_selection[1])
            if try_buy:
                self.gc_input.inventory.get_item(menu_selection[0], 1)
                self.gc_input.update_game_dialogue("You bought 1 " + menu_selection[0])
                print("You bought it!")
                success = True
            else:
                print("failed to buy the item")
                success = False
                self.gc_input.update_game_dialogue("You can't afford 1 " + menu_selection[0])
        else:
            print("you're poor")
            success = False
            self.gc_input.update_game_dialogue("You can't afford 1 " + menu_selection[0])
        return success

    def set_menu(self, person_talking_to):
        self.talking_to = person_talking_to
        self.update_menu_items_list()
        self.gc_input.set_keyboard_manager(InMenu.ID)
        self.gc_input.menu_manager.add_menu_to_stack(self.name)



    def update_menu_items_list(self):
        self.menu_item_list = (self.gd_input.character_list[self.talking_to].items_list).copy()
        self.menu_item_list.append(("Exit", "-"))
