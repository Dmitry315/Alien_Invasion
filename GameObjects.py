from configuration import *
import numpy as np
from random import choice
from time import sleep


# function to calculate angle:
# for moving and rotating
def calculate_angle(x1, y1, centrx, centry):
    delta_x, delta_y = centrx - x1, centry - y1
    angle = 360 - np.degrees(np.arctan2(delta_y, delta_x))
    return angle


def print_text(windows, text, font):
    text = font.render(text, 1, (255, 255, 255))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_y += text_y // 2
    windows.fill((0, 0, 0))
    windows.blit(text, (text_x, text_y))


# Abstract class of all objects in game
class GameObject(pygame.sprite.Sprite):
    def __init__(self, cords, speed1, image):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed1
        self.loaded_image = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = cords[0]
        self.rect.y = cords[1]
        self.mask = pygame.mask.from_surface(self.image)

    def draw_object(self, windows, direction):
        dir_x, dir_y = direction
        angle = calculate_angle(self.rect.x, self.rect.y, dir_x, dir_y) - 90
        self.image = pygame.transform.rotate(self.loaded_image, angle)
        old_cords = self.rect.x, self.rect.y
        self.rect = self.image.get_rect()
        windows.blit(self.image, old_cords)
        self.rect.x, self.rect.y = old_cords

    # move object in direction
    # calculates with angle function in main.py
    def move(self, direction):
        dir_x, dir_y = direction
        angle = 360 - calculate_angle(self.rect.x, self.rect.y, dir_x, dir_y)
        self.rect.x += self.speed * np.cos(angle / 180 * np.pi)
        self.rect.y += self.speed * np.sin(angle / 180 * np.pi)
        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)


# other rigid objects (Earth, meteors)
class NeutralObject(GameObject):
    def __init__(self, cords, speed1, image):
        super().__init__(cords, speed1, image)

    # there is no need in rotation
    def draw_object(self, windows):
        windows.blit(self.image, (self.rect.x, self.rect.y))


class Earth(NeutralObject):
    def __init__(self, cords, image):
        super().__init__(cords, 0, image)

    # Earth doesn't move in this game
    def move(self):
        pass


# appears with hard difficylty
class Meteor(NeutralObject):
    def __init__(self, cords, image):
        super().__init__(cords, choice([2, 3, 4]), image)

    # direction: from top to bottom
    def move(self):
        self.rect.y += self.speed


class Bullet(pygame.sprite.Sprite):
    def __init__(self, cords, mouse_cord):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 12
        angle = 360 - calculate_angle(cords[0], cords[1], mouse_cord[0], mouse_cord[1])
        self.speed_x = self.speed * np.cos(angle / 180 * np.pi)
        self.speed_y = self.speed * np.sin(angle / 180 * np.pi)
        self.image = pygame.Surface((2 * bullet_radius, 2 * bullet_radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, (255, 0, 0), (bullet_radius, bullet_radius), bullet_radius)
        self.rect = pygame.Rect(cords[0], cords[1], 2 * bullet_radius, 2 * bullet_radius)
        self.rect.x = cords[0]
        self.rect.y = cords[1]
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)
        if self.rect.x > width or self.rect.y > height \
                or self.rect.x < 0 or self.rect.y < 0:
            return True
        return False

    def draw_object(self, windows):
        windows.blit(self.image, (self.rect.x, self.rect.y))


# Hero class
class Hero(GameObject):
    def __init__(self, cords, speed1, image):
        super().__init__(cords, speed1, image)
        self.cords = cords

    # move hero
    def move(self, xy):
        self.rect.x += xy[0]
        self.rect.y += xy[1]

    def gravitation(self, earth):
        r = np.sqrt(np.power((self.rect.x - earth[0]), 2)
                    + np.power((self.rect.y - earth[1]), 2))
        grav_speed = 500 / r + 0.75
        dir_x, dir_y = earth
        angle = 360 - calculate_angle(self.rect.x, self.rect.y, dir_x, dir_y)
        self.rect.x += grav_speed * np.cos(angle / 180 * np.pi)
        self.rect.y += grav_speed * np.sin(angle / 180 * np.pi)


class SpaceEnemy(GameObject):
    def __init__(self, cords, speed1, image, direction):
        super().__init__(cords, speed1, image)
        # it is better to give enemies direction in init
        self.direction = direction

    # there is no need to give direction in function
    # all enemies fly in Earth direction
    def move(self):
        super().move(self.direction)

    def draw_object(self, windows):
        super().draw_object(windows, self.direction)


class Particle(pygame.sprite.Sprite):
    colors = [(255, 0, 0), (255, 255, 0), (255, 165, 0)]

    def __init__(self, group, cords, dx, dy):
        super().__init__(group)
        self.image = pygame.Surface((3, 3), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, choice(Particle.colors), (0, 0, 3, 3), 2)
        self.rect = self.image.get_rect()
        self.rect.x = cords[0]
        self.rect.y = cords[1]
        self.velocity = [dx, dy]
        self.start_point = cords

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        r = np.sqrt(np.power((self.rect.x - self.start_point[0]), 2)
                    + np.power((self.rect.y - self.start_point[1]), 2))
        if r > 35:
            self.kill()

