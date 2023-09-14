import pygame as pg

class CustomGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()

    def update(self, deltaTime):
        for bullet in self.sprites():
            bullet.update(deltaTime)

    def draw(self, screen, camPos):
        for bullet in self.sprites():
            bullet.draw(screen, camPos)
