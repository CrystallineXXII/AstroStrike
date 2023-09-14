from random import randint
import pygame as pg
from pygame.math import Vector2
from .custom_group import CustomGroup

ObstacleGroup = CustomGroup()

class Obstacle(pg.sprite.Sprite):
    def __init__(self, pos, size, ObstacleGroup):
        super().__init__(ObstacleGroup)
        self.pos = Vector2(pos)
        self.size = size

        self.image = pg.image.load("Assets/Images/Obstacle.png").convert_alpha()
        self.image = pg.transform.rotozoom(self.image,randint(-90,90),self.size)
        self.rect = self.image.get_rect(center=pos)

        self.mask = pg.mask.from_surface(self.image)

    def draw(self, screen, camPos):
        Mrect = self.image.get_rect(center=self.pos - camPos)
        screen.blit(self.image, Mrect)

