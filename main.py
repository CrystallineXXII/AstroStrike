import pygame as pg
from pygame.math import Vector2
from time import time
from scripts import classes as cl

pg.init()
screen = pg.display.set_mode((1024, 750),pg.DOUBLEBUF)
pg.display.set_caption("AstroStike")

font = pg.font.Font("Assets/Fonts/Comfortaa.ttf", 20)

def debug(string:str):
    text = font.render(string, True, "#FFFFFF", "#000000")
    screen.blit(text, (0, 0))



def game():
    clock = pg.time.Clock()
    FPS = 0

    camPos = Vector2(0, 0)
    player = cl.Player(camPos + Vector2(512, 375))

    objects = [pg.Rect(x*100-2500, y*100-2500, 5, 5) for x in range(0, 50) for y in range(0, 50)]


    prevTime = time()
    while True:
        
        clock.tick(FPS)

        deltaTime = time() - prevTime
        prevTime = time()

    #---Event-Handling--------------------------------------
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
    #-------------------------------------------------------

        camPos = player.pos - Vector2(512, 375)
        screen.fill("#000020")

    #---Drawing---------------------------------------------
       
        for obj in objects:
            pg.draw.rect(screen, "#FFFFFF", (obj.x - camPos.x, obj.y - camPos.y, obj.height, obj.width))

        player.update(deltaTime)
        player.draw(screen, camPos)

        cl.BulletGroup.update(deltaTime)
        for i in cl.BulletGroup:
            i.draw(screen, camPos)

    #-------------------------------------------------------

        debug(f"FPS: {round(clock.get_fps())} | ({camPos.x:.0f},{camPos.y:.0f}) | Vel: {player.vel.length():.0f} | {player.dir:.0f} | {player.targetDir:.0f}")
        pg.display.update()

if __name__ == "__main__":

    func = game
    params = ()

    while True:
        func,params = func(*params)