import pygame
from ctypes import windll

BULLET_RADIUS = 3
# add player speed
SPEED = 6
# window size
size = width, height = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)

# load images
PLAYER_IMAGE = pygame.image.load('images/spaceship.png')
EARTH_IMAGE = pygame.image.load('images/Earth.png')
ENEMY_SPACESHIP_IMAGE = pygame.image.load('images/enemy_spaceship.png')
METEOR_IMAGE = pygame.image.load('images/meteor.png')
# EARTH_IMAGE = pygame.image.load('images/Planet.png')

# events
ENEMY_APPEAR = 29
METEOR_APPEAR = 31
# EARTH_ROTATE = 28
