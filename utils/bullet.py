import pygame as pg
from pygame.math import Vector2
from .counter import Counter
from .custom_group import CustomGroup

BulletGroup = CustomGroup()

class Bullet(pg.sprite.Sprite):

    def __init__(self, posVec:Vector2, velVec:Vector2, heading:Vector2,*,player_owned:bool = True):

        super().__init__(BulletGroup)
        self.pos = Vector2(posVec)
        self.dir = heading.reflect(Vector2(0,1)).rotate(180)
        self.vel = velVec + self.dir * 1000

        self.image = pg.Surface((5, 15))
        self.image.fill("#48ffc8")
        self.display_image = self.image
        self.rect = self.image.get_rect(center=posVec)

        self.lifeTime = Counter(0, maxValue=1)
        self.display_image = pg.transform.rotozoom(self.image,self.dir.angle_to(Vector2(0,-1)), 1)
        self.player_owned = player_owned


        self.mask = pg.mask.from_surface(self.display_image)

    def update(self, deltaTime):
        self.pos += self.vel * deltaTime
        self.rect.center = self.pos


        if self.lifeTime.tick(deltaTime):
            self.kill()

        
        
    def draw(self, screen, camPos):
        Mrect = self.image.get_rect(center=self.pos - camPos)
        screen.blit(self.display_image, Mrect)

        