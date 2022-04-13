from spritesheet import Spritesheet


class Inventory(object):
    def __init__(self, gd_input, gc_input):
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.current_items = []
        self.current_key_items = []
        self.bag_slots = ["inventory_menu_2", "key_inventory_menu_2"]
        self.current_bag_slot = 0

    def bag_left(self):
        self.bag_slots.append(self.bag_slots.pop(self.bag_slots.index(self.bag_slots[0])))

    def change_bag_slot(self):
        self.gc_input.menu_manager.self.bag_slots[0] = True

    # TODO: Fix this up
    def bag_slot_right(self):
        self.gd_input.menu_list[self.bag_slots[self.current_bag_slot]].exit_menu()
        if self.current_bag_slot < (len(self.bag_slots)-1):
            self.current_bag_slot +=1
        elif self.current_bag_slot == (len(self.bag_slots)-1):
            self.current_bag_slot = 0
        self.gd_input.menu_list[self.bag_slots[self.current_bag_slot]].set_menu()

    def bag_slot_left(self):
        print(self.gd_input.menu_list[self.bag_slots[self.current_bag_slot]])
        print(self.current_bag_slot)

        self.gd_input.menu_list[self.bag_slots[self.current_bag_slot]].exit_menu()
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

        print(self.gd_input.menu_list[self.bag_slots[self.current_bag_slot]])
        print(self.current_bag_slot)
        self.gd_input.menu_list[self.bag_slots[self.current_bag_slot]].set_menu()

    def reset_bag_slot(self):
        self.current_bag_slot = 0

    def get_item(self, item_name: str, quantity_acquired: int):
        if item_name in self.current_items:
            self.gd_input.item_list[item_name].quantity += quantity_acquired
        else:
            self.current_items.append(self.gd_input.item_list[item_name].name)
            self.gd_input.item_list[item_name].quantity += quantity_acquired

    def unget_item(self, item_name: str, quantity_used: int):
        if (item_name in self.current_items) and (quantity_used <= self.gd_input.item_list[item_name].quantity):
            self.gd_input.item_list[item_name].quantity -= quantity_used

        elif (item_name in self.current_items) and (quantity_used > self.gd_input.item_list[item_name].quantity):
            self.gc_input.update_game_dialogue("You do not have enough " + str(item_name))
        else:
            print("there was nothing to remove??")

        if self.gd_input.item_list[item_name].quantity == 0:
            self.current_items.remove(self.gd_input.item_list[item_name].name)

    def use_up_item(self, item_name: str, quantity_used: int):
        #TODO: Make sure this can't go below 0
        if self.gd_input.item_list[item_name].quantity > quantity_used:
            self.gd_input.item_list[item_name].quantity -= quantity_used
            print(self.gd_input.item_list[item_name].quantity)
        elif self.gd_input.item_list[item_name].quantity == quantity_used:
            self.current_items.remove(self.gd_input.item_list[item_name].name)
            self.gd_input.item_list[item_name].quantity -= quantity_used
            print(str(self.gd_input.item_list[item_name].quantity) + " part2")
        else:
            print("you cannot use that now")

    def get_key_item(self, key_item_name: str):
        self.current_key_items.append(self.gd_input.key_item_list[key_item_name].name)
        self.gd_input.key_item_list[key_item_name].quantity = 1

    def use_up_key_item(self, key_item_name: str):
        self.gd_input.key_item_list[key_item_name].quantity = 0
        self.current_key_items.pop(self.gd_input.key_item_list[key_item_name].name)

    def sort_current_items(self):
        self.gc_input.inventory.current_items = sorted(self.gc_input.inventory.current_items)

class Outfit(object):
    NAME = "Outfit"
    def __init__(self, gc_input, gd_input):
        self.gd_input = gd_input
        self.gc_input = gc_input
        self.name = self.NAME
        self.have = False
        self.spritesheet = None

    def wear_outfit(self):
        self.gd_input.player["Player"].put_on_outfit(self.spritesheet)

class CowboyOutfit(Outfit):
    NAME = "Cowboy Outfit"
    def __init__(self, gd_input, gc_input):
        super().__init__(gc_input, gd_input)
        self.name = self.NAME
        self.have = False
        self.spritesheet = Spritesheet("assets/player/Player_cowboy_CS.png", 32, 40)
        self.display_pic = self.spritesheet.get_image(0, 0)

class NormalOutfit(Outfit):
    NAME = "Normal Outfit"
    def __init__(self, gd_input, gc_input):
        super().__init__(gc_input, gd_input)
        self.name = self.NAME
        self.have = False
        self.spritesheet = Spritesheet("assets/player/Player_CS.png", 32, 40)
        self.display_pic = self.spritesheet.get_image(0, 0)

class FrogOutfit(Outfit):
    NAME = "Frog Outfit"
    def __init__(self, gd_input, gc_input):
        super().__init__(gc_input, gd_input)
        self.name = self.NAME
        self.have = False
        self.spritesheet = Spritesheet("assets/player/Player_frog_CS.png", 32, 40)
        self.display_pic = self.spritesheet.get_image(0, 0)

class ShumaOutfit(Outfit):
    NAME = "Shuma Outfit"
    def __init__(self, gd_input, gc_input):
        super().__init__(gc_input, gd_input)
        self.name = self.NAME
        self.have = False
        self.spritesheet = Spritesheet("assets/NPC_sprites/Shuma_CS.png", 32, 40)
        self.display_pic = self.spritesheet.get_image(0, 0)