import pygame
import numpy
import os

pygame.init()
pygame.mouse.set_pos(500, 500)

size = width, height = 1000, 1000
speed = 6
x, y = 500, 500
player = pygame.image.load('spaceship.png')
clock = pygame.time.Clock()

windows = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
windows.fill((0, 0, 0))


def calculate_angle(x1, y1, centrx, centry):
    delta_x, delta_y = centrx - x1, centry - y1
    angle = 360 - numpy.degrees(numpy.arctan2(delta_y, delta_x))
    return angle


def draw_hero():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    angle = calculate_angle(x, y, mouse_x, mouse_y)
    rotated_image = pygame.transform.rotate(player, angle - 90)
    windows.blit(rotated_image, (x, y))


run = True
while run:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    if keys[pygame.K_w]:
        y -= speed
    if keys[pygame.K_a]:
        x -= speed
    if keys[pygame.K_s]:
        y += speed
    if keys[pygame.K_d]:
        x += speed
    windows.fill((0, 0, 0))
    draw_hero()
    pygame.display.update()
pygame.quit()
