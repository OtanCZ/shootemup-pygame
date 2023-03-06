from threading import Timer

import pygame

from entities.BaseEntity import BaseEntity


class DestructibleEntity(BaseEntity):
    def __init__(self, x, y, x_velocity, y_velocity, texture, angle, health, max_health, invincibility_ms):
        super().__init__(x, y, x_velocity, y_velocity, texture, angle)
        self.hurting = False
        self.health = health
        self.max_health = max_health
        self.invincibility_ms = invincibility_ms

    def hurt(self, damage):
        if not self.hurting:
            self.health -= damage
            self.hurting = True
            redTimer = Timer(self.invincibility_ms, self.deactivateInvincibility)
            redTimer.start()

    def deactivateInvincibility(self):
        self.hurting = False

    def playerdraw(self, screen):
        if self.x > screen.get_width() - self.texture.get_width():
            self.x = screen.get_width() - self.texture.get_width()
        if self.x < 0:
            self.x = 0
        if self.y > screen.get_height() - self.texture.get_height():
            self.y = screen.get_height() - self.texture.get_height()
        if self.y < 0:
            self.y = 0

        self.draw(screen)

    def draw(self, screen):
        if self.hurting:
            hurt_texture = self.texture.copy()
            hurt_texture.fill((125, 0, 0), None, special_flags=pygame.BLEND_RGB_ADD)
            screen.blit(pygame.transform.rotate(hurt_texture, self.angle), (self.x, self.y))
        else:
            screen.blit(pygame.transform.rotate(self.texture, self.angle), (self.x, self.y))
