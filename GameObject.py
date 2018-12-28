from main import calculate_angle, width, height
import pygame
from numpy import sin, cos, pi


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
        self.x += self.speed * cos(angle / 180 * pi)
        self.y += self.speed * sin(angle / 180 * pi)
        self.x = int(self.x)
        self.y = int(self.y)

    # return hit boxes of objects
    # for checking collision
    def hit_box(self, sizex, sizey):
        return pygame.Rect(self.x + 10, self.y, sizex - 10, sizey)


# other rigid objects (Earth, meteorites)
class NeutralObject(GameObject):
    def __init__(self, cords, speed, image):
        super().__init__(cords, 0, image)
        self.x = cords[0]
        self.y = cords[1]
        self.speed = speed
        self.image = image

    # there is no need in rotation
    def draw_object(self, windows):
        windows.blit(self.image, (self.x, self.y))


class Earth(NeutralObject):
    def __init__(self, cords, image):
        super().__init__(cords, 0, image)
        self.x = cords[0]
        self.y = cords[1]
        self.image = image

    # Earth doesn't move in this game
    def move(self):
        pass


class Bullet(NeutralObject):
    def __init__(self, cords, mouse_cord):
        self.x = cords[0]
        self.y = cords[1]
        self.speed = 10
        angle = 360 - calculate_angle(self.x, self.y, mouse_cord[0], mouse_cord[1])
        self.speed_x = self.speed * cos(angle / 180 * pi)
        self.speed_y = self.speed * sin(angle / 180 * pi)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.x = int(self.x)
        self.y = int(self.y)
        if self.x > width or self.y > height or self.x < 0 or self.y < 0:
            return True
        return False

    def draw_object(self, windows):
        pygame.draw.circle(windows, (255, 0, 0), (int(self.x), int(self.y)), 3, 0)
