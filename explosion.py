import pygame
import random
from constants import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, particle_count=None, radius_scale=1.0):
        # attach to containers if provided by main
        pygame.sprite.Sprite.__init__(self, getattr(self, "containers", ()))

        if particle_count is None:
            particle_count = EXPLOSION_PARTICLE_COUNT

        self.particles = []
        for _ in range(particle_count):
            angle = random.uniform(0, 360)
            speed = random.uniform(EXPLOSION_PARTICLE_SPEED * 0.5, EXPLOSION_PARTICLE_SPEED) * radius_scale
            vel = pygame.Vector2(0, 1).rotate(angle) * speed
            life = random.uniform(EXPLOSION_LIFETIME_SECONDS * 0.7, EXPLOSION_LIFETIME_SECONDS * 1.3)
            size = random.uniform(1, EXPLOSION_PARTICLE_RADIUS * radius_scale)
            self.particles.append({
                "pos": pygame.Vector2(x, y),
                "vel": vel,
                "life": life,
                "max_life": life,
                "size": size,
            })

    def update(self, dt):
        alive = []
        for p in self.particles:
            p["life"] -= dt
            if p["life"] > 0:
                # simple friction so particles slow down slightly
                p["vel"] *= 0.98
                p["pos"] += p["vel"] * dt
                alive.append(p)
        self.particles = alive
        if not self.particles:
            self.kill()

    def draw(self, screen):
        for p in self.particles:
            t = max(0.0, min(1.0, p["life"] / p["max_life"]))
            # color fades from yellow (1.0 -> (255,200,0)) to red/dark (0.0 -> (100,30,0))
            r = int(255 * (0.6 + 0.4 * t))
            g = int(200 * t)
            b = int(0 * t)
            color = (r, g, b)
            pygame.draw.circle(screen, color, p["pos"], int(p["size"]))
