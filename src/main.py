import pygame
from data import *

gd = GameData()
gc = GameController(gd)

pygame.init()
pygame.display.set_caption('NPC')

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print("nice!")

pygame.display.update()
gc.tick()