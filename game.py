# Pygame Project
# Nicolas Lunt
# ProgLang
# 3/7/24

# Game.py

import pygame
import sys

from scripts.entities import PhysicsEntity, Player
from scripts.utilities import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Midterm')

        scr_res = (640, 480)
        self.screen = pygame.display.set_mode(scr_res)

        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
                'decor': load_images('tiles/decor'),
                'grass': load_images('tiles/grass'),
                'large_decor': load_images('tiles/large_decor'),
                'stone': load_images('tiles/stone'),
                'player': load_image('entities/player.png'),
                'background': load_image('background.png'),
                'clouds': load_images('clouds'),
                'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
                'player/run' : Animation(load_images('entities/player/run'), img_dur=4),
                'player/jump': Animation(load_images('entities/player/jump')),
                'player/slide': Animation(load_images('entities/player/slide')),
                'player/wall_slide': Animation(load_images('entities/player/wall_slide'))
            }
        print(self.assets)

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)

        self.scroll = [0, 0]

        self.platforms = [[175, 480, 70, 10]]
        # score
        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 10)
        
    def run(self):
        while True:
            #print(self.tilemap.physics_rects_around(self.player.pos))
            #self.screen.fill((255, 255, 255))
            self.display.blit(self.assets['background'], (0,0))

            scroll_inc = 30
            player_y = self.player.rect().centery # only allows scrolling down
            if player_y < self.scroll[1] + self.display.get_height() / 4:
                self.scroll[1] = player_y - self.display.get_height() / 4
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            if self.player.rect().centery > self.scroll[1] + self.display.get_height():
                pygame.quit()
                sys.exit()

            self.score = max(-player_y // 10, self.score)

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False                
            
            # constant jumping
            if(self.player.velocity[1] == 0):
                self.player.velocity[1] = -4
            
            for i in range(len(self.platforms)):
                block = pygame.draw.rect(self.screen, (0,0,0), self.platforms[i])

            self.text = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
            self.textRect = self.text.get_rect()
            self.textRect.topleft = (10, 10)  # Position of the score box

            # Draw score text onto the display surface
            self.display.blit(self.text, self.textRect)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)
        
Game().run()