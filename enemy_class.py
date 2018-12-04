import pygame
import random

class Enemy:

    def __init__(self, name):
        self.name = name
        self.image = pygame.image.load("enemy_sprites/" + name + ".png")
        self.hp = random.randint(18, 30)
        self.defense = random.randint(1, 6)
        self.strength = random.randint(1, 6)

    def attack(self):
        return random.randint(7, 16) + self.strength

    def take_damage(self, damage_taken):
        self.hp -= (damage_taken - self.defense)
