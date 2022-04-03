from inventory import *
from menus import *
from items import *


class GoalManager(object):
    def __init__(self, gd_input, gc_input):
        self.gd_input = gd_input
        self.gc_input = gc_input

    def check_goals(self):
        if len(self.gd_input.goal_list) > 0:
            for goal in self.gd_input.goal_list:
                if self.gd_input.goal_list[goal].status == "incomplete":
                    self.gd_input.goal_list[goal].check_requirement()
                    if self.gd_input.goal_list[goal].requirement:
                        self.gc_input.update_game_dialogue(str(self.gd_input.goal_list[goal].name) + " done, you received a " + self.gd_input.goal_list[goal].reward + "!")
                        self.gc_input.inventory.get_item(self.gd_input.goal_list[goal].reward, 1)
                        self.gd_input.goal_list[goal].status = "complete"
                    else:
                        pass
                else:
                    pass

class Goal(object):
    def __init__(self, gd_input, gc_input):
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.status = "incomplete"
        self.name = self.NAME

class Goal1(Goal):
    NAME = "Goal 1"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)
        self.requirement = ("You saved the game!" in self.gd_input.menu_list[GameActionDialogue.NAME].menu_item_list)
        self.reward = TimeSeed.NAME

    def check_requirement(self):
        self.requirement = ("You saved the game!" in self.gd_input.menu_list[GameActionDialogue.NAME].menu_item_list)

class Goal2(Goal):
    NAME = "Goal 2"

    def __init__(self, gd_input, gc_input):
        super().__init__(gd_input, gc_input)
        self.requirement = ("goal 2", self.gd_input.menu_list[CharacterDialogue.NAME].talking_to == "Donna")
        self.reward = Book1.NAME


    def check_requirement(self):
        self.requirement = (self.gd_input.menu_list[CharacterDialogue.NAME].talking_to == "Donna")
