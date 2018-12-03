from constants import *
import mainmenu
import overworld
import os

if __name__ == "__main__":
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
    # Initialize the pygame library
    pygame.init()
    # Create screen
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen = pygame.display.set_mode(size, pygame.NOFRAME)
    # Set window title
    pygame.display.set_caption("Food War")
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Initialize the joysticks
    pygame.joystick.init()

    p_current = P_TITLESCREEN
    playing = True
    filler = MENU_GRAY
    #current_surface = mainmenu.MainMenu(screen)
    #load = current_surface.run()
    #current_surface = overworld.OverworldScreen(screen, load)
    current_surface = overworld.OverworldScreen(screen)
    current_surface.run()


pygame.joystick.quit()
pygame.quit()
