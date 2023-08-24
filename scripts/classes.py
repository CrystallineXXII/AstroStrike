import pygame as pg
from pygame.math import Vector2
from random import randint

BulletGroup = pg.sprite.Group()

class Counter:
    def __init__(self, startValue,*,loopOver=False, maxValue=0):
        self.value = startValue
        self.loopOver = loopOver
        self.maxValue = maxValue

    def tick(self, deltaTime):
        self.value += deltaTime if self.loopOver else 0
        if self.value > self.maxValue and not self.loopOver:
            self.value = self.maxValue
        elif self.value > self.maxValue and self.loopOver:
            self.value = 0
            return True
        return False

    def reset(self):
        self.value = 0


class Player(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.targetDir = 0
        self.dir = 0
        self.display_image = pg.transform.rotozoom(pg.image.load("Assets/Images/Skylark.png"), 0, 0.5).convert_alpha()
        self.image = pg.transform.rotozoom(pg.image.load("Assets/Images/Skylark.png"), 0, 0.5).convert_alpha()
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.speed = 5000
        self.maxAcc = 1000
        self.trailPoints = []

        self.bulletTimer = Counter(0, loopOver=True, maxValue=0.1)

    def update(self, deltaTime):
        self.acc = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.acc = 1
        if keys[pg.K_s]:
            self.vel -= self.vel * 0.9 * deltaTime
        if keys[pg.K_a]:
            self.targetDir -= deltaTime * 90
        if keys[pg.K_d]:
            self.targetDir += deltaTime * 90
        if keys[pg.K_SPACE]:
            if self.bulletTimer.tick(deltaTime):
                Bullet(self.pos, self.dir, self.vel.length() + 200)


        self.vel += (Vector2(0,-1) * self.acc).rotate(self.dir) * self.maxAcc * deltaTime
        self.image = pg.transform.rotozoom(self.display_image, -self.dir,1)

        self.dir += (self.targetDir - self.dir) * deltaTime * 7

        if self.targetDir > 360:
            self.targetDir -= 360
            self.dir -= 360
        if self.targetDir < 0:
            self.targetDir += 360
            self.dir += 360



        if self.vel.length() > self.speed:
            self.vel = self.vel.normalize() * self.speed
        if self.vel.length() < 10:
            self.vel = Vector2(0, 0)


        self.pos += self.vel * deltaTime
        self.vel -= self.vel * 0.5 * deltaTime



        self.trailPoints.append(self.pos + Vector2(26,100).rotate(self.dir))
        self.trailPoints.append(self.pos + Vector2(-24,100).rotate(self.dir))
        
        while len(self.trailPoints) > 20:
            self.trailPoints.pop(0)

    def draw(self, screen, camPos):
        Mrect = self.image.get_rect(center=self.pos - camPos)
        screen.blit(self.image, Mrect)
        for point in self.trailPoints:
            pg.draw.circle(screen, "red", (point.x - camPos.x, point.y - camPos.y), randint(3,7))

class Bullet(pg.sprite.Sprite):

    def __init__(self, pos, dir, speed):
        super().__init__(BulletGroup)
        self.image = pg.Surface((5, 5))
        self.image.fill("red")
        self.display_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.dir = dir
        self.speed = speed
        self.vel = Vector2(0, 0)


    def update(self, deltaTime):
        self.vel = Vector2(0, -1).rotate(self.dir) * self.speed
        self.pos += self.vel * deltaTime
        self.rect.center = self.pos
        self.display_image = pg.transform.rotozoom(self.image, -self.dir, 1)

        
        
    def draw(self, screen, camPos):
        Mrect = self.image.get_rect(center=self.pos - camPos)
        screen.blit(self.display_image, Mrect)