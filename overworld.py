import maphandler
import joystick
from constants import *


class OverworldScreen(pygame.Surface):

    def __init__(self, surface, loadgame="new"):
        self.screen = surface
        self.player_loc = [1, 1]
        self.player_dir = 3
        self.map = maphandler.Map("maps/test.map")
        self.forward = pygame.image.load("player_sprites/forward.png")
        self.back = pygame.image.load("player_sprites/back.png")
        self.left = pygame.image.load("player_sprites/left.png")
        self.right = pygame.image.load("player_sprites/right.png")

    def run(self):
        clock = pygame.time.Clock()
        while True:
            action = 0
            for event in pygame.event.get():
                # Handle pressing the 'X' in the top-right to close the program
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F4 and bool(event.mod & pygame.KMOD_ALT):
                        pygame.display.quit()
                        pygame.quit()
                    if event.key in keyboard_dict.keys():
                        action = keyboard_dict[event.key]
                else:
                    action = joystick.joystick_handler()

            # Draw world
            self.draw()
            # Draw conversations
            # Draw menu
            self.input_handler(action)
            pygame.display.flip()
            clock.tick(60)

    def draw(self):
        self.screen.fill(MENU_GRAY)
        w, h = pygame.display.get_surface().get_size()
        pic_size = self.map.map[0][0].name.get_width()
        w = (w - pic_size) / 2
        h = (h - pic_size) / 2
        # Just in case although it should never come up
        # Draw base map
        for y, row in enumerate(self.map.map):
            for x, col in enumerate(row):
                self.screen.blit(col.name, ((x - self.player_loc[0]) * pic_size + w, (y - self.player_loc[1]) * pic_size + h))
                if col.type == "a":
                    self.screen.blit(col.char,
                                     ((x - self.player_loc[0]) * pic_size + w, (y - self.player_loc[1]) * pic_size + h))

        # Draw things on map
        player = self.direction_handler()
        self.screen.blit(player, (w, h))

    def direction_handler(self):
        if self.player_dir == 0:
            return self.back
        elif self.player_dir == 1:
            return self.left
        elif self.player_dir == 2:
            return self.forward
        elif self.player_dir == 3:
            return self.right

    def input_handler(self, player_input):
        tmp_X = self.player_loc[1]
        tmp_Y = self.player_loc[0]
        if player_input in (UP, LEFT, DOWN, RIGHT):
            if player_input == UP:
                tmp_X -= 1
                self.player_dir = 0
            elif player_input == DOWN:
                tmp_X += 1
                self.player_dir = 2
            elif player_input == LEFT:
                tmp_Y -= 1
                self.player_dir = 1
            elif player_input == RIGHT:
                tmp_Y += 1
                self.player_dir = 3
            if self.map.map[tmp_X][tmp_Y].type == ".":
                self.player_loc = [tmp_Y, tmp_X]
            elif self.map.map[tmp_X][tmp_Y].type == "1":
                newX, newY = self.map.map[tmp_X][tmp_Y].newcords.split(",")
                self.player_loc = [int(newY), int(newX)]
                tmp = self.map.map[tmp_X][tmp_Y].goes_to
                self.map = maphandler.Map(tmp)

        elif player_input == ACCEPT:
            print("temp")

