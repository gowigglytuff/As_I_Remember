class KeyItem(object):
    def __init__(self, gd_input, gc_input):
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.name = self.NAME
        self.quantity = 0
        pass

    def use_item(self):
        if self.check_if_can_use_item():
            print("You used the " + self.name)
            self.gc_input.update_game_dialogue("You used the " + str(self.name))
            self.item_use()
        else:
            self.fail_to_use_item()

    def item_use(self):
        pass

    def check_if_can_use_item(self):
        result = True
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("You can't use that now!")


class Shovel(KeyItem):
    NAME = "Shovel"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)

    def item_use(self):
        facing_tile = self.gd_input.player["Player"].check_adj_tile(self.gd_input.player["Player"].get_direct(self.gd_input.player["Player"].facing))
        object_filling = facing_tile.object_filling
        filling_type = facing_tile.filling_type
        full = facing_tile.full

        if full:
            print(object_filling, filling_type)

            if object_filling == "rock":
                pass


    def check_if_can_use_item(self):
            result = False
            facing_tile = self.gd_input.player["Player"].check_adj_tile(self.gd_input.player["Player"].get_direct(self.gd_input.player["Player"].facing))
            filling_type = facing_tile.filling_type
            if filling_type == "Rock":
                result = True
            else:
                pass
            return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("You can't use that now!")


class Hammer(KeyItem):
    NAME = "Hammer"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)

    def item_use(self):
        facing_tile = self.gd_input.player["Player"].check_adj_tile(self.gd_input.player["Player"].get_direct(self.gd_input.player["Player"].facing))
        object_filling = facing_tile.object_filling
        filling_type = facing_tile.filling_type
        full = facing_tile.full

        if full:
            if filling_type == "Prop":

                if self.gd_input.prop_list[object_filling]._TYPENAME in ["large stone"]:
                    self.gd_input.prop_list[object_filling].dissolve()
                    self.gc_input.update_game_dialogue("Your mighty blow shattered the stone!")
                else:
                    pass
            else:
                pass
        else:
            pass

    def check_if_can_use_item(self):
        result = False
        facing_tile = self.gd_input.player["Player"].check_adj_tile(self.gd_input.player["Player"].get_direct(self.gd_input.player["Player"].facing))
        object_filling = facing_tile.object_filling
        filling_type = facing_tile.filling_type
        full = facing_tile.full

        if full:
            if filling_type == "Prop":
                if self.gd_input.prop_list[object_filling]._TYPENAME in ["large stone"]:
                    result = True
        else:
            pass
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("You can't use that now!")


class SeedPouch(KeyItem):
    NAME = "Seed Pouch"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)

    def item_use(self):
        self.gc_input.get_coins(10)

    def check_if_can_use_item(self):
        result = True
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("You can't use that now!")