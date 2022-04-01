import pygame
from data import GameData, GameController



class Inventory(object):
    def __init__(self, GameController: GameController, GameData: GameData):
        self.GameController = GameController
        self.GameData = GameData

        self.current_items = []
        self.current_key_items = []
        self.bag_slots = ["inventory_menu_2", "key_inventory_menu_2"]
        self.current_bag_slot = 0
        self.selected_item = None

    # TODO: Remove this
    def select_item(self, selected_item):
        self.selected_item = selected_item

    def bag_left(self):
        self.bag_slots.append(self.bag_slots.pop(self.bag_slots.index(self.bag_slots[0])))

    def change_bag_slot(self):
        self.GameController.menu_manager.self.bag_slots[0] = True

    def bag_slot_right(self):
        self.GameData.menu_list[self.bag_slots[self.current_bag_slot]].exit_menu()
        if self.current_bag_slot < (len(self.bag_slots)-1):
            self.current_bag_slot +=1
        elif self.current_bag_slot == (len(self.bag_slots)-1):
            self.current_bag_slot = 0
        # TODO: Fix this up
        self.GameData.menu_list[self.bag_slots[self.current_bag_slot]].set_menu()


    def bag_slot_left(self):
        print(self.GameData.menu_list[self.bag_slots[self.current_bag_slot]])
        print(self.current_bag_slot)

        self.GameData.menu_list[self.bag_slots[self.current_bag_slot]].exit_menu()
        # if self.current_bag_slot > 0:
        #     self.current_bag_slot -=1
        # else:
        #     self.current_bag_slot = (len(self.bag_slots)-1)

        if self.current_bag_slot == 0:
            self.current_bag_slot = 1
            print("moving 1")
        elif self.current_bag_slot == 1:
            self.current_bag_slot = 0
            print("moving 2")

        print(self.GameData.menu_list[self.bag_slots[self.current_bag_slot]])
        print(self.current_bag_slot)
        self.GameData.menu_list[self.bag_slots[self.current_bag_slot]].set_menu()

    def reset_bag_slot(self):
        self.current_bag_slot = 0

    def get_item(self, item_name: str, quantity_acquired: int):
        if item_name in self.current_items:
            self.GameData.item_list[item_name].quantity += quantity_acquired
        else:
            self.current_items.append(self.GameData.item_list[item_name].name)
            self.GameData.item_list[item_name].quantity += quantity_acquired

    def unget_item(self, item_name: str, quantity_used: int):
        if item_name in self.current_items:
            self.GameData.item_list[item_name].quantity -= quantity_used
        else:
            print("there was nothing to remove??")
        if self.GameData.item_list[item_name].quantity == 0:
            self.current_items.remove(self.GameData.item_list[item_name].name)

    def use_up_item(self, item_name: str, quantity_used: int):
        #TODO: Make sure this can't go below 0
        if self.GameData.item_list[item_name].quantity > quantity_used:
            self.GameData.item_list[item_name].quantity -= quantity_used
            print(self.GameData.item_list[item_name].quantity)
        elif self.GameData.item_list[item_name].quantity == quantity_used:
            self.current_items.remove(self.GameData.item_list[item_name].name)
            self.GameData.item_list[item_name].quantity -= quantity_used
            print(str(self.GameData.item_list[item_name].quantity) + " part2")
        else:
            print("you cannot use that now")

    def get_key_item(self, key_item_name: str):
        self.current_key_items.append(self.GameData.key_item_list[key_item_name].name)
        self.GameData.key_item_list[key_item_name].quantity = 1

    def use_up_key_item(self, key_item_name: str):
        self.GameData.key_item_list[key_item_name].quantity = 0
        self.current_key_items.pop(self.GameData.key_item_list[key_item_name].name)

    def sort_current_items(self):
        self.GameController.inventory.current_items = sorted(self.GameController.inventory.current_items)


class KeyItem(object):
    def __init__(self, name, GameData, GameController):
        self.GameController = GameController
        self.GameData = GameData
        self.name = name
        self.quantity = 0
        pass

    def use_key_item(self):
        print("You used the " + self.name)


class Item(object):
    '''
    :type gc_input: GameController
    :type gd_input: GameData
    :return: None
    '''
    NAME = None
    def __init__(self, gd_input, gc_input):
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.name = self.NAME
        self.quantity = 0
        self.sell_price = 0
        pass

    def use_item(self):
        if self.check_if_can_use_item():
            print("You used the " + self.name)
            self.gc_input.inventory.use_up_item(self.name, 1)
            self.gc_input.update_game_dialogue("You used 1 " + str(self.name))
            self.item_use()
        else:
            self.fail_to_use_item()

    def item_use(self):
        pass

    def check_if_can_use_item(self):
        result = True
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("You can't use that now")


class Cheese(Item):
    NAME = "Cheese"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)
        self.sell_price = 5

    def item_use(self):
        self.gc_input.get_coins(10)

    def check_if_can_use_item(self):
        result = True
        if self.gd_input.player[Player.NAME].x % 2 == 0:
            result = False

        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("You can't use it on odd tiles")

class Bread(Item):
    NAME = "Bread"
    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)
        self.sell_price = 5

    def item_use(self):
        self.gc_input.update_game_dialogue("Your hunger went away!")

class TimeSeed(Item):
    NAME = "Time Seed"
    USETYPE = "Single"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)
        self.sell_price = 100

    def item_use(self):
        self.gc_input.update_game_dialogue("The wind hummed joyously!")


class Book1(Item):
    NAME = "Book 1"
    USETYPE = "Reusable"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)
        self.sell_price = 10

    def item_use(self):
        self.gc_input.update_game_dialogue("You read " + self.NAME)

class Book2(Item):
    NAME = "Book 2"
    USETYPE = "Reusable"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)
        self.sell_price = 10

    def item_use(self):
        self.gc_input.update_game_dialogue("You read " + self.NAME)

class Book3(Item):
    NAME = "Book 3"
    USETYPE = "Reusable"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)
        self.sell_price = 10

    def item_use(self):
        self.gc_input.update_game_dialogue("You read " + self.NAME)

class Mask(Item):
    NAME = "Mask"
    USETYPE = "Reusable"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)
        self.sell_price = 10

    def item_use(self):
        self.gc_input.update_game_dialogue("You went incognito")

class Stick(Item):
    NAME = "Stick"
    USETYPE = "Reusable"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)
        self.sell_price = 10

    def item_use(self):
        self.gc_input.update_game_dialogue("You poked with the stick")

class Toy(Item):
    NAME = "Toy"
    USETYPE = "Reusable"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)
        self.sell_price = 10

    def item_use(self):
        self.gc_input.update_game_dialogue("You played with the " + self.NAME)
