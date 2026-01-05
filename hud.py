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
        self.draw_lifes(screen)
    
    def draw_score(self, screen):
        screen.blit(
            self.__font.render(f"Score: {self.score}", True, "white"),
            (10, 10)
        )

    def draw_lifes(self, screen):
        screen.blit(
            self.__font.render("Lives: ", True, "white"),
            (10, 50)
        )
        for i in range(self.lifes):
            self.draw_ship(screen, 80 + i * 30, 65)
    
    def draw_ship(self, screen, x, y):
        points = [
            (x, y - PLAYER_RADIUS),
            (x - PLAYER_RADIUS / 2, y + PLAYER_RADIUS / 2),
            (x + PLAYER_RADIUS / 2, y + PLAYER_RADIUS / 2),
        ]
        # TODO: This should be a call to a Player method, since it should draw the ship shape
        pygame.draw.polygon(screen, "red", points, LINE_WIDTH)