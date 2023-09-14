import pygame as pg
from pygame.math import Vector2
from .counter import Counter
from .enemy import Enemy, EnemyGroup
from random import randint


class Core:
    def __init__(self, player):
        self.pos = Vector2(0, 0)
        self.health = 100
        self.maxHealth = 100
        self.base_image = pg.transform.rotozoom(
            pg.image.load("Assets/Images/cBase.png").convert_alpha(), 0, 0.5
        )
        self.turret_image = pg.transform.rotozoom(
            pg.image.load("Assets/Images/cTurret.png").convert_alpha(), 0, 0.5
        )
        self.turret_display_image = self.turret_image.copy()
        self.rect = self.base_image.get_rect(center=self.pos)
        self.spawn_counter = Counter(0, loopOver=True, maxValue=20)

        self.target = player
        self.turret_angle = 0
        Enemy(Vector2(10000, 0).rotate(randint(0, 360)), self.target, self)

    def update(self, camPos, deltaTime, screen):
        if self.spawn_counter.tick(deltaTime):
            Enemy(Vector2(10000, 0).rotate(randint(0, 360)), self.target, self)

        self.rect.center = self.pos - camPos

        for enemy in EnemyGroup:
            enemy.update(camPos, deltaTime, screen)

        screen.blit(self.base_image, self.rect)

        closest_enemy = None
        for enemy in EnemyGroup:
            if not closest_enemy:
                closest_enemy = enemy
            elif (enemy.pos - self.pos).length() < (
                closest_enemy.pos - self.pos
            ).length():
                closest_enemy = enemy

        if closest_enemy:
            tangle = -Vector2(0, -1).angle_to(closest_enemy.pos)

        else:
            tangle = self.turret_angle
        self.turret_angle += (tangle - self.turret_angle) * 10 * deltaTime
        self.turret_display_image = pg.transform.rotate(
            self.turret_image, self.turret_angle
        )

        if 10 < (length := (closest_enemy.pos - self.pos).length()) < 1000:
            pg.draw.line(
                screen,
                "#48ffc8",
                self.pos - camPos,
                self.pos - camPos + Vector2(0, -length).rotate(-self.turret_angle),
                5,
            )

        screen.blit(
            self.turret_display_image,
            self.turret_display_image.get_rect(center=self.pos - camPos),
        )

