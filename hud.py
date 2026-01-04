import pygame
from constants import *

class Hud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.score = 0
        self.lifes = PLAYER_MAX_LIFES
        self.__font = pygame.font.SysFont("Verdana", 20)
    
    def draw(self, screen):
        self.draw_score(screen)
    
    def draw_score(self, screen):
        screen.blit(
            self.__font.render(f"Score: {self.score}", True, "white"),
            (10, 10)
        )
