import pygame as pg
from pygame.math import Vector2
from .custom_group import CustomGroup

EnemyGroup = CustomGroup()
class Enemy(pg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__(EnemyGroup)
        self.pos = Vector2(pos)
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self.maxSpeed = 100
        self.primarayTarget = Vector2(0,0)
        self.secondaryTarget = Vector2(0,0)