from random import randint

import pygame
from data import *
from loading import *
from features import *
from mapClasses import *

gd = GameData()
gc = GameController(gd)
em = EventsManager(gd, gc)
picaso = Picaso(gd, gc)

def main():
    init_game(gd, gc)
    run_game_loop()


def run_game_loop():
    running = True

    # NPC1 = Feature(4, 3, 128, 128, ["assets/NPC.png", "assets/NPC - f2.png", "assets/NPC-blue.png"], "Mary")
    Phrase1 = Phrase("Hello World", True, 100, 300, (255, 255, 255), 20)
    Phrase2 = Phrase("Goodbye World", True, 100, 300, (255, 255, 255), 20)

    # set up the events that allow things to move (add these to the individual classes of each of the dudes)
    printout = pygame.USEREVENT + 3
    pygame.time.set_timer(printout, 500)

    player_steps_timer = pygame.USEREVENT + 7
    pygame.time.set_timer(player_steps_timer, 20)

    current_phrase = None


    while running:
        pygame.draw.rect(gc.screen, (255, 255, 2), (0, 0, 500, 500))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if gc.input:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_1:
                        current_phrase = Phrase1
                        current_phrase.write_phrase_slowly(200)
                        gc.LockInput()

                    if event.key == pygame.K_2:
                        current_phrase = Phrase2
                        current_phrase.write_phrase_slowly(200)
                        gc.LockInput()

                    if event.key == pygame.K_RIGHT:
                        gd.player["Player"].turn_right()
                        can_move = gd.positioner[gc.room].can_move(gd.player["Player"])
                        if can_move:
                            gd.player["Player"].walk_right()
                            gd.player["Player"].walk_cycle()
                            gc.LockInput()
                        else:
                            pass


                    if event.key == pygame.K_LEFT:
                        gd.player["Player"].turn_left()
                        can_move = gd.positioner[gc.room].can_move(gd.player["Player"])
                        if can_move:
                            gd.player["Player"].walk_left()
                            gd.player["Player"].walk_cycle()
                            gc.LockInput()
                        else:
                            pass

                    if event.key == pygame.K_UP:
                        gd.player["Player"].turn_back()
                        can_move = gd.positioner[gc.room].can_move(gd.player["Player"])
                        if can_move:
                            gd.player["Player"].walk_back()
                            gd.player["Player"].walk_cycle()
                            gc.LockInput()
                        else:
                            pass

                    if event.key == pygame.K_DOWN:
                        gd.player["Player"].turn_front()
                        can_move = gd.positioner[gc.room].can_move(gd.player["Player"])
                        if can_move:
                            gd.player["Player"].walk_front()
                            gd.player["Player"].walk_cycle()
                            gc.LockInput()
                        else:
                            pass

                    if event.key == pygame.K_RETURN:

                        test_facing = gd.player["Player"].get_facing_tile()
                        print("player facingx: " + (str(test_facing.x) + ", " + "player facingy: " + str(test_facing.y)))
                        print("player x: " + str(gd.player["Player"].x) + ", " + "player y: " + str(gd.player["Player"].y))

                    if event.key == pygame.K_SPACE:
                        print("player x: " + str(gd.player["Player"].x))
                        print("player imagex: " + str(gd.player["Player"].imagex))
                        print("player y: " + str(gd.player["Player"].y))
                        print("player imagey: " + str(gd.player["Player"].imagey))

                        print("Tiles grid fill list:")
                        for item in gd.room[gc.room].tiles_array:
                            for x in item:
                                print(str(x.x) + ", " + str(x.y) + ":" + x.object_filling)

                        Drawables = gd.get_all_drawables()
                        print(Drawables[1].x)
                        print(Drawables[1].y)

            # check to see if any events have occured
            for character in gd.character:
                if event.type == gd.character[character].initiate:
                    if gd.character[character].state == "idle":
                        gd.character[character].do_activity()

            #check for a single step in series of walk cycle steps for each character
            for character in gd.character:
                if event.type == gd.character[character].walk_clock:
                    gd.character[character].check_if_walking()

            # check for a single step in series of walk cycle steps for Player
            if event.type == player_steps_timer:
                gd.player["Player"].check_if_walking()


        if current_phrase is not None:
            current_phrase.write_current_phrase(gc.screen)

        picaso.big_draw()
        pygame.display.update()
        gc.tick()


if __name__ == "__main__":
    main()