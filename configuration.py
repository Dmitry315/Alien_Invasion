import pygame
from ctypes import windll

# default settings
####################
# frames per second
fps = 60
difficulty = 1
enemy_speed = 2
# enemy spawn rate
spawn = 1700
####################
bullet_radius = 3
# add player speed
speed = 6
# window size
size = width, height = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)


# load images
PLAYER_IMAGE = pygame.image.load('images/spaceship.png')
# EARTH_IMAGE = pygame.image.load('images/Earth.png')
ENEMY_SPACESHIP_IMAGE = pygame.image.load('images/enemy_spaceship.png')
METEOR_IMAGE = pygame.image.load('images/meteor.png')
EARTH_IMAGE = pygame.image.load('images/Planet.png')

# events
ENEMY_APPEAR = 29
METEOR_APPEAR = 31
EARTH_ROTATE = 28
