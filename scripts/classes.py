import pygame as pg
from pygame.math import Vector2
from random import randint

from math import cos, sin


class Obstacle(pg.sprite.Sprite):
    def __init__(self, pos, size):
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

class Counter:
    def __init__(self, startValue,*,loopOver=False, maxValue=0):
        self.value = startValue
        self.loopOver = loopOver
        self.maxValue = maxValue

    def tick(self, deltaTime):
        self.value += deltaTime

        if self.value > self.maxValue and not self.loopOver:
            self.value = self.maxValue
            return True
        elif self.value > self.maxValue and self.loopOver:
            self.value = 0
            return True
        return False

    def reset(self):
        self.value = 0

class CustomGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()

    def update(self, deltaTime):
        for bullet in self.sprites():
            bullet.update(deltaTime)

    def draw(self, screen, camPos):
        for bullet in self.sprites():
            bullet.draw(screen, camPos)

class Player(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.targetDir = Vector2(0, -1)
        self.dir = Vector2(0, -1)
        self.display_image = pg.transform.rotozoom(pg.image.load("Assets/Images/Skylark.png"), 0, 0.5).convert_alpha()
        self.image = pg.transform.rotozoom(pg.image.load("Assets/Images/Skylark.png"), 0, 0.5).convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.speed = 5000
        self.maxAcc = 1000
        self.trailPoints = []

        self.bulletTimer = Counter(0, loopOver=True, maxValue=0.1)

        self.mask = pg.mask.from_surface(self.image)

    def update(self, deltaTime):
        self.acc = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.acc = 1
        if keys[pg.K_s]:
            self.vel -= self.vel * 0.9 * deltaTime
        if keys[pg.K_a]:
            self.targetDir = self.targetDir.rotate(deltaTime * 90)
        if keys[pg.K_d]:
            self.targetDir = self.targetDir.rotate(deltaTime * -90)
        if keys[pg.K_SPACE]:
            if self.bulletTimer.tick(deltaTime):
                Bullet(self.pos, self.vel, self.dir)


        self.vel += (Vector2(0,-1) * self.acc).rotate(self.dir.angle_to(Vector2(0,-1))) * self.maxAcc * deltaTime
        self.image = pg.transform.rotozoom(self.display_image, -self.dir.angle_to(Vector2(0,-1)),1)
        self.mask = pg.mask.from_surface(self.image)

        self.dir = self.dir.lerp(self.targetDir, 0.1)





        if self.vel.length() > self.speed:
            self.vel = self.vel.normalize() * self.speed
        if self.vel.length() < 10:
            self.vel = Vector2(0, 0)


        self.pos += self.vel * deltaTime
        self.vel -= self.vel * 0.5 * deltaTime



        self.trailPoints.append(self.pos + Vector2(26,100).rotate(self.dir.angle_to(Vector2(0,-1))))
        self.trailPoints.append(self.pos + Vector2(-24,100).rotate(self.dir.angle_to(Vector2(0,-1))))
        
        while len(self.trailPoints) > 20:
            self.trailPoints.pop(0)

    def draw(self, screen, camPos):
        for point in self.trailPoints:
            pg.draw.circle(screen, "red", (point.x - camPos.x, point.y - camPos.y), randint(3,7))
        self.rect = self.image.get_rect(center=self.pos - camPos)
        screen.blit(self.image, self.rect)

class Bullet(pg.sprite.Sprite):

    def __init__(self, posVec:Vector2, velVec:Vector2, heading:Vector2):

        super().__init__(BulletGroup)
        self.pos = Vector2(posVec)
        self.dir = heading.reflect(Vector2(0,1)).rotate(180)
        self.vel = velVec + self.dir * 1000

        self.image = pg.Surface((5, 15))
        self.image.fill("red")
        self.display_image = self.image
        self.rect = self.image.get_rect(center=posVec)

        self.lifeTime = Counter(0, maxValue=1)
        self.display_image = pg.transform.rotozoom(self.image,self.dir.angle_to(Vector2(0,-1)), 1)
        print(self.vel.length()) 

        self.mask = pg.mask.from_surface(self.display_image)

    def update(self, deltaTime):
        self.pos += self.vel * deltaTime
        self.rect.center = self.pos


        if self.lifeTime.tick(deltaTime):
            self.kill()

        
        
    def draw(self, screen, camPos):
        Mrect = self.image.get_rect(center=self.pos - camPos)
        screen.blit(self.display_image, Mrect)

        

BulletGroup = CustomGroup()
ObstacleGroup = CustomGroup()