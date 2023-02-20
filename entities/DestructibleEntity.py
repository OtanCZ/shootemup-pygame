from entities.BaseEntity import BaseEntity


class DestructibleEntity(BaseEntity):
    def __init__(self, x, y, x_velocity, y_velocity, texture, health, max_health):
        super().__init__(x, y, x_velocity, y_velocity, texture)
        self.health = health
        self.max_health = max_health