# Pygame Project
# Benjamin Weidner
# edited Nick Lunt 2.27.24
# ProgLang
# 2/15/2024

# tilemap.py

NEIGHBOR_OFFSETS = [(-1,0), (-1, -1), (0, -1), (1, -1), (1,0), (0,0), (-1,1), (0,1), (1,1)]
PHYSICS_TILES = {'grass', 'stone'}

import pygame
import random

class Tilemap:  
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap[str(0 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (0 + i, 10)}
        
        for j in range(-100, 10, 3):
            for i in range(3):
                spawnChance = random.randint(0,10)
                if(spawnChance < 5):
                    pass
                elif(spawnChance >= 5 & spawnChance < 8):
                    pass
                    # spawn 1 platform
                    self.tilemap[str(i) + ';' + str(j)] = {'type': 'grass', 'variant': 1, 'pos': (i, j)}
                elif(spawnChance >= 8 & spawnChance < 9):
                    pass
                    # spawn 2 platforms
                else:
                    # spawn 3 platforms
                    pass
            




    def render(self, surf, offset=(0,0)):
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

        
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

##        for loc in self.tilemap:
        
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1]) // self.tile_size)
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects     
