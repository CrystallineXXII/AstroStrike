import pygame as pg
from pygame.math import Vector2
from .custom_group import CustomGroup

EnemyGroup = CustomGroup()

def dotted(screen, color, start, end):
    distance = (end - start).length()
    direction = (end - start).normalize()
    for i in range(0, int(distance / 10)):
        pg.draw.circle(
            screen,
            color,
            start + direction * i * 10,
            2,
        )

class Enemy(pg.sprite.Sprite):
    def __init__(self, pos, player, core):
        super().__init__(EnemyGroup)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.active = True
        self.maxSpeed = 1750
        self.primaray_target = player
        self.secondary_target = core
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
                1000
                * deltaTime
                * (self.primaray_target.pos - self.pos).normalize()
            )
            self.vel = min(self.vel.length(), self.maxSpeed) * self.vel.normalize()
            self.pos += self.vel * deltaTime
            self.vel -= self.vel * 0.5 * deltaTime
            self.rect.center = self.pos - camPos

            dotted(
                screen,
                "#f62525",
                self.pos - camPos,
                self.secondary_target.pos - camPos,
            )

        else:
            try:
                self.vel += (
                    1000
                    * deltaTime
                    * (self.secondary_target.pos - self.pos).normalize()
                )
                self.vel = min(self.vel.length(), self.maxSpeed) * self.vel.normalize()
                self.pos += self.vel * deltaTime
                self.vel -= self.vel * 0.5 * deltaTime
                self.rect.center = self.pos - camPos

                dotted(
                    screen,
                    "#797979",
                    self.pos - camPos,
                    self.secondary_target.pos - camPos,
                )
            except Exception as e:
                print(e)

        screen.blit(self.display_image, self.rect)

