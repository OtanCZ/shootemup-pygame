import math
from random import random
from threading import Timer

import pygame
from entities.BaseEntity import BaseEntity
from entities.DestructibleEntity import DestructibleEntity
from entities.ProjectileEntity import ProjectileEntity


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 600, 400
        self.projectiles = []
        self.enemies = []
        self.player = None
        self.score = 0
        self.difficulty = 3
        self.enemySpawnerTimer = Timer(self.difficulty, self.spawnEnemy)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.player = DestructibleEntity(0, 0, 0, 0, pygame.image.load("resources/images/player.png"), 0, 3, 3, 0.5)
        self.player.x = self.width / 2 - self.player.texture.get_width() / 2
        self.player.y = self.height - self.player.texture.get_height()
        self.enemySpawnerTimer.start()
        pygame.mixer.music.load("resources/sounds/Numb.mid")
        pygame.mixer.music.play(-1)
    def spawnEnemy(self):
        tankiness = random()*5
        self.enemies.append(DestructibleEntity(random()*(self.width-32), -16, 0, 0.16-0.025*tankiness, pygame.image.load("resources/images/player.png"), 180, tankiness, tankiness, 0.1))

        self.enemySpawnerTimer = Timer(self.difficulty, self.spawnEnemy)
        self.enemySpawnerTimer.start()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False
            if event.key == pygame.K_UP:
                self.player.y_velocity = -0.4
            if event.key == pygame.K_DOWN:
                self.player.y_velocity = 0.4
            if event.key == pygame.K_LEFT:
                self.player.x_velocity = -0.4
            if event.key == pygame.K_RIGHT:
                self.player.x_velocity = 0.4
            if event.key == pygame.K_SPACE:
                self.projectiles.append(ProjectileEntity(self.player.x + self.player.texture.get_width() / 2, self.player.y, 0, -1, pygame.image.load("resources/images/bullet.png").convert_alpha(), 0, 1))
                pygame.mixer.Sound.play(pygame.mixer.Sound("resources/sounds/laserShoot.wav"))


            if event.key == pygame.K_BACKSPACE:
                self.enemies.append(DestructibleEntity(self.player.x + self.player.texture.get_width() / 2, self.player.y, 0, 0, pygame.image.load("resources/images/player.png").convert_alpha(), 0, 3, 3, 0.5))
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.player.y_velocity = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.player.x_velocity = 0

    def on_loop(self):
        self.difficulty = 3 - round(pygame.time.get_ticks() / 250000, 3)
        self.player.update()
        for projectile in self.projectiles:
            projectile.update()

        for enemy in self.enemies:
            enemy.update()
            if enemy.y > self.height:
                self.enemies.remove(enemy)
                self.player.hurt(1)

            if self.player.x < enemy.x < self.player.x + self.player.texture.get_width() and self.player.y < enemy.y < self.player.y + self.player.texture.get_height():
                self.player.hurt(1)
                enemy.hurt(1)
                pygame.mixer.Sound.play(pygame.mixer.Sound("resources/sounds/hitHurt.wav"))

            for projectile in self.projectiles:
                if enemy.x < projectile.x < enemy.x + enemy.texture.get_width() and enemy.y < projectile.y < enemy.y + enemy.texture.get_height():
                    enemy.hurt(projectile.damage)
                    pygame.mixer.Sound.play(pygame.mixer.Sound("resources/sounds/hitHurt.wav"))
                    self.projectiles.remove(projectile)

            if enemy.health <= 0:
                self.enemies.remove(enemy)
                pygame.mixer.Sound.play(pygame.mixer.Sound("resources/sounds/explosion.wav"))
                self.score = self.score + 1

            if self.player.health <= 0:
                pygame.mixer.Sound.play(pygame.mixer.Sound("resources/sounds/explosion.wav"))
                self._running = False

        for projectile in self.projectiles:
            if projectile.y < 0 or projectile.y > self.height or projectile.x < 0 or projectile.x > self.width:
                self.projectiles.remove(projectile)

    def on_render(self):
        self._display_surf.fill((255, 255, 255))
        self.player.playerdraw(self._display_surf)
        for projectile in self.projectiles:
            projectile.draw(self._display_surf)
        for enemy in self.enemies:
            enemy.draw(self._display_surf)

        font = pygame.font.SysFont("monospace", 18)
        text = font.render('Score: ' + str(self.score) + " | Health: " + str(self.player.health) + " | Difficulty: " + str(self.difficulty), True, 'black')
        textRect = text.get_rect()
        textRect.center = (self.width/2, self.height-9)
        self._display_surf.blit(text, textRect)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()

