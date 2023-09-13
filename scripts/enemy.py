import pygame as pg
from pygame.math import Vector2
from .custom_group import CustomGroup
from .counter import Counter
import math

EnemyGroup = CustomGroup()


class Enemy(pg.sprite.Sprite):
    def __init__(self, pos, player, core):
        super().__init__(EnemyGroup)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.active = True
        self.maxSpeed = 1750
        self.primaray_target = player
        self.home = core
        self.image = pg.Surface((30, 30))
        self.image.fill(pg.Color("red"))
        self.display_image = self.image.copy()
        self.rect = self.image.get_rect(center=pos)

    def update(self, camPos, deltaTime, screen):
        self.active = (
            True if (self.pos - self.primaray_target.pos).length() < 2500 else False
        )
        if self.active:
            self.vel += (
                self.active
                * 1000
                * deltaTime
                * (self.primaray_target.pos - self.pos).normalize()
            )
            self.vel = min(self.vel.length(), self.maxSpeed) * self.vel.normalize()
            self.pos += self.vel * deltaTime
            self.rect.center = self.pos - camPos
        else:
            try:
                self.vel += (
                    self.active
                    * 1000
                    * deltaTime
                    * (self.home.pos - self.pos).normalize()
                )
                self.vel = min(self.vel.length(), self.maxSpeed) * self.vel.normalize()
                self.pos += self.vel * deltaTime
                self.rect.center = self.pos - camPos
            except:
                pass

        screen.blit(self.display_image, self.rect)


class Core:
    def __init__(self, player):
        self.pos = Vector2(0, 0)
        self.health = 100
        self.maxHealth = 100
        self.image = pg.transform.rotozoom(
            pg.image.load("Assets/Images/CoreV1.png").convert_alpha(), 0, 0.5
        )
        self.rect = self.image.get_rect(center=self.pos)
        self.spawn_counter = Counter(0, loopOver=True, maxValue=20)
        Enemy(Vector2(0, 0), player, self)

        self.target = player

    def update(self, camPos, deltaTime, screen):
        if self.spawn_counter.tick(deltaTime):
            Enemy(Vector2(0, 0), self.target, self)

        self.rect.center = self.pos - camPos

        for enemy in EnemyGroup:
            enemy.update(camPos, deltaTime, screen)

        screen.blit(self.image, self.rect)
