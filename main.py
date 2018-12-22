import pygame
import numpy as np
from units import *
from GameObject import *
from ctypes import *

# init game
pygame.init()
pygame.mouse.set_pos(0, 0)
# add game constants
SPEED = 6
PLAYER_IMAGE = pygame.image.load('spaceship.png')
EARTH_IMAGE = pygame.image.load('Earth.png')
FPS = 100
# FPS
clock = pygame.time.Clock()
# window size
size = width, height = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)
# FULLSCREEN
windows = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
windows.fill((0, 0, 0))


# function to calculate angle:
# for moving and rotating
def calculate_angle(x1, y1, centrx, centry):
    delta_x, delta_y = centrx - x1, centry - y1
    angle = 360 - np.degrees(np.arctan2(delta_y, delta_x))
    return angle


if __name__ == '__main__':
    # init hero
    hero = Hero((500, 500), SPEED, PLAYER_IMAGE)
    # init Earth
    Earth_cords = (width // 2 - 50, height // 2 - 50)
    Earth = Earth(Earth_cords, EARTH_IMAGE)
    earth_hit_box = Earth.hit_box(100, 95)

    run = True
    # first level cycle
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # get pressed keys
        keys = pygame.key.get_pressed()
        # close game on esc
        if keys[pygame.K_ESCAPE]:
            run = False
        # move hero with WASD
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
        # init hero hit box
        hero_hit_box = pygame.Rect(hero.x, hero.y, 80, 80)
        # check collision
        if hero.hit_box(80, 80).colliderect(earth_hit_box):
            run = False
            print('collided')
        # depict objects
        Earth.draw_object()
        # hero follow mouse
        hero.draw_object(pygame.mouse.get_pos())
        pygame.display.update()

    pygame.quit()
