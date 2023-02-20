import pygame
from entities.BaseEntity import BaseEntity


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.player = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.player = BaseEntity(0, 0, 0, 0, pygame.image.load("images/player.png"))
        self.player.x = self.width / 2 - self.player.texture.get_width() / 2
        self.player.y = self.height - self.player.texture.get_height()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False
            if event.key == pygame.K_UP:
                self.player.y_velocity = -1
            if event.key == pygame.K_DOWN:
                self.player.y_velocity = 1
            if event.key == pygame.K_LEFT:
                self.player.x_velocity = -1
            if event.key == pygame.K_RIGHT:
                self.player.x_velocity = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.player.y_velocity = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.player.x_velocity = 0

    def on_loop(self):
        self.player.update()

    def on_render(self):
        self._display_surf.fill((255, 255, 255))
        self.player.draw(self._display_surf)
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

