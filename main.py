import pygame as pg
from pygame.math import Vector2

pg.init()
screen = pg.display.set_mode((1024, 750))
pg.display.set_caption("AstroStike")
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    screen.fill("#000000")

    pg.display.update()