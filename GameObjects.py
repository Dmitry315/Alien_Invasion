from configuration import *
import numpy as np


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
class GameObject:
    def __init__(self, cords, speed, image):
        self.x = cords[0]
        self.y = cords[1]
        self.speed = speed
        self.image = image

    def draw_object(self, windows, direction):
        dir_x, dir_y = direction
        angle = calculate_angle(self.x, self.y, dir_x, dir_y) - 90
        rotated_image = pygame.transform.rotate(self.image, angle)
        windows.blit(rotated_image, (self.x, self.y))

    # move object in direction
    # calculates with angle function in main.py
    def move(self, direction):
        dir_x, dir_y = direction
        angle = 360 - calculate_angle(self.x, self.y, dir_x, dir_y)
        self.x += self.speed * np.cos(angle / 180 * np.pi)
        self.y += self.speed * np.sin(angle / 180 * np.pi)
        self.x = int(self.x)
        self.y = int(self.y)

    # return hit boxes of objects
    # for checking collision
    def hit_box(self, sizex, sizey):
        return pygame.Rect(self.x + 10, self.y, sizex - 10, sizey)


# other rigid objects (Earth, meteorites)
class NeutralObject(GameObject):
    def __init__(self, cords, speed, image):
        super().__init__(cords, speed, image)

    # there is no need in rotation
    def draw_object(self, windows):
        windows.blit(self.image, (self.x, self.y))


class Earth(NeutralObject):
    def __init__(self, cords, image):
        super().__init__(cords, 0, image)

    # Earth doesn't move in this game
    def move(self):
        pass


class Bullet(NeutralObject):
    def __init__(self, cords, mouse_cord):
        self.x = cords[0]
        self.y = cords[1]
        self.speed = 12
        angle = 360 - calculate_angle(self.x, self.y, mouse_cord[0], mouse_cord[1])
        self.speed_x = self.speed * np.cos(angle / 180 * np.pi)
        self.speed_y = self.speed * np.sin(angle / 180 * np.pi)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.x = int(self.x)
        self.y = int(self.y)
        if self.x > width or self.y > height or self.x < 0 or self.y < 0:
            return True
        return False

    def draw_object(self, windows):
        pygame.draw.circle(windows, (255, 0, 0), (int(self.x), int(self.y)), BULLET_RADIUS, 0)

    def hit_box(self):
        return pygame.Rect(self.x + 10, self.y, BULLET_RADIUS * 2, BULLET_RADIUS * 2)


# Hero class
class Hero(GameObject):
    def __init__(self, cords, speed, image):
        super().__init__(cords, speed, image)

    # move hero
    def move(self, xy):
        self.x += xy[0]
        self.y += xy[1]

    def hit_box(self):
        return super().hit_box(80, 80)

    def gravitation(self, earth):
        r = np.sqrt(np.power((self.x - earth[0]), 2) + np.power((self.y - earth[1]), 2))
        grav_speed = 500 / r
        dir_x, dir_y = earth
        angle = 360 - calculate_angle(self.x, self.y, dir_x, dir_y)
        self.x += grav_speed * np.cos(angle / 180 * np.pi)
        self.y += grav_speed * np.sin(angle / 180 * np.pi)
        self.x = int(self.x)
        self.y = int(self.y)


class SpaceEnemy(GameObject):
    def __init__(self, cords, speed, image, direction):
        super().__init__(cords, speed, image)
        # it is better to give enemies direction in init
        self.direction = direction

    # there is no need to give direction in function
    # all enemies fly in Earth direction
    def move(self):
        super().move(self.direction)

    def draw_object(self, windows):
        super().draw_object(windows, self.direction)

    def hit_box(self):
        return super().hit_box(55, 41)
