import constants
import pygame
import random
import player_class
import enemy_class
import joystick


class Combat(pygame.Surface):

    # Player has
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.fontsize = 30
        self.enemy_list = []
        self.selecting = False
        self.in_submenu = False
        self.action_choice = 0
        self.sub_choice = 0
        self.selection_choice = 0
        self.sub_menu = ""
        self.my_font = pygame.font.SysFont('Arial Black', self.fontsize)  # creates the font, size 15 (you can change this)
        self.pointer_image = pygame.image.load("player_sprites/pointer.png")
        self.pointer_image = pygame.transform.smoothscale(self.pointer_image, (int(self.pointer_image.get_width() / 2), int(self.pointer_image.get_height() / 2)))
        # Come up with enemies
        for x in range(1, random.randint(2, 4)):
            self.enemy_list.append(enemy_class.Enemy(random.choice(constants.enemies)))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            # Reset any possible action
            action = 0
            # Go through any actions taken by the user
            for event in pygame.event.get():
                # Key events
                if event.type == pygame.KEYDOWN:
                    # Alt+F4 = quitting
                    if event.key == pygame.K_F4 and bool(event.mod & pygame.KMOD_ALT):
                        pygame.display.quit()
                        pygame.quit()
                    # Handle actual controls
                    if event.key in constants.keyboard_dict.keys():
                        action = constants.keyboard_dict[event.key]
                # Handle any joystick actions over the keyboard actions
                else:
                    action = joystick.joystick_handler()

            # Draw screen
            self.draw()

            if self.selecting:
                self.select_handler(action)
            elif self.in_submenu:
                self.sub_menu_handler(action)
            else:
                self.menu_handler(action)
            pygame.display.flip()
            clock.tick(60)
            # Handle actions

            if not self.enemy_list:
                return self.player

    def draw(self):
        self.screen.fill(constants.MENU_GRAY)
        w, h = self.screen.get_size()
        # Draw box that holds menu options
        pygame.draw.rect(self.screen, constants.LIGHT_BLUE, (1, h * 2 / 3, w, h * 1 / 3))  # makes the box
        pygame.draw.rect(self.screen, (255, 255, 255), (1, h * 2 / 3, w - 4, h * 1 / 3 - 3), 5)  # makes outline around the box
        # Draw enemies
        for index, enemy in enumerate(self.enemy_list):
            self.screen.blit(enemy.image, (self.screen.get_height() * (index + 1) / len(self.enemy_list), self.screen.get_height() / 4))
            self.draw_menu_item("HP: " + str(enemy.hp), (self.screen.get_height() * (index + 1) / len(self.enemy_list), self.screen.get_height() / 4 - self.fontsize))
        # Draw/write menu options
        for index, option in enumerate(constants.fight_options):
            self.draw_menu_item(option, [300, (self.screen.get_height() * 5 / 7) + index * (self.fontsize + 30)])
        self.draw_menu_item("HP: " + str(self.player.hp), [50, (self.screen.get_height() * 5 / 7) + 0 * (self.fontsize + 30)])
        self.draw_menu_item("MP: " + str(self.player.mp), [50, (self.screen.get_height() * 5 / 7) + 1 * (self.fontsize + 30)])
        self.draw_menu_item("Lvl:" + str(self.player.level), [50, (self.screen.get_height() * 5 / 7) + 2 * (self.fontsize + 30)])
        self.draw_menu_item("XP:" + str(self.player.xp), [50, (self.screen.get_height() * 5 / 7) + 3 * (self.fontsize + 30)])

        # Draw pointer
        self.screen.blit(pygame.transform.rotate(self.pointer_image, 90), [220, (self.screen.get_height() * 5 / 7) + self.action_choice * (self.fontsize + 30) - int(self.pointer_image.get_width() / 4)])
        # Draw fight selector if applicable
        if self.selecting:
            self.screen.blit(self.pointer_image, [self.screen.get_height() * (self.selection_choice + 1) / len(self.enemy_list) + self.pointer_image.get_width(), self.screen.get_height() / 4 - self.pointer_image.get_height()])
        if self.in_submenu:
            pygame.draw.rect(self.screen, constants.LIGHT_BLUE, (500, h * 2 / 3 + 25, 300, 300))  # makes the box
            pygame.draw.rect(self.screen, (255, 255, 255),      (500, h * 2 / 3 + 25, 300, 300), 5)  # makes outline around the box
            for index, option in enumerate(self.submenu_items):
                self.draw_menu_item(option, [520, (self.screen.get_height() * 5 / 7) + index * (self.fontsize + 30)])
            self.screen.blit(pygame.transform.rotate(self.pointer_image, 90), [420, (self.screen.get_height() * 5 / 7) + self.sub_choice * (self.fontsize + 30) - int(self.pointer_image.get_width() / 4)])

    def draw_menu_item(self, text, location):
        label = self.my_font.render(text, 1, constants.BLACK)  # creates the label
        self.screen.blit(label, (location[0], location[1]))  # renders the label

    def menu_handler(self, input):
        if input == constants.UP:
            self.action_choice -= 1
            if self.action_choice < 0:
                self.action_choice = 3
        elif input == constants.DOWN:
            self.action_choice += 1
            if self.action_choice > len(constants.fight_options) - 1:
                self.action_choice = 0
        elif input == constants.ACCEPT:
            self.action_picker()

    def action_picker(self):
        if self.action_choice == 0:
            self.selecting = True
        elif self.action_choice == 1:
            self.sub_menu = "spell"
            self.submenu_items = list(self.player.spells.keys())
            self.in_submenu = True
        elif self.action_choice == 2:
            self.in_submenu = True
            self.submenu_items = self.player.items
            self.sub_menu = 'items'
        else:
            self.enemy_list = []

    def select_handler(self, input):
        if input == constants.LEFT:
            self.selection_choice -= 1
            if self.selection_choice < 0:
                self.selection_choice = len(self.enemy_list) - 1
        elif input == constants.RIGHT:
            self.selection_choice += 1
            if self.selection_choice > len(self.enemy_list) - 1:
                self.selection_choice = 0
        elif input == constants.ACCEPT:
            self.selection_picker()
            self.selecting = False
            for enemy in self.enemy_list:
                self.player.hp -= enemy.attack()
                if self.player.hp <= 0:
                    pygame.QUIT()
        elif input == constants.REJECT:
            self.selecting = False

    def selection_picker(self):
        self.enemy_list[self.selection_choice].take_damage(self.player.attack())
        if self.enemy_list[self.selection_choice].hp <= 0:
            self.enemy_list.pop(self.selection_choice)
            print(self.player.xp)
            self.player.get_xp(random.randint(10, 15))
        if len(self.enemy_list) - 1 < self.selection_choice:
            self.selection_choice -= 1

    def sub_menu_handler(self, input):
        if input == constants.UP:
            self.sub_choice -= 1
            if self.sub_choice < 0:
                self.sub_choice = len(self.submenu_items) - 1
        elif input == constants.DOWN:
            self.sub_choice += 1
            if self.sub_choice > len(self.submenu_items) - 1:
                self.sub_choice = 0
        elif input == constants.ACCEPT:
            self.submenu_picker()
            for enemy in self.enemy_list:
                self.player.hp -= enemy.attack()
                if self.player.hp <= 0:
                    pygame.QUIT()
            self.in_submenu = False
        elif input == constants.REJECT:
            self.in_submenu = False

    def submenu_picker(self):
        if self.sub_menu == "spell":
            damage = self.player.cast_spell(self.submenu_items[self.sub_choice])
            if damage > 0:
                removables = []
                for enemy in self.enemy_list:
                    enemy.take_damage(int(damage))
                    if enemy.hp <= 0:
                        removables.append(enemy)
                for enemy in removables:
                    print(self.player.xp)
                    self.player.get_xp(random.randint(10, 15))
                    self.enemy_list.remove(enemy)
        else:
            self.player.use_item()



