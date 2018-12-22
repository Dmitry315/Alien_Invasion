import pygame
import numpy as np
import os
from GameObject import *
from units import *

pygame.init()
pygame.mouse.set_pos(500, 500)
size = width, height = 1000, 1000
SPEED = 6
PLAYER_IMAGE = pygame.image.load('spaceship.png')
clock = pygame.time.Clock()

windows = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
windows.fill((0, 0, 0))


def calculate_angle(x1, y1, centrx, centry):
    delta_x, delta_y = centrx - x1, centry - y1
    angle = 360 - np.degrees(np.arctan2(delta_y, delta_x))
    return angle


if __name__ == '__main__':
    hero = Hero((500, 500), SPEED, PLAYER_IMAGE)
    run = True
    while run:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        x = 0
        y = 0
        if keys[pygame.K_w]:
            y -= SPEED
        if keys[pygame.K_a]:
            x -= SPEED
        if keys[pygame.K_s]:
            y += SPEED
        if keys[pygame.K_d]:
            x += SPEED
        windows.fill((0, 0, 0))
        hero.move((x, y))
        hero.draw_object(pygame.mouse.get_pos())
        pygame.display.update()
    pygame.quit()
