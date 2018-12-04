import pygame


class Tile:
    # The tile has various information about itself like what square it's equivalent too and it's image is loaded
    def __init__(self, type):
        self.type = type

    def secondary_init(self, terrain_type, dictionary, tileset):
        if terrain_type == self.type:
            tileset = tileset.rstrip() + "_map_sprites/"
            self.name = pygame.image.load(tileset + dictionary["name"].rstrip() + ".png")
            if "char" in dictionary.keys():
                self.char = pygame.image.load("npc_sprites/" + dictionary["char"].rstrip() + ".png")
            else:
                self.char = ""
            if "goes_to" in dictionary.keys():
                self.goes_to = dictionary["goes_to"].rstrip()
                self.newcords = dictionary["start"]
            else:
                self.goes_to = ""


class Map:
    def __init__(self, mapname):
        # Mapname is used to save players location
        self.mapname = mapname
        self.map = []
        file = open(mapname, "r")
        portion = 0
        tmp = []
        terrain_type = ""
        tmp_dict = {}
        for line in file:
            # Grab what tileset we'll be using
            if portion == 0:
                self.tileset = line
                portion += 1
            # Map portion
            elif portion == 1:
                if line[0] != "[":
                    for x in line.rstrip():
                        tmp.append(Tile(x))
                    self.map.append(tmp)
                    tmp = []
                else:
                    portion += 1
                    terrain_type = line[1]
            # Gives additional information to tile class
            if portion == 2:
                # If the line is a new specifier we need to give that information to the map and reset the dict
                if line[0] == "[" and line[1] != terrain_type:
                    for x, row in enumerate(self.map):
                        for y, col in enumerate(row):
                            col.secondary_init(terrain_type, tmp_dict, self.tileset)
                    self.map[x][y].secondary_init(terrain_type, tmp_dict, self.tileset)
                    tmp_dict = {}
                    terrain_type = line[1]
                elif "=" in line:
                    key, value = line.split("=")
                    tmp_dict[key] = value
        for row in self.map:
            for col in row:
                col.secondary_init(terrain_type, tmp_dict, self.tileset)
                self.map[x][y].secondary_init(terrain_type, tmp_dict, self.tileset)
