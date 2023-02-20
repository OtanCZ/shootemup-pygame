from entities.BaseEntity import BaseEntity


class ProjectileEntity(BaseEntity):
    def __init__(self, x, y, x_velocity, y_velocity, texture, damage):
        super().__init__(x, y, x_velocity, y_velocity, texture)
        self.damage = damage
