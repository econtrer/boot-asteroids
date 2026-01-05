import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # must override
        pass

    def update(self, dt):
        # must override
        pass

    def collides_with(self, other):
        return (self.position.distance_to(other.position) <= (self.radius + other.radius))

    def wrap(self):
        """Wrap the sprite around the screen when it moves outside the visible area.

        This uses the sprite's radius so objects fully leave before appearing on the opposite
        side, creating a seamless wrap effect. Log a "wrap" event for visibility when a
        wrap happens (useful for smoke tests and debugging).
        """
        wrapped_x = False
        wrapped_y = False

        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
            wrapped_x = True
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
            wrapped_x = True

        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
            wrapped_y = True
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
            wrapped_y = True

        if wrapped_x or wrapped_y:
            # Import here to avoid potential import cycles and to keep top-level imports minimal
            from logger import log_event

            log_event(
                "wrap",
                obj=self.__class__.__name__,
                x=round(self.position.x, 2),
                y=round(self.position.y, 2),
                wrapped_x=wrapped_x,
                wrapped_y=wrapped_y,
            )
