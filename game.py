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
                'bricks': load_images('tiles/bricks'),
                'player': load_image('entities/player.png'),
                'background': load_image('background.png'),
                'menuBackground': load_image('backgroundMenu.png'),
                'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
                'player/run' : Animation(load_images('entities/player/run'), img_dur=4),
                'player/jump': Animation(load_images('entities/player/jump')),
                'player/slide': Animation(load_images('entities/player/slide')),
                'player/wall_slide': Animation(load_images('entities/player/wall_slide'))
            }
        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)

        self.scroll = [0, 0]

        # score
        self.score = 0
        self.scoreFont = pygame.font.Font('freesansbold.ttf', 10)
        self.menu = pygame.font.Font('freesansbold.ttf', 24)
        self.title = pygame.font.Font('futur.ttf', 32)
        self.hi_score = 0
        
        self.game_state = 0

    def run(self): # switches between menu and playing, resets important vars before playing
        while True:
            if self.game_state == 0: # menu
                self.player = Player(self, (50, 50), (8, 15))
                self.tilemap = Tilemap(self, tile_size=16)
                self.scroll = [0, 0]
                self.score = 0
                self.mainMenu()
            elif self.game_state == 1: # game
                
                self.play()
        
    def play(self):
        while self.game_state == 1:
            self.display.blit(self.assets['background'], (0,0))

            scroll_inc = 30
            player_y = self.player.rect().centery # only allows scrolling down
            if player_y < self.scroll[1] + self.display.get_height() / 4: # only updates camera height moving up if the player height is 1/4 of the the display height
                self.scroll[1] = player_y - self.display.get_height() / 4
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            if self.player.rect().centery > self.scroll[1] + self.display.get_height(): # if they move below the bottom of the screen, change game state
                self.game_state = 0

            self.score = max(-player_y // 10, self.score) # update score in the corner
            self.hi_score = max(self.score , self.hi_score) # update high score

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


            self.text = self.scoreFont.render('Score: ' + str(self.score), True, (255, 255, 255))
            self.textRect = self.text.get_rect()
            self.textRect.topleft = (10, 10)  # Position of the score box

            self.display.blit(self.text, self.textRect)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

    def mainMenu(self):
        while self.game_state == 0:
            self.display.blit(self.assets['menuBackground'], (0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # start
                        self.game_state = 1

            self.text = self.menu.render('Press Enter to Start\n     High Score: ' + str(self.hi_score), True, (255, 255, 255))
            self.textRect = self.text.get_rect()
            self.textRect.topleft = (50, 150)  # text position

            self.text2 = self.title.render('Moon Jumper', True, (227, 197, 245))
            self.textRect2 = self.text2.get_rect()
            self.textRect2.topleft = (50, 75)  # text position
            self.display.blit(self.text2, self.textRect2)
            # add text to display 
            self.display.blit(self.text, self.textRect)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()