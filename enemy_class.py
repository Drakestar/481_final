import pygame
import random


class Enemy:
    # Kept it nice and simple, could have had enemy information in a file then load them into these values, but eh
    def __init__(self, name):
        self.name = name
        self.image = pygame.image.load("enemy_sprites/" + name + ".png")
        self.hp = random.randint(18, 30)
        self.defense = random.randint(1, 6)
        self.strength = random.randint(1, 4)

    def attack(self):
        return random.randint(1, 3) + self.strength

    def take_damage(self, damage_taken):
        self.hp -= (damage_taken - self.defense)
