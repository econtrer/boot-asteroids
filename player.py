import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.draw_hitbox = False
        self.shoot_cd_timer = 0
        self.respawn_invincibility_timer = 0
        self.lifes = PLAYER_MAX_LIFES
        self.is_blinking = False
  
    def is_invincible(self):
        return self.respawn_invincibility_timer > 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        if self.is_blinking and (self.respawn_invincibility_timer % 0.2) > 0.1: # ~100 ms visible, ~100 ms invisible
            return
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
        if self.draw_hitbox:
            pygame.draw.circle(screen, "red", self.position, PLAYER_RADIUS, LINE_WIDTH)
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Rotation
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        
        # Forward / backward
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)

        # Shoot
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        if self.shoot_cd_timer > 0:
            self.shoot_cd_timer -= dt
        
        if self.respawn_invincibility_timer > 0:
            self.respawn_invincibility_timer -= dt
        else:
            self.is_blinking = False
    
    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.shoot_cd_timer > 0:
            return

        shot = Shot(self.position.x, self.position.y)
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SHOOT_SPEED
        shot.velocity = rotated_with_speed_vector

        self.shoot_cd_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

    def respawn(self):
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.respawn_invincibility_timer = PLAYER_RESPAWN_INVINCIBILITY_SECONDS
        self.is_blinking = True
