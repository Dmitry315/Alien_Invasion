import pygame
from ctypes import windll

with open('game_settings.txt', encoding='utf-8', mode='r') as f:
    lines = f.readlines()
    FPS = int(lines[0].split()[1])
    diff = int(lines[1].split()[1])
    if diff > 3:
        DIFFICULTY = 3
    elif diff < 0:
        DIFFICULTY = 0
    else:
        DIFFICULTY = diff

# window size
size = width, height = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)

# add player speed
SPEED = 4 * 90 / FPS

# load images
PLAYER_IMAGE = pygame.image.load('images/spaceship.png')
EARTH_IMAGE = pygame.image.load('images/Earth.png')
ENEMY_SPACESHIP = pygame.image.load('images/enemy_spaceship.png')


# events
ENEMY_APPEAR = 30

# enemy speed
ENEMY_SPEED = 3 if DIFFICULTY == 3 else 2

# Bullet radius
BULLET_RADIUS = 4 if DIFFICULTY <= 1 else 3

# enemy spawn rate
# if DIFFICULTY == 0 enemies won't spawn
if DIFFICULTY != 0:
    SPAWN = 2000 - DIFFICULTY * 300
