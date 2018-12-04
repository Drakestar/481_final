import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MENU_GRAY = (50, 50, 50)
LIGHT_BLUE = (100, 100, 255)

WIDTH = 960
HEIGHT = 640
SCREEN_SIZE = [WIDTH, HEIGHT]

LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
ACCEPT = 5
REJECT = 6
GAME_MENU = 7
SYSTEM_MENU = 8

enemies = ["flan", "ghoast", "sasquash", "slider", "spaghyetti"]

fight_options = ["Fight", "Spell", "Item", "Flee"]

keyboard_dict = {pygame.K_LEFT: 1, pygame.K_RIGHT: 2, pygame.K_UP: 3, pygame.K_DOWN: 4, pygame.K_z: 5, pygame.K_x: 6,
                 pygame.K_c: 7, pygame.K_ESCAPE: 8}
