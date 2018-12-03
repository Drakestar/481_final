import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MENU_GRAY = (40, 40, 40)
LIGHT_BLUE = (100, 100, 255)

WIDTH = 960
HEIGHT = 640
SCREEN_SIZE = [WIDTH, HEIGHT]

P_TITLESCREEN = 0
P_SETTINGS = 1
P_GAME = 2

MAP_FLOOR = 0
MAP_WALL = 1
MAP_NPC = 2
MAP_EXIT = 3

LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
ACCEPT = 5
REJECT = 6
GAME_MENU = 7
SYSTEM_MENU = 8

keyboard_dict = {pygame.K_LEFT: 1, pygame.K_RIGHT: 2, pygame.K_UP: 3, pygame.K_DOWN: 4, pygame.K_z: 5, pygame.K_x: 6,
                 pygame.K_c: 7, pygame.K_ESCAPE: 8}
