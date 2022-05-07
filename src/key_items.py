class KeyItem(object):
    def __init__(self, gd_input, gc_input):
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.name = self.NAME
        self.quantity = 0
        pass

    def use_item(self):
        if self.check_if_can_use_item():
            self.gc_input.update_game_dialogue("You used the " + str(self.name))
            self.item_use()

        else:
            self.gc_input.update_game_dialogue("You attempted to use the " + str(self.name))
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
        # TODO: Give this a use
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
        self.gc_input.update_game_dialogue("You can't use that now...")


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
        self.gc_input.update_game_dialogue("You can't use that now...")


class SeedPouch(KeyItem):
    NAME = "Seed Pouch"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)

    def item_use(self):
        # TODO: Give this a use
        self.gc_input.update_game_dialogue("You keep your Time Seeds in there!")

    def check_if_can_use_item(self):
        result = True
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("You can't use that now...")


class HitchingThumb(KeyItem):
    NAME = "Hitching Thumb"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)

    def item_use(self):
        self.gd_input.menu_list["hitchiking_menu"].set_menu()

    def check_if_can_use_item(self):
        # TODO: Make it check if it's near a road
        result = True
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("You can only use that near a road!")


class WaterBottle(KeyItem):
    NAME = "Water Bottle"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)

    def item_use(self):
        # TODO: Give this a use
        self.gc_input.update_game_dialogue("You took a refreshing drink of water!")

    def check_if_can_use_item(self):
        result = True
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("It's empty!")


class GymPass(KeyItem):
    NAME = "Gym Pass"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)

    def item_use(self):
        # TODO: Give this a use
        self.gc_input.update_game_dialogue("You can use this to go to the gym")

    def check_if_can_use_item(self):
        result = True
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("You're not at the gym...")


class BirdCall(KeyItem):
    NAME = "Bird Call"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)

    def item_use(self):
        # TODO: Give this a use
        self.gc_input.update_game_dialogue("It made a sound like a bird!")

    def check_if_can_use_item(self):
        result = True
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("It made a wheezing sound...")


class Cellphone(KeyItem):
    NAME = "Cellphone"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)

    def item_use(self):
        # TODO: Give this a use
        self.gc_input.update_game_dialogue("You called Grandma!")

    def check_if_can_use_item(self):
        # TODO: Make it so that this can only be used on a few tiles in the whole game and drop hints about it
        result = False
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("There isn't any signal here...")


class Gameboy(KeyItem):
    NAME = "Gameboy"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)

    def item_use(self):
        # TODO: Give this a use
        self.gc_input.update_game_dialogue("You played your favourite game!")

    def check_if_can_use_item(self):
        # TODO: Make it so that this lets you play/practise all the mini games you've encountered thus far
        result = True
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("It's out of batteries...")


class Net(KeyItem):
    NAME = "Net"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)

    def item_use(self):
        # TODO: Give this a use
        self.gc_input.update_game_dialogue("You swung the net!")

    def check_if_can_use_item(self):
        result = True
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("It's not the time to use that now...")


class Radio(KeyItem):
    NAME = "Radio"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)

    def item_use(self):
        # TODO: Give this a use
        self.gc_input.update_game_dialogue("Its playing CHFR!")

    def check_if_can_use_item(self):
        result = True
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("It's just making white noise")


class Lighter(KeyItem):
    NAME = "Lighter"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)

    def item_use(self):
        # TODO: Give this a use
        self.gc_input.update_game_dialogue("It made a pretty flame!")

    def check_if_can_use_item(self):
        result = False
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("We should not be playing with fire...")


class Boomerang(KeyItem):
    NAME = "Boomerang"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)

    def item_use(self):
        # TODO: Give this a use
        self.gc_input.update_game_dialogue("You threw the boomerang!")

    def check_if_can_use_item(self):
        result = False
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("It's not the time to use that now...")


class CoopNumber(KeyItem):
    NAME = "Co-op Number"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)
        self.current_number = 1859

    def item_use(self):
        # TODO: Give this a use
        self.gc_input.update_game_dialogue("It's your Co-op number: " + str(self.current_number))

    def check_if_can_use_item(self):
        result = True
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("Lets use that later...")


class Compass(KeyItem):
    NAME = "Compass"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)

    def item_use(self):
        self.gc_input.update_game_dialogue("Your current Latitude is: " + str(self.gd_input.player["Player"].x))
        self.gc_input.update_game_dialogue("Your current Longitude is: " + str(self.gd_input.player["Player"].y))

    def check_if_can_use_item(self):
        result = True
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("Lets use that later...")