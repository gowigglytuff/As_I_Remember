import pygame

from keyboards import InStartMenu, InYesNo, InInventory, InKeyInventory, InUse, InGame, InBuying


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


class ToDoList(Overlay):
    def __init__(self, GameController, GameData, name, x, y, image):
        super().__init__(GameController, GameData, name, x, y, image)
        self.to_dos = ["say hi to your mom", "kiss your cat", "eat a pear", "say hi to your mom", "kiss your cat", "eat a pear", "say hi to your mom", "kiss your cat", "eat a pear", "say hi to your mom", "kiss your cat", "eat a pear"]
        self.page = 1

    def display_overlay(self):
        self.screen.blit(self.image, (self.x, self.y))
        my_font = pygame.font.Font(self.GameController.font, 20)
        item = my_font.render("To Do List", 1, (0, 0, 0))
        self.GameController.screen.blit(item, (self.x + 45, self.y + 40))

        item_number = 0
        item_number = 1
        for item in self.to_dos:
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(str(item_number) + ". " + item, 1, (0, 0, 0))
            self.GameController.screen.blit(item, (self.x + 45, self.y + 50 + (20 * item_number)))
            item_number += 1


class ProfileCard(Overlay):
    def __init__(self, GameController, GameData, name, x, y, image):
        super().__init__(GameController, GameData, name, x, y, image)

    def display_overlay(self):
        self.screen.blit(self.image, (self.x, self.y))
        self.screen.blit(self.GameData.player["Player"].spritesheet.get_image(0, 0),( self.x +57, self.y +50))

        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render("Name: Jayden", 1, (0, 0, 0))
        self.GameController.screen.blit(item, (self.x +125, self.y + 40))

        item2 = my_font.render("Reputation: ", 1, (0, 0, 0))
        self.GameController.screen.blit(item2, (self.x + 125, self.y + 60))


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


class MenuManager(object):
    def __init__(self):
        self.character_interact_menu = False
        self.shopkeeper_interact_menu = False
        self.start_menu = False
        self.inventory_menu = False
        self.key_inventory_menu = False
        self.use_menu = False
        self.yes_no_menu = False
        self.buying_menu = False

    def activate_menu(self, menu_to_activate):
        if menu_to_activate == "character_interact_menu":
            self.character_interact_menu = True
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

    def deactivate_menu(self, menu_to_deactivate):
        if menu_to_deactivate == "character_interact_menu":
            self.character_interact_menu = False
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


class NewMenu(object):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay, associated_keyer_ID, offset_x=30, offset_y=20):
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
        self.associated_keyer_ID = associated_keyer_ID

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
        self.screen.blit(item, (self.x - 15, (self.y+2 + self.y_spacing) + (self.cursor_at * self.menu_spread)))

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
        self.GameController.set_keyboard_manager(self.associated_keyer_ID)
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
        pass

    def do_option(self):
        pass

class TalkingMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay, offset_x=150, offset_y = 50, associated_keyer_ID="ITKM_Keyer")
        self.talking_to = None
        self.menu_item_list.append("Exit")

    def set_talking_to(self, talking_to):
        self.talking_to = talking_to

    def unset_talking_to(self):
        self.talking_to = None

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))
        self.display_cursor()

        my_font = pygame.font.Font(self.GameController.font, 10)
        print(self.GameData.character_list[self.talking_to].name)
        item = my_font.render(self.GameData.character_list[self.talking_to].name + ":", 1, (0, 0, 0))
        self.GameController.screen.blit(item, (self.GameData.overlay_list["text_box"].x + 150, self.GameData.overlay_list["text_box"].y + 20))

        for option in range(self.size):
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))
        self.display_cursor()

class StartMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay, associated_keyer_ID="IRM_Keyer")
        self.menu_item_list.append("Exit")

    def do_option(self):
        menu_selection = self.get_current_menu_item()

        if menu_selection == "Bag":
            print("You looked in your bag!")
            self.GameData.menu_list["inventory_menu"].set_menu()


        elif menu_selection == "Key Items":
            print("You looked in your bag!")
            self.GameData.menu_list["key_inventory_menu"].set_menu()

        elif menu_selection == "Profile":
            self.GameController.add_current_overlay("ID_card")
            self.GameController.MenuManager.start_menu = False
            self.GameController.set_keyboard_manager("IPM_Keyer")
            self.GameData.menu_list["start_menu"].reset_cursor()

        elif menu_selection == "Chore List":
            self.GameController.add_current_overlay("To_do_list")
            self.GameController.MenuManager.start_menu = False
            self.GameController.set_keyboard_manager("ITDLM_Keyer")
            self.GameData.menu_list["start_menu"].reset_cursor()

        else:
            print("You exited the menu")
            self.GameController.set_keyboard_manager(InGame.ID)
            self.GameController.MenuManager.start_menu = False
            self.GameData.menu_list["start_menu"].reset_cursor()

    def choose_option(self):
        self.do_option()

class KeyInventoryMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay, associated_keyer_ID="IKM_Keyer")
        self.y_spacing = 20
        self.associated_manager = InKeyInventory.ID

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
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay, associated_keyer_ID="IIM_Keyer")
        self.y_spacing = 20
        self.associated_manager = InInventory.ID
        self.max_length = 14

    def update_menu_items_list(self):
        self.menu_item_list = sorted(self.GameController.inventory.current_items)

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

        if self.size > self.max_length and self.cursor_at == self.max_length -1:
            self.menu_item_list.append(self.menu_item_list.pop(0))

        elif self.cursor_at == menu_length_calc - 1:
            pass
        else:
            self.cursor_at += 1

    def cursor_up(self):
        menu_length_calc = 0
        if self.size >= self.max_length:
            menu_length_calc = self.max_length
        elif self.size < self.max_length:
            menu_length_calc = self.size

        if self.cursor_at == 0:
            self.menu_item_list.insert(0, self.menu_item_list.pop(self.max_length-1))

        else:
            self.cursor_at -= 1

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
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay, associated_keyer_ID="IU_Keyer")
        self.menu_item_list.append("Exit")

    def set_menu(self):
        self.update_menu_items_list()
        if self.GameController.current_menu is not None:
            self.set_origin(self.GameController.current_menu)
            menu_selection = self.GameData.menu_list[self.origin].get_current_menu_item()
            self.GameController.inventory.select_item(menu_selection)

        self.GameController.set_keyboard_manager(self.associated_keyer_ID)
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
            self.GameController.set_keyboard_manager(self.GameData.menu_list[self.origin].associated_manager)
            self.GameData.menu_list[self.origin].do_option(menu_selection)

        elif menu_selection == "Toss":
            self.reset_cursor()
            self.GameController.MenuManager.deactivate_menu(self.name)
            self.GameController.set_keyboard_manager(self.GameData.menu_list[self.origin].associated_manager)
            self.GameData.menu_list[self.origin].do_option(menu_selection)

    def do_not_do_option(self):
        self.GameData.menu_list[self.origin].do_not_do_option()
        self.exit_menus()


class YesNoMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay, associated_keyer_ID="YN_Keyer")

    def set_menu(self):
        self.update_menu_items_list()
        if self.GameController.current_menu is not None:
            self.set_origin(self.GameController.current_menu)
        self.GameController.set_keyboard_manager(self.associated_keyer_ID)
        self.GameController.MenuManager.activate_menu(self.name)
        self.GameController.set_current_menu(self.name)

    def choose_option(self):
        menu_selection = self.GameData.menu_list[self.name].get_current_menu_item()

        if menu_selection == "Yes":
            self.GameData.menu_list[self.origin].do_option()
            self.exit_menus()

        if menu_selection == "No":
            self.GameData.menu_list[self.origin].do_not_do_option()
            self.exit_menus()



class ShopKeeperInteractMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay, offset_x=150, offset_y = 50, associated_keyer_ID="ISKCO_Keyer")
        self.talking_to = None
        self.menu_item_list.append("Exit")

    def set_talking_to(self, talking_to):
        self.talking_to = talking_to

    def set_menu(self, talking_to):
        self.update_menu_items_list()
        print(self.GameController.current_menu)
        if self.GameController.current_menu is not None:
            print("hi")
            self.set_origin(self.GameController.current_menu)
            self.GameController.MenuManager.deactivate_menu(self.origin)
            self.GameData.menu_list[self.origin].reset_cursor()
        self.set_talking_to(talking_to)
        self.GameController.set_keyboard_manager(self.associated_keyer_ID)
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

    def choose_option(self):
        self.do_option()

    def do_option(self):
        menu_selection = self.get_current_menu_item()

        if menu_selection == "Buy":
            self.GameData.menu_list["buying_menu"].set_menu()
            self.GameController.MenuManager.deactivate_menu("shopkeeper_interact_menu")

        elif menu_selection == "Sell":
            print("You sold an item")
            self.GameController.set_keyboard_manager(InGame.ID)
            self.GameController.MenuManager.shopkeeper_interact_menu = False
            self.GameData.character_list[self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].direction).object_filling].set_state("idle")

        elif menu_selection == "Exit":
            print("Please come again!")
            self.GameController.set_keyboard_manager(InGame.ID)
            self.GameController.MenuManager.shopkeeper_interact_menu = False
            self.GameData.character_list[self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].direction).object_filling].set_state("idle")



class BuyingMenu(NewMenu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay, associated_keyer_ID="IB_Keyer")

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
            self.screen.blit(item, (self.x + 120, self.y +20 + (option * self.menu_spread)))
        self.display_cursor()

    def choose_option(self):
        self.do_option()

    def do_option(self):
        menu_selection = self.GameData.menu_list[self.name].get_current_menu_item()
        print(menu_selection)

    def display_cursor(self):
        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render("-", 1, (0, 0, 0))
        self.screen.blit(item, (self.x - 15, (self.y + 2 + 20) + (self.cursor_at * self.menu_spread)))


