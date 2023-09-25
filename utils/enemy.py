import pygame as pg
from pygame.math import Vector2
from .custom_group import CustomGroup
from .counter import Counter
from .bullet import Bullet


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
        self.primary_target = player
        self.secondary_target = core
        self.image = pg.transform.rotozoom(pg.image.load("Assets/Images/Reaver.png").convert_alpha(),0,0.5)
        self.display_image = self.image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.current_direction = Vector2(0,0)
        self.target_direction = Vector2(0, 0)

        self.bulletTimer = Counter(0, loopOver=True, maxValue=0.1)

        self.trail_points = []

    def update(self, camPos, deltaTime, screen):
        self.active = (
            True if (self.pos - self.primary_target.pos).length() < 2500 else False
        )
        if self.active:
            self.vel += (
                1000
                * deltaTime
                * self.current_direction
            )
            self.vel = min(self.vel.length(), self.maxSpeed) * self.vel.normalize()
            self.pos += self.vel * deltaTime
            self.vel -= self.vel * 0.5 * deltaTime
            self.rect.center = self.pos - camPos

            # dotted(
            #     screen,
            #     "#f62525",
            #     self.pos - camPos,
            #     self.secondary_target.pos - camPos,
            # )

        else:
            try:
                self.vel += (
                    1000
                    * deltaTime
                    * self.current_direction
                )
                self.vel = min(self.vel.length(), self.maxSpeed) * self.vel.normalize()
                self.pos += self.vel * deltaTime
                self.vel -= self.vel * 0.5 * deltaTime
                self.rect.center = self.pos - camPos

                # dotted(
                #     screen,
                #     "#797979",
                #     self.pos - camPos,
                #     self.secondary_target.pos - camPos,
                # )
            except Exception as e:
                print(e)

        target = (
            self.primary_target
            if self.active
            else self.secondary_target
        )
        self.target_direction = (target.pos - self.pos).normalize()

        self.trail_points.append([
            self.pos + Vector2(0, 10).rotate(self.current_direction.angle_to(Vector2(0,-1))),
            self.pos + Vector2(-10, 10).rotate(self.current_direction.angle_to(Vector2(0,-1))),
            self.pos + Vector2(10, 10).rotate(self.current_direction.angle_to(Vector2(0,-1))),
        ])

        self.trail_points = self.trail_points[-20:]

        if len(self.trail_points) > 1:
            pg.draw.lines(
                screen,
                "#EC663B",
                False,
                [point[0] - camPos for point in self.trail_points],
                2,
            )
            pg.draw.lines(
                screen,
                "#EC663B",
                False,
                [point[1] - camPos for point in self.trail_points],
                2,
            )
            pg.draw.lines(
                screen,
                "#EC663B",
                False,
                [point[2] - camPos for point in self.trail_points],
                2,
            )
        if (self.pos - target.pos).magnitude() < 1000:
            if self.bulletTimer.tick(deltaTime):
                Bullet(self.pos, self.vel, self.current_direction.reflect(Vector2(0,1)).rotate(180), player_owned=False)


        self.current_direction =  self.current_direction.lerp(self.target_direction, min((5 * deltaTime,1)))
        
        self.display_image = pg.transform.rotozoom(
            self.image, self.current_direction.angle_to(Vector2(0,-1)), 1
        )
        self.rect = self.display_image.get_rect(center=self.pos - camPos)

        screen.blit(self.display_image, self.rect)

