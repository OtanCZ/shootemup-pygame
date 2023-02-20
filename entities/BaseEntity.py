import pygame


class BaseEntity:
    def __init__(self, x, y, x_velocity, y_velocity, texture):
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.texture = texture
        self.angle = 0

    def update(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def draw(self, screen):
        if(self.x > screen.get_width() - self.texture.get_width()):
            self.x = screen.get_width() - self.texture.get_width()
        if(self.x < 0):
            self.x = 0
        if(self.y > screen.get_height() - self.texture.get_height()):
            self.y = screen.get_height() - self.texture.get_height()
        if(self.y < 0):
            self.y = 0

        screen.blit(pygame.transform.rotate(self.texture, self.angle), (self.x, self.y))

