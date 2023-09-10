import pygame as pg
from pygame.math import Vector2

import math

def draw_vel_gizmo(screen, camPos, player):
    pg.draw.arc(
        screen,
        "#25c9f6",
        pg.Rect(player.pos - camPos - Vector2(150, 150), Vector2(300, 300)),
        math.radians(player.vel.angle_to(Vector2(1, 0)) - 10),
        math.radians(player.vel.angle_to(Vector2(1, 0)) + 10),
    )
    pg.draw.circle(
        screen,
        "#25c9f6",
        player.pos
        - camPos
        + Vector2(0, 150).rotate(-player.vel.angle_to(Vector2(0,1))),
        3,
    )

def draw_gizmos(screen, camPos, player):
    pg.draw.circle(screen, "#333333", player.pos - camPos, 150, 1)
    if player.vel.length() > 0:
        draw_vel_gizmo(screen, camPos, player)

