import maphandler
import joystick
import random
import combat
import xml.etree.ElementTree as ET
import player_class
from constants import *


class OverworldScreen(pygame.Surface):

    def __init__(self, surface, loadgame="saves/new.xml"):
        self.screen = surface
        self.player_dir = 3
        self.is_fighting = False
        self.fight_chance = 0
        self.player = self.loadplayer(loadgame)
        self.player_loc = self.player.coords
        self.map = maphandler.Map(self.player.map)
        self.forward = pygame.image.load("player_sprites/forward.png")
        self.back = pygame.image.load("player_sprites/back.png")
        self.left = pygame.image.load("player_sprites/left.png")
        self.right = pygame.image.load("player_sprites/right.png")

    # Main gameplay loop
    def run(self):
        # Set clock for fps
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
                    if event.key in keyboard_dict.keys():
                        action = keyboard_dict[event.key]
                # Handle any joystick actions over the keyboard actions
                else:
                    action = joystick.joystick_handler()
            # If there is a fight
            if self.is_fighting:
                self.is_fighting = False
                fight = combat.Combat(self.screen, self.player)
                self.player = fight.run()
            # Draw world
            self.draw()

            self.input_handler(action)
            pygame.display.flip()
            clock.tick(60)

    # Draw call to draw the world
    def draw(self):
        # Fill any background
        self.screen.fill(MENU_GRAY)
        # Get width and height of overall screen for printing the tiles to screen
        w, h = pygame.display.get_surface().get_size()
        pic_size = self.map.map[0][0].name.get_width()
        w = (w - pic_size) / 2
        h = (h - pic_size) / 2
        # Loop through tiles
        for y, row in enumerate(self.map.map):
            for x, col in enumerate(row):
                # Print whatever the tiles name is
                self.screen.blit(col.name, ((x - self.player_loc[0]) * pic_size + w, (y - self.player_loc[1]) * pic_size + h))
                # For things other than an npc could easily do between a-z or A-Z to coincide with any special things on
                # a tile
                if col.type == "a":
                    self.screen.blit(col.char,
                                     ((x - self.player_loc[0]) * pic_size + w, (y - self.player_loc[1]) * pic_size + h))

        # Draw player on map with their direction
        player = self.direction_handler()
        self.screen.blit(player, (w, h))

    # Checks which direction the player should be facing
    def direction_handler(self):
        if self.player_dir == 0:
            return self.back
        elif self.player_dir == 1:
            return self.left
        elif self.player_dir == 2:
            return self.forward
        elif self.player_dir == 3:
            return self.right

    # Handles input and determines whether a fight will start
    def input_handler(self, player_input):
        # Create new temp location for checking whether a new location will work
        tmp_X = self.player_loc[1]
        tmp_Y = self.player_loc[0]
        if player_input in (UP, LEFT, DOWN, RIGHT):
            # Basically a switch statement that changes direction regardless of actual movement
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
            # The player was able to actually move so do stuff
            if self.map.map[tmp_X][tmp_Y].type == ".":
                # Set the players new location
                self.player_loc = [tmp_Y, tmp_X]
                # Calculate whether they end up in a fight
                if random.random() <= self.fight_chance:
                    self.fight_chance = 0
                    self.is_fighting = True
                else:
                    self.fight_chance += .025
            elif self.map.map[tmp_X][tmp_Y].type == "1":
                newX, newY = self.map.map[tmp_X][tmp_Y].newcords.split(",")
                self.player_loc = [int(newY), int(newX)]
                tmp = self.map.map[tmp_X][tmp_Y].goes_to
                self.map = maphandler.Map(tmp)

        elif player_input == ACCEPT:
            self.saveplayer()

    def loadplayer(self, load_name):
        tmp = player_class.Player()
        tree = ET.parse(load_name)
        root = tree.getroot()
        tmp.maphp = int(root[0].text)
        tmp.hp = int(root[1].text)
        tmp.maxmp = int(root[2].text)
        tmp.mp = int(root[3].text)
        tmp.level = int(root[4].text)
        tmp.xp = int(root[5].text)
        for equipment in root[6]:
            tmp.equip(equipment.text, equipment.attrib)
        for spells in root[7]:
            tmp.make_spell(spells.text, spells.attrib)
        for items in root[8]:
            tmp.get_item(items.text, items.attrib)
        tmp.map = root[9].text
        tmp.coords = [int(root[9].attrib['x']), int(root[9].attrib['y'])]
        return tmp

    def saveplayer(self):
        root = ET.Element("player")
        ET.SubElement(root, "maxhp").text = str(self.player.maxhp)
        ET.SubElement(root, "hp").text = str(self.player.hp)
        ET.SubElement(root, "maxmp").text = str(self.player.maxmp)
        ET.SubElement(root, "mp").text = str(self.player.mp)
        ET.SubElement(root, "level").text = str(self.player.level)
        ET.SubElement(root, "xp").text = str(self.player.xp)
        equipment = ET.SubElement(root, "equipped")
        ET.SubElement(equipment, "helmet", defense="5").text = list(self.player.equipment.keys())[0]
        spells = ET.SubElement(root, "spells")
        ET.SubElement(spells, "spell", type="damage", target="aoe", cost="5", amount="10").text = "Fireball"
        ET.SubElement(spells, "spell", type="heal", target="ally", cost="10", amount="20").text = "Heal"
        items = ET.SubElement(root, "items")
        ET.SubElement(items, "item", amount="5", type="heal", target="ally", heal="10").text = "Healing Potion"
        ET.SubElement(root, "location", x=str(self.player_loc[0]), y=str(self.player_loc[1])).text = self.map.mapname
        tree = ET.ElementTree(root)
        tree.write("saves/old.xml")
