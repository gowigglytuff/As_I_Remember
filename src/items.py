
from features import *

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
        if self.gd_input.player["Player"].x % 2 == 0:
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
        self.gc_input.update_game_dialogue("The wind hums joyously! Time passes...")
        self.gc_input.time_of_day += 1


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

class FossilA(Item):
    NAME = "Fossil A"
    USETYPE = "Single"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)
        self.sell_price = 100

    def item_use(self):
        self.gc_input.update_game_dialogue("It's an interesting fossil!")

class FossilB(Item):
    NAME = "Fossil B"
    USETYPE = "Single"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)
        self.sell_price = 200

    def item_use(self):
        self.gc_input.update_game_dialogue("It's an interesting fossil!")

class FossilC(Item):
    NAME = "Fossil C"
    USETYPE = "Single"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)
        self.sell_price = 500

    def item_use(self):
        self.gc_input.update_game_dialogue("It's an interesting fossil!")