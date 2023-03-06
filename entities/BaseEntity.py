import pygame


class BaseEntity:
    def __init__(self, x, y, x_velocity, y_velocity, texture, angle):
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.texture = texture
        self.angle = angle

    def update(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def draw(self, screen):
        screen.blit(pygame.transform.rotate(self.texture, self.angle), (self.x, self.y))