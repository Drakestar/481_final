from constants import *
import joystick
import time


class MainMenu(pygame.Surface):

    def __init__(self, surface):
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.screen = surface
        self.load = "saves/new.xml"
        self.playing = True
        self.title = pygame.image.load('menu_sprites/title_screen.png')
        self.logo = pygame.image.load('menu_sprites/logo.png')
        self.logo = pygame.transform.scale(self.logo, size).convert()
        self.controls = pygame.image.load('menu_sprites/controls.png')
        self.controls = pygame.transform.scale(self.controls, size).convert()
        self.control_alpha = 255
        self.controlscreen = pygame.display.set_mode(size, pygame.NOFRAME)
        self.food_list = []
        self.food_list.append(pygame.image.load('menu_sprites/menufood1.png'))
        self.food_list.append(pygame.image.load('menu_sprites/menufood2.png'))
        self.food_list.append(pygame.image.load('menu_sprites/menufood3.png'))
        self.pointer_png = pygame.image.load('menu_sprites/menu_pointer.png')
        self.pointer = 0
        self.menu_items = ['New Game', 'Load Game', 'Exit']
        self.food_ys = [0, self.screen.get_height() / 3, self.screen.get_height() * 2 / 3]

    def run(self):
        self.firstDraw()
        clock = pygame.time.Clock()
        while self.playing:
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

            self.draw()
            self.input_handler(action)
            pygame.display.flip()
            clock.tick(60)
        return self.load

    def firstDraw(self):
        self.screen.blit(self.logo, (0, 0))
        pygame.display.flip()
        time.sleep(2)
        while self.control_alpha > 0:
            self.logo.set_alpha(self.control_alpha)
            self.control_alpha -= 5
            self.screen.blit(self.controls, (0, 0))
            self.screen.blit(self.logo, (0, 0))
            pygame.display.flip()
        self.logo.set_alpha(0)
        self.screen.blit(self.controls, (0, 0))
        self.control_alpha = 255
        time.sleep(2)

    def input_handler(self, player_input):
        if player_input == UP:
            self.pointer -= 1
            if self.pointer < 0:
                self.pointer = len(self.menu_items) - 1
        elif player_input == DOWN:
            self.pointer += 1
            if self.pointer > len(self.menu_items) - 1:
                self.pointer = 0
        elif player_input == ACCEPT:
            self.input_menu_picked()

    def input_menu_picked(self):
        if self.pointer == 0:
            self.playing = False
        elif self.pointer == 1:
            self.load = "saves/old.xml"
            self.playing = False
        elif self.pointer == 2:
            pygame.display.quit()
            pygame.quit()

    def draw(self):
        # Clear the screen
        self.screen.fill(MENU_GRAY)
        # Blit the title, and all menu items pointer
        self.screen.blit(self.title, (self.get_midpoint(self.title.get_size()[0]), 0))
        # Draw the menu buttons
        for i, option in enumerate(self.menu_items):
            self.make_button(self.screen, BLUE, WHITE, self.get_midpoint(100), 300 + 30 * i, 100, 20, option)
        # Draw the pointer to menu buttons
        self.draw_menu_pointer()
        # Draw the scrolling food
        for i, item in enumerate(self.food_list):
            self.draw_food(item, i)
        if self.control_alpha > 0:
            self.controls.set_alpha(self.control_alpha)
            self.control_alpha -= 10
            self.screen.blit(self.controls, (0, 0))

    @staticmethod
    def make_button(surface, color, text_color, x, y, width, height, text):
        pygame.draw.rect(surface, (0, 0, 0), (x - 1, y - 1, width + 2, height + 2), 1)  # makes outline around the box
        pygame.draw.rect(surface, color, (x, y, width, height))  # makes the box
        myfont = pygame.font.SysFont('Arial Black', 15)  # creates the font, size 15 (you can change this)
        label = myfont.render(text, 1, text_color)  # creates the label
        surface.blit(label, (x + 2, y))  # renders the label

    def get_midpoint(self, width):
        return (self.screen.get_width() - width) / 2

    def draw_menu_pointer(self):
        self.screen.blit(self.pointer_png, (self.get_midpoint(175), 296 + self.pointer * 30))

    def draw_food(self, food_pic, food_index):
        self.screen.blit(food_pic, (self.get_midpoint(food_pic.get_size()[0]), self.food_ys[food_index]))
        if self.food_ys[food_index] > self.screen.get_height():
            self.food_ys[food_index] = -food_pic.get_size()[1] + 10
