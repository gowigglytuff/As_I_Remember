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
        if item_name in self.current_items:
            self.gd_input.item_list[item_name].quantity -= quantity_used
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


