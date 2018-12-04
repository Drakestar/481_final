import random


class Player:
    def __init__(self):
        self.maxhp = 100
        self.hp = 100
        self.maxmp = 50
        self.mp = 50
        self.level = 1
        self.xp = 50
        self.strength = 5
        self.defense = 0
        self.equipment = {}
        self.spells = {}
        self.items = {}
        self.map = "maps/test.map"
        self.coords = [2, 4]

    def equip(self, new_armor, dictionary):
        self.defense += int(dictionary['defense'])
        self.equipment[new_armor] = dictionary

    def make_spell(self, name, dictionary):
        self.spells[name] = Spell(dictionary)

    def attack(self):
        return random.randrange(self.level, self.strength + self.level)

    def take_hit(self, damage):
        self.hp -= (damage - self.defense)

    def get_item(self, name, dictionary):
        self.items[name] = dictionary

    def cast_spell(self, spellname):
        if self.spells[spellname].type == 'heal' and self.mp - self.spells[spellname].cost >= 0:
            self.hp += int(self.spells[spellname].amount)
            self.mp -= int(self.spells[spellname].cost)
            return 0
        elif self.spells[spellname].type == 'damage' and self.mp - self.spells[spellname].cost >= 0:
            self.mp -= int(self.spells[spellname].cost)
            return self.spells[spellname].amount
        else:
            return 0

    def use_item(self):
        print(self.items)
        self.hp += int(self.items['Healing Potion']['amount'])

    def get_xp(self, amount):
        self.xp += amount
        if self.xp >= 100:
            self.level += 1
            self.xp = 0
            self.maxhp += 10
            self.hp = self.maxhp
            self.maxmp += 5
            self.mp = self.maxmp
            self.strength += 1

class Spell:
    def __init__(self, dictionary):
        self.type = dictionary['type']
        self.target = dictionary['target']
        self.cost = int(dictionary['cost'])
        self.amount = int(dictionary['amount'])
