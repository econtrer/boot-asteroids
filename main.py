import pygame
import sys
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from hud import Hud
from constants import *
from logger import log_state, log_event

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    # Pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    # On screen objects setup
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Hud.containers = (drawable)
    
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    player.draw_hitbox = False
    hud = Hud()
    asteroid_field = AsteroidField()

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        for d in drawable:
            d.draw(screen)
        
        updatable.update(dt)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                if not player.is_invincible():    
                    log_event("player_hit")
                    if player.lifes > 1:
                        player.lifes -= 1
                        player.respawn()
                        # TODO: This feels like we need to manage a global state.
                        # Hud class should probably have a reference to the Player object.
                        # Refactor later.
                        hud.lifes = player.lifes
                    else:
                        print("Game over!")
                        sys.exit()
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    score = asteroid.split()
                    hud.score += score
                    shot.kill()

if __name__ == "__main__":
    main()
