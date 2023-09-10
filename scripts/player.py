import pygame as pg
from pygame.math import Vector2
from .bullet import Bullet
from .counter import Counter




class Player(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.targetDir = Vector2(0, -1)
        self.dir = Vector2(0, -1)
        self.display_image = pg.transform.rotozoom(pg.image.load("Assets/Images/Shrike.png"), 0, 0.5).convert_alpha()
        self.image = self.display_image.copy()
        self.rect = self.image.get_rect()
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.speed = 5000
        self.maxAcc = 1000
        self.trailPoints = []
        self.trail_counter = Counter(0, maxValue=0.01, loopOver=True)

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

        if self.pos.length() < 9850:
            self.vel += (Vector2(0,-1) * self.acc).rotate(self.dir.angle_to(Vector2(0,-1))) * self.maxAcc * deltaTime
            self.image = pg.transform.rotozoom(self.display_image, -self.dir.angle_to(Vector2(0,-1)),1)
            self.mask = pg.mask.from_surface(self.image)

            try:
                self.dir = self.dir.lerp(self.targetDir, 5 * deltaTime)
            except:
                pass
        else:
            self.vel = self.vel.reflect(self.pos.normalize())
            self.pos = self.pos.normalize() * 9850




        if self.vel.length() > self.speed:
            self.vel = self.vel.normalize() * self.speed
        if self.vel.length() < 10:
            self.vel = Vector2(0, 0)


        self.pos += self.vel * deltaTime
        self.vel -= self.vel * 0.5 * deltaTime



        if self.trail_counter.tick(deltaTime):
            self.trailPoints.append([
                self.pos + Vector2(  0,80).rotate(self.dir.angle_to(Vector2(0,-1))),
                self.pos + Vector2( 10,80).rotate(self.dir.angle_to(Vector2(0,-1))),
                self.pos + Vector2(-10,80).rotate(self.dir.angle_to(Vector2(0,-1))),
                self.pos + Vector2(-59,50).rotate(self.dir.angle_to(Vector2(0,-1))),
                self.pos + Vector2( 59,50).rotate(self.dir.angle_to(Vector2(0,-1))),
            ])
        
        while len(self.trailPoints) > 10:
            self.trailPoints.pop(0)

    def draw(self, screen, camPos):
        if len(self.trailPoints) > 1:
            pg.draw.lines(screen, "#0edddd", False, [a[0] - camPos for a in self.trailPoints], 2)
            pg.draw.lines(screen, "#0edddd", False, [b[1] - camPos for b in self.trailPoints], 2)
            pg.draw.lines(screen, "#0edddd", False, [c[2] - camPos for c in self.trailPoints], 2)
            pg.draw.lines(screen, "#0edddd", False, [d[3] - camPos for d in self.trailPoints], 2)
            pg.draw.lines(screen, "#0edddd", False, [e[4] - camPos for e in self.trailPoints], 2)


        self.rect = self.image.get_rect(center=self.pos - camPos)
        
        screen.blit(self.image, self.rect)