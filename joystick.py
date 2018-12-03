from constants import *

"""
******************** EVENT HANDLERS *******************************
Action variable has 8 possible states, but start at 0 if no action is taken
1 - Left
2 - Right
3 - Up
4 - Down
5 - Accept/'A' equivalent
6 - Decline/'B' equivalent
7 - Inventory/Menu
8 - Exit
"""


def joystick_handler():
    action = 0
    # For each joystick:
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        for i in range(joystick.get_numbuttons()):
            button = joystick.get_button(i)
            if button:
                if i == 0:
                    action = ACCEPT
                elif i == 1:
                    action = REJECT
                elif i == 7:
                    action = GAME_MENU
                elif i == 6:
                    action = SYSTEM_MENU

        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        for i in range(joystick.get_numhats()):
            hat = joystick.get_hat(i)
            if hat[0] == -1:
                action = LEFT
            elif hat[0] == 1:
                action = RIGHT
            if hat[1] == -1:
                action = DOWN
            elif hat[1] == 1:
                action = UP
        return action