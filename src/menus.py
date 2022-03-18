import textwrap

import pygame

from keyboards import InGame
from spritesheet import Spritesheet


class MenuManager(object):
    def __init__(self):
        self.conversation_options_menu = False
        self.shopkeeper_interact_menu = False
        self.start_menu = False
        self.inventory_menu = False
        self.key_inventory_menu = False
        self.use_menu = False
        self.yes_no_menu = False
        self.buying_menu = False
        self.to_do_list_menu = False
        self.in_conversation_menu = False
        self.static_menus = ["stats_menu", "game_action_dialogue_menu"]
        self.active = []
        self.menu_stack = []
        self.visable_menus = []

    def add_menu_to_stack(self, menu_to_add):
        self.menu_stack.insert(0, menu_to_add)



    def activate_menu(self, menu_to_activate):
        self.active.append(menu_to_activate)

    def deactivate_menu(self, menu_to_deactivate):
        self.active.remove(menu_to_deactivate)

    def activate_menu2(self, menu_to_activate):
        if menu_to_activate == "conversation_options_menu":
            self.conversation_options_menu = True
        if menu_to_activate == "shopkeeper_interact_menu":
            self.shopkeeper_interact_menu = True
        if menu_to_activate == "start_menu":
            self.start_menu = True
        if menu_to_activate == "inventory_menu":
            self.inventory_menu = True
        if menu_to_activate == "key_inventory_menu":
            self.key_inventory_menu = True
        if menu_to_activate == "use_menu":
            self.use_menu = True
        if menu_to_activate == "yes_no_menu":
            self.yes_no_menu = True
        if menu_to_activate == "buying_menu":
            self.buying_menu = True
        if menu_to_activate == "to_do_list_menu":
            self.to_do_list_menu = True
        if menu_to_activate == "in_conversation_menu":
            self.in_conversation_menu = True

    def deactivate_menu2(self, menu_to_deactivate):
        if menu_to_deactivate == "conversation_options_menu":
            self.conversation_options_menu = False
        if menu_to_deactivate == "shopkeeper_interact_menu":
            self.shopkeeper_interact_menu = False
        if menu_to_deactivate == "start_menu":
            self.start_menu = False
        if menu_to_deactivate == "inventory_menu":
            self.inventory_menu = False
        if menu_to_deactivate == "key_inventory_menu":
            self.key_inventory_menu = False
        if menu_to_deactivate == "use_menu":
            self.use_menu = False
        if menu_to_deactivate == "yes_no_menu":
            self.yes_no_menu = False
        if menu_to_deactivate == "buying_menu":
            self.buying_menu = False
        if menu_to_deactivate == "to_do_list_menu":
            self.to_do_list_menu = False
        if menu_to_deactivate == "in_conversation_menu":
            self.in_conversation_menu = False


class Overlay(object):
    def __init__(self, GameController, GameData, name, x, y, image):
        self.GameController = GameController
        self.GameData = GameData
        self.screen = self.GameController.screen
        self.x = x
        self.y = y
        self.name = name
        self.image = image.get_image(0, 0)

    def display_overlay(self):
        self.screen.blit(self.image, (self.x, self.y))


class TextBox(Overlay):
    def __init__(self, GameController, GameData, name, x, y, image):
        super().__init__(GameController, GameData, name, x, y, image)

    def display_phrase(self, character):
    # prints the speakers name
        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render(self.GameData.character_list[character].name + ":", 1, (0, 0, 0))
        self.GameController.screen.blit(item, (
        self.GameData.overlay_list["text_box"].x + 150, self.GameData.overlay_list["text_box"].y + 20))

        # prints phrases to be spoke
        text_line = 0
        for line in self.GameData.character_list[character].speaking_queue:
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(line, 1, (0, 0, 0))
            self.GameController.screen.blit(item, (self.GameData.overlay_list["text_box"].x + 150,
                                                   self.GameData.overlay_list["text_box"].y + 50 + 25 * text_line))
            text_line += 1


class StaticMenu(object):
    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData
        self.screen = self.GameController.screen
        GameData.add_overlay("stats_overlay", Overlay(GameController, GameData, "stats_overlay", 800, 50, Spritesheet("assets/menu_images/use_menu.png", 100, 100)))
        self.overlay = "stats_overlay"
        self.offset_x = 10
        self.offset_y = 20
        self.x = self.GameData.overlay_list[self.overlay].x + self.offset_x
        self.y = self.GameData.overlay_list[self.overlay].y + self.offset_y
        self.name = "stats_menu"
        self.menu_item_list = [("Coins: ", str(GameController.your_coins)), ("Seeds:", str(GameController.your_seeds)), ("Love: ", "100")]
        self.menu_spread = 25
        self.menu_go = True
        self.cursor_at = 0
        self.y_spacing = 0


        self.origin = None


    def update_menu_items_list(self):
        self.menu_item_list = [("Coins: ", str(self.GameController.your_coins)), ("Seeds:", str(self.GameController.your_seeds)), ("Love: ", "100")]

    @property
    def size(self):
        return len(self.menu_item_list)

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(self.menu_item_list[option][0], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))

        for quantitity in range(self.size):
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(self.menu_item_list[quantitity][1], 1, (0, 0, 0))
            self.screen.blit(item, (self.x + 80 - (10 * len(self.menu_item_list[quantitity][1])), self.y + (quantitity * self.menu_spread)))


class GameActionDialogue(object):
    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData
        self.screen = self.GameController.screen
        GameData.add_overlay("game_dialogue_box", Overlay(GameController, GameData, "game_dialogue_box", 780, 680, Spritesheet("assets/menu_images/testing_menu.png", 200, 100)))
        self.overlay = "game_dialogue_box"
        self.offset_x = 10
        self.offset_y = 20
        self.x = self.GameData.overlay_list[self.overlay].x + self.offset_x
        self.y = self.GameData.overlay_list[self.overlay].y + self.offset_y
        self.name = "game_action_dialogue_menu"
        self.menu_item_list = ["This is the game dialouge box!"]
        self.menu_spread = 15
        self.menu_go = True
        self.cursor_at = 0
        self.y_spacing = 0


        self.origin = None


    def update_menu_items_list(self):
        self.menu_item_list = [("Coins: ", str(self.GameController.your_coins)), ("Seeds:", str(self.GameController.your_seeds)), ("Love: ", "100")]

    @property
    def size(self):
        return len(self.menu_item_list)

    def show_dialogue(self, phrase):
        if len(self.menu_item_list) >= 4:
            del self.menu_item_list[0]
        self.menu_item_list.append(phrase)
        # self.display_menu()

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.GameController.font, 6)
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))


class CharacterDialogue(object):
    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData
        self.screen = self.GameController.screen
        GameData.add_overlay("dialogue_text_box", TextBox(GameController, GameData, "text_box", 250, 550, Spritesheet("assets/menu_images/text_box.png", 500, 150)))
        self.overlay = "dialogue_text_box"
        self.offset_x = 150
        self.offset_y = 25
        self.x = self.GameData.overlay_list[self.overlay].x + self.offset_x
        self.y = self.GameData.overlay_list[self.overlay].y + self.offset_y
        self.name = "character_dialogue_menu"
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
            self.exit_menus()

    @property
    def size(self):
        return len(self.menu_item_list)

    def display_menu(self):
        # prints the dialgue text box
        self.GameData.overlay_list[self.overlay].display_overlay()

        # Display characters name
        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render(self.GameData.character_list[self.talking_to].name + ":", 1, (0, 0, 0))
        self.GameController.screen.blit(item, (self.x,  self.y))

        # Displays characters dialogue
        text_line = 1
        for line in self.speaking_queue:
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(line, 1, (0, 0, 0))
            self.GameController.screen.blit(item, (self.x,  self.y + self.y_spacing * text_line))
            text_line += 1

        # Displays characters photo
        self.GameController.screen.blit(self.GameData.character_list[self.talking_to].face_image, (self.GameData.overlay_list[self.overlay].x,  self.GameData.overlay_list[self.overlay].y+2))

    def set_origin(self, menu_name):
        self.origin = menu_name

    def exit_menus(self):
        self.GameController.current_menu = None

        self.GameData.character_list[self.talking_to].set_state("idle")
        self.GameController.set_speaker(None)

        if self.origin is not None:
            self.GameData.menu_list[self.origin].reset_cursor()
            self.origin = None
        self.GameController.MenuManager.deactivate_menu(self.name)
        self.GameController.set_keyboard_manager(InGame.ID)

    def set_menu(self, talking_to, phrase):
        self.talking_to = talking_to
        # self.update_menu_items_list()
        self.update_menu_items_list(phrase)
        self.set_current_phrase()
        self.set_speaking_queue()

        if self.GameController.current_menu is not None:
            self.set_origin(self.GameController.current_menu)
            self.GameController.MenuManager.deactivate_menu(self.origin)
            self.GameData.menu_list[self.origin].reset_cursor()
        self.GameController.set_keyboard_manager("IRM_Keyer")
        self.GameController.MenuManager.activate_menu(self.name)
        self.GameController.set_current_menu(self.name)


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


class NewMenu(object):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay, offset_x=30, offset_y=20):
        self.GameController = GameController
        self.GameData = GameData
        self.screen = self.GameController.screen
        self.overlay = overlay
        self.x = self.GameData.overlay_list[self.overlay].x + offset_x
        self.y = self.GameData.overlay_list[self.overlay].y + offset_y
        self.name = name
        self.menu_item_list = menu_item_list
        self.menu_spread = 25
        self.menu_go = menu_go
        self.cursor_at = 0
        self.y_spacing = 0

        self.origin = None


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

    def set_origin(self, menu_name):
        self.origin = menu_name

    def reset_origin(self):
        self.origin = None

    def reset_cursor(self):
        self.cursor_at = 0

    def display_cursor(self):
        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render("-", 1, (0, 0, 0))
        self.screen.blit(item, (self.x - 12, (self.y+2 + self.y_spacing) + (self.cursor_at * self.menu_spread)))

    def get_current_menu_item(self):
        menu_selection = self.menu_item_list[self.cursor_at]
        return menu_selection

    # each menu needs its own

    def set_menu(self):
        self.update_menu_items_list()
        if self.GameController.current_menu is not None:
            self.set_origin(self.GameController.current_menu)
            self.GameController.MenuManager.deactivate_menu(self.origin)
            self.GameData.menu_list[self.origin].reset_cursor()
        self.GameController.set_keyboard_manager("IRM_Keyer")
        self.GameController.MenuManager.activate_menu(self.name)
        self.GameController.set_current_menu(self.name)

    def unset_menu(self):
        pass

    def exit_menus(self):
        self.reset_cursor()
        self.GameController.current_menu = None
        if self.origin is not None:
            self.GameData.menu_list[self.origin].reset_cursor()
            self.origin = None
        self.GameController.MenuManager.deactivate_menu(self.name)
        self.GameController.set_keyboard_manager(InGame.ID)

    def exit_this_menu(self):
        self.reset_cursor()
        self.GameController.current_menu = None
        self.GameController.MenuManager.deactivate_menu(self.name)

    @property
    def size(self):
        return len(self.menu_item_list)

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))
        self.display_cursor()

    def choose_option(self):
        self.do_option()

    def do_option(self):
        pass

    def try_to_exit(self):
        pass


class ToDoListMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay)

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))
        self.display_cursor()

    def do_option(self):
        self.exit_menus()

    def choose_option(self):
        self.do_option()


class ConversationOptionsMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay, offset_x=150, offset_y = 30)
        self.talking_to = None
        self.menu_item_list.append("Exit")
        self.offset_x = 150
        self.offset_y = 25
        self.x = self.GameData.overlay_list[self.overlay].x + self.offset_x
        self.y = self.GameData.overlay_list[self.overlay].y + self.offset_y
        self.y_spacing = 25
        self.menu_photo = Spritesheet("assets/NPC_sprites/faces/DonnaFace.png", 150, 150).get_image(0, 0)

    def set_talking_to(self, talking_to):
        self.talking_to = talking_to

    def unset_talking_to(self):
        self.talking_to = None

    def display_menu(self):
        # Display Overlay
        self.GameData.overlay_list[self.overlay].display_overlay()

        # Display speakers name
        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render(self.GameData.character_list[self.talking_to].name + ":", 1, (0, 0, 0))
        self.GameController.screen.blit(item, (self.x, self.y))

        # Display Dialogue Options
        text_line = 1
        for option in range(self.size):
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + self.y_spacing * text_line))
            text_line += 1
        self.display_cursor()
        text_line = 1

        # Displays characters photo
        self.GameController.screen.blit(self.GameData.character_list[self.talking_to].face_image, (self.GameData.overlay_list[self.overlay].x,  self.GameData.overlay_list[self.overlay].y+2))

    def do_option(self):
        menu_selection = self.GameData.menu_list["conversation_options_menu"].get_current_menu_item()
        if menu_selection == "Talk":
            self.GameData.menu_list["character_dialogue_menu"].set_menu(self.talking_to, self.GameData.character_list[self.talking_to].phrase)
            self.GameData.menu_list["conversation_options_menu"].set_talking_to(None)

        elif menu_selection == "Give Gift":
            self.GameData.menu_list["gift_menu"].set_menu()

        elif menu_selection == "Exit":
            self.GameData.menu_list["conversation_options_menu"].set_talking_to(None)
            self.GameData.character_list[self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].get_direct(self.GameData.player["Player"].facing)).object_filling].set_state("idle")
            self.exit_menus()

    def do_not_do_option(self):
        self.GameData.menu_list["conversation_options_menu"].set_talking_to(None)
        self.GameData.character_list[self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].get_direct(self.GameData.player["Player"].facing)).object_filling].set_state("idle")
        self.exit_menus()

    def set_menu(self, person_talking_to):
        self.update_menu_items_list()
        if self.GameController.current_menu is not None:
            self.set_origin(self.GameController.current_menu)
            self.GameController.MenuManager.deactivate_menu(self.origin)
            self.GameData.menu_list[self.origin].reset_cursor()
        self.GameController.set_keyboard_manager("IRM_Keyer")
        self.GameController.MenuManager.activate_menu(self.name)
        self.GameController.set_current_menu(self.name)
        self.set_talking_to(person_talking_to)

    def give_item(self, item):

        self.GameController.inventory.unget_item(item, 1)
        self.GameController.update_game_dialogue("You gave " + self.talking_to + " 1 " + item)
        self.GameData.menu_list["character_dialogue_menu"].set_menu(self.talking_to, self.GameData.character_list[self.talking_to].phrase_thanks)
        self.set_talking_to(None)


class StartMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay)
        self.menu_item_list.append("Exit")

    def do_option(self):
        menu_selection = self.get_current_menu_item()

        if menu_selection == "Bag":
            self.GameData.menu_list["inventory_menu"].set_menu()

        elif menu_selection == "Key Items":
            self.GameData.menu_list["key_inventory_menu"].set_menu()

        elif menu_selection == "Chore List":
            self.GameData.menu_list["to_do_list_menu"].set_menu()

        elif menu_selection == "Profile":
            self.GameData.menu_list["profile_menu"].set_menu()

        elif menu_selection == "Exit":
            self.exit_menus()

        elif menu_selection == "Outfits":
            # TODO: Add outfit selection
            self.GameController.update_game_dialogue("You have no other outfits")
            self.exit_menus()

        elif menu_selection == "Save":
            self.GameController.update_game_dialogue("You saved the game!")
            self.exit_menus()

        # elif menu_selection == "Chore List":
        #     self.GameController.add_current_overlay("To_do_list")
        #     self.GameController.MenuManager.start_menu = False
        #     self.GameController.set_keyboard_manager("ITDLM_Keyer")
        #     self.GameData.menu_list["start_menu"].reset_cursor()

        else:
            self.exit_menus()

    def choose_option(self):
        self.do_option()

    def try_to_exit(self):
        self.exit_menus()


class KeyInventoryMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay)
        self.y_spacing = 20

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render("<  KEY ITEMS  >", 1, (0, 0, 0))
        self.screen.blit(item, (self.x, self.y))

        for option in range(self.size):
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + self.y_spacing + (option * self.menu_spread)))

        self.display_cursor()

    def choose_option(self):
        self.GameData.menu_list["use_menu"].set_menu()

    def do_option(self, choice=None):
        menu_selection = choice

        if menu_selection == "Use":
            self.GameData.key_item_list[self.get_current_menu_item()].use_key_item()
            self.GameController.inventory.select_item(None)
            self.GameController.inventory.reset_bag_slot()
            self.exit_menus()


        elif menu_selection == "Toss":
            print("You tossed put the item")
            self.GameController.inventory.reset_bag_slot()
            self.exit_menus()

        elif menu_selection == "Exit":
            self.GameController.inventory.reset_bag_slot()
            self.exit_menus()

    def do_not_do_option(self):
        self.GameController.inventory.reset_bag_slot()
        self.exit_menus()

    def cursor_left(self):
        self.reset_cursor()
        self.update_menu_items_list()
        self.GameController.inventory.bag_slot_left()

    def cursor_right(self):
        self.reset_cursor()
        self.update_menu_items_list()
        self.GameController.inventory.bag_slot_right()


class InventoryMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay)
        self.y_spacing = 20
        self.max_length = 14

    def update_menu_items_list(self):
        self.menu_item_list = sorted(self.GameController.inventory.current_items)
        # TODO: Add exit to menu

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.GameController.font, 10)
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
            if len(str(self.GameData.item_list[self.menu_item_list[option]].quantity)) == 3:
                spacing = 110
            elif len(str(self.GameData.item_list[self.menu_item_list[option]].quantity)) == 2:
                spacing = 120
            else:
                spacing = 130

            item = my_font.render("x" + str(self.GameData.item_list[self.menu_item_list[option]].quantity), 1, (0, 0, 0))
            self.screen.blit(item, (self.x + spacing, self.y + self.y_spacing + (option * self.menu_spread)))
        self.display_cursor()

    def choose_option(self):
        self.GameData.menu_list["use_menu"].set_menu()

    def do_option(self, choice=None):
        menu_selection = choice

        if menu_selection == "Use":
            self.GameData.item_list[self.get_current_menu_item()].use_item()
            self.GameController.inventory.select_item(None)
            self.GameController.inventory.reset_bag_slot()
            self.exit_menus()

        elif menu_selection == "Toss":
            print("You tossed out the " + str(self.get_current_menu_item()) + "!")
            self.GameController.inventory.reset_bag_slot()
            self.exit_menus()

        elif menu_selection == "Exit":
            self.GameController.inventory.reset_bag_slot()
            self.exit_menus()

    def do_not_do_option(self):
        self.GameController.inventory.reset_bag_slot()
        self.exit_menus()

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
        self.GameController.inventory.bag_slot_left()

    def cursor_right(self):
        self.reset_cursor()
        self.update_menu_items_list()
        self.GameController.inventory.bag_slot_right()


class UseMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay)
        self.menu_item_list.append("Exit")

    def set_menu(self):
        self.update_menu_items_list()
        if self.GameController.current_menu is not None:
            self.set_origin(self.GameController.current_menu)
            menu_selection = self.GameData.menu_list[self.origin].get_current_menu_item()
            self.GameController.inventory.select_item(menu_selection)

        self.GameController.set_keyboard_manager("IRM_Keyer")
        self.GameController.MenuManager.activate_menu(self.name)
        self.GameController.set_current_menu(self.name)


    def choose_option(self):
        menu_selection = self.GameData.menu_list["use_menu"].get_current_menu_item()

        if menu_selection == "Use":
            self.GameData.menu_list["yes_no_menu"].set_menu()

        elif menu_selection == "Toss":
            self.GameData.menu_list["yes_no_menu"].set_menu()


        elif menu_selection == "Exit":
            self.GameData.menu_list[self.origin].do_not_do_option()
            self.GameController.MenuManager.deactivate_menu(self.name)
            self.GameController.MenuManager.deactivate_menu(self.origin)
            self.exit_menus()


    def do_option(self):
        menu_selection = self.GameData.menu_list["use_menu"].get_current_menu_item()

        if menu_selection == "Use":
            self.reset_cursor()
            self.GameController.MenuManager.deactivate_menu(self.name)
            self.GameData.menu_list[self.origin].do_option(menu_selection)

        elif menu_selection == "Toss":
            self.reset_cursor()
            self.GameController.MenuManager.deactivate_menu(self.name)
            self.GameData.menu_list[self.origin].do_option(menu_selection)

    def do_not_do_option(self):
        self.GameData.menu_list[self.origin].do_not_do_option()
        self.exit_menus()


class YesNoMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay)

    def set_menu(self):
        self.update_menu_items_list()
        if self.GameController.current_menu is not None:
            self.set_origin(self.GameController.current_menu)
        self.GameController.set_keyboard_manager("IRM_Keyer")
        self.GameController.MenuManager.activate_menu(self.name)
        self.GameController.set_current_menu(self.name)

    def choose_option(self):
        menu_selection = self.GameData.menu_list[self.name].get_current_menu_item()

        if menu_selection == "Yes":
            self.exit_this_menu()
            self.GameData.menu_list[self.origin].do_option()
            self.origin = None


        if menu_selection == "No":
            print(self.GameController.MenuManager.active)
            self.GameData.menu_list[self.origin].do_not_do_option()
            self.exit_menus()

    def exit_this_menu(self):
        self.reset_cursor()
        self.GameController.current_menu = None
        self.GameController.MenuManager.deactivate_menu(self.name)


class ShopKeeperInteractMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay, offset_x=150, offset_y = 50)
        self.talking_to = None
        self.menu_item_list.append("Exit")

    def set_talking_to(self, talking_to):
        self.talking_to = talking_to

    def set_menu(self, talking_to):
        self.update_menu_items_list()
        if self.GameController.current_menu is not None:
            self.set_origin(self.GameController.current_menu)
            self.GameController.MenuManager.deactivate_menu(self.origin)
            self.GameData.menu_list[self.origin].reset_cursor()
        self.set_talking_to(talking_to)
        self.GameController.set_keyboard_manager("IRM_Keyer")
        self.GameController.MenuManager.activate_menu(self.name)
        self.GameController.set_current_menu(self.name)

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))
        self.display_cursor()

        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render(self.GameData.character_list[self.talking_to].name + ":", 1, (0, 0, 0))
        self.GameController.screen.blit(item, (self.GameData.overlay_list["text_box"].x + 150, self.GameData.overlay_list["text_box"].y + 20))

        # Displays characters photo
        self.GameController.screen.blit(self.GameData.character_list[self.talking_to].face_image, (self.GameData.overlay_list[self.overlay].x,  self.GameData.overlay_list[self.overlay].y+2))


    def choose_option(self):
        self.do_option()

    def do_option(self):
        menu_selection = self.get_current_menu_item()

        if menu_selection == "Buy":
            self.GameData.menu_list["buying_menu"].set_menu()

        elif menu_selection == "Sell":
            # print("You sold an item")
            # self.GameData.character_list[self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].direction).object_filling].set_state("idle")
            # self.exit_menus()
            self.GameData.menu_list["inventory_select_menu"].set_menu()

        elif menu_selection == "Exit":
            self.GameData.character_list[self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].direction).object_filling].set_state("idle")
            self.exit_menus()

    def process_item_selection(self, item):
        print("You sold 1 " + str(item))
        self.GameController.inventory.unget_item(item, 1)
        self.GameController.get_coins(self.GameData.item_list[item].sell_price)


class BuyingMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay)

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render("$    SHOP    $", 1, (0, 0, 0))
        self.screen.blit(item, (self.x, self.y))


        for option in range(self.size):
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(self.menu_item_list[option][0], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + 20 + (option * self.menu_spread)))

            item = my_font.render("$" + str(self.menu_item_list[option][1]), 1, (0, 0, 0))
            self.screen.blit(item, (self.x + 140 - (10 * len(str(self.menu_item_list[option][1]))), self.y +20 + (option * self.menu_spread)))
        self.display_cursor()

    def choose_option(self):
        self.do_option()

    def do_option(self):
        if self.try_buy_item():
            self.GameData.character_list[self.GameData.menu_list[self.origin].talking_to].set_state("idle")
            self.exit_menus()
        else:
            pass

    def display_cursor(self):
        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render("-", 1, (0, 0, 0))
        self.screen.blit(item, (self.x - 15, (self.y + 2 + 20) + (self.cursor_at * self.menu_spread)))

    def try_buy_item(self):
        success = False
        menu_selection = self.GameData.menu_list[self.name].get_current_menu_item()
        if self.GameController.your_coins >= menu_selection[1]:
            try_buy = self.GameController.try_use_coins(menu_selection[1])
            if try_buy:
                self.GameController.inventory.get_item(menu_selection[0], 1)
                self.GameController.update_game_dialogue("You bought 1 " + menu_selection[0])
                print("You bought it!")
                success = True
            else:
                print("failed to buy the item")
                success = False
                self.GameController.update_game_dialogue("You can't afford 1 " + menu_selection[0])
        else:
            print("you're poor")
            success = False
            self.GameController.update_game_dialogue("You can't afford 1 " + menu_selection[0])
        return success

    def set_menu(self):

        if self.GameController.current_menu is not None:
            self.set_origin(self.GameController.current_menu)
            self.GameController.MenuManager.deactivate_menu(self.origin)
            self.GameData.menu_list[self.origin].reset_cursor()
        self.update_menu_items_list()
        self.GameController.set_keyboard_manager("IRM_Keyer")
        self.GameController.MenuManager.activate_menu(self.name)
        self.GameController.set_current_menu(self.name)

    def update_menu_items_list(self):
        self.menu_item_list = self.GameData.character_list[self.GameData.menu_list[self.origin].talking_to].items_list


class ProfileMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay)

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()
        self.screen.blit(self.GameData.player["Player"].spritesheet.get_image(0, 0),( self.x + 27, self.y + 30))

        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render("Name: Shuma", 1, (0, 0, 0))
        self.GameController.screen.blit(item, (self.x +125, self.y + 40))

        item2 = my_font.render("Reputation: ", 1, (0, 0, 0))
        self.GameController.screen.blit(item2, (self.x + 125, self.y + 60))

    def do_option(self):
        self.exit_menus()

    def choose_option(self):
        self.do_option()


class GiftingMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay)
        self.y_spacing = 20
        self.max_length = 14

    def update_menu_items_list(self):
        self.menu_item_list = sorted(self.GameController.inventory.current_items)
        # TODO: Add exit to menu

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.GameController.font, 10)
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
            if len(str(self.GameData.item_list[self.menu_item_list[option]].quantity)) == 3:
                spacing = 110
            elif len(str(self.GameData.item_list[self.menu_item_list[option]].quantity)) == 2:
                spacing = 120
            else:
                spacing = 130

            item = my_font.render("x" + str(self.GameData.item_list[self.menu_item_list[option]].quantity), 1, (0, 0, 0))
            self.screen.blit(item, (self.x + spacing, self.y + self.y_spacing + (option * self.menu_spread)))
        self.display_cursor()

    def choose_option(self):
        self.GameData.menu_list["yes_no_menu"].set_menu()

    def do_option(self):

        chosen_item = None
        # self.GameController.inventory.select_item(None)
        chosen_item = self.get_current_menu_item()
        self.exit_this_menu()
        self.GameData.menu_list[self.origin].give_item(chosen_item)
        print(self.GameController.current_menu)



    def do_not_do_option(self):
        self.GameData.menu_list[self.origin].do_not_do_option()
        self.exit_menus()

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
        self.GameController.current_menu = None
        if self.origin is not None:
            self.GameData.menu_list[self.origin].reset_cursor()
            self.origin = None
        self.GameController.MenuManager.deactivate_menu(self.name)
        self.GameController.set_keyboard_manager(InGame.ID)


class SellingMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay)
        self.y_spacing = 20
        self.max_length = 14

    def update_menu_items_list(self):
        self.menu_item_list = sorted(self.GameController.inventory.current_items)
        # TODO: Add exit to menu

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.GameController.font, 10)
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
            if len(str(self.GameData.item_list[self.menu_item_list[option]].sell_price)) == 3:
                spacing = 110
            elif len(str(self.GameData.item_list[self.menu_item_list[option]].sell_price)) == 2:
                spacing = 120
            else:
                spacing = 130

            cost = my_font.render("$" + str(self.GameData.item_list[self.menu_item_list[option]].sell_price), 1, (0, 0, 0))
            self.screen.blit(cost, (self.x + spacing, self.y + self.y_spacing + (option * self.menu_spread)))
        self.display_cursor()

    def choose_option(self):
        self.GameData.menu_list["yes_no_menu"].set_menu()

    def do_option(self):
        chosen_item = None
        self.GameController.inventory.select_item(None)
        chosen_item = self.get_current_menu_item()
        self.GameData.menu_list[self.origin].process_item_selection(chosen_item)
        self.GameData.character_list[self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].facing).object_filling].set_state("idle")
        self.exit_menus()


    def do_not_do_option(self):
        self.exit_menus()

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
        self.GameController.current_menu = None
        if self.origin is not None:
            self.GameData.menu_list[self.origin].reset_cursor()
            self.origin = None
        self.GameController.MenuManager.deactivate_menu(self.name)
        self.GameController.set_keyboard_manager(InGame.ID)