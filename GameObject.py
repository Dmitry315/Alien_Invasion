from main import *


# Abstract class of all objects in game
class GameObject:
    def __init__(self, cords, speed, image):
        self.x = cords[0]
        self.y = cords[1]
        self.speed = speed
        self.image = image

    def draw_object(self, direction):
        dir_x, dir_y = direction
        angle = calculate_angle(self.x, self.y, dir_x, dir_y) - 90
        rotated_image = pygame.transform.rotate(self.image, angle)
        windows.blit(rotated_image, (self.x, self.y))

    # move object in direction
    # calculates with angle function in main.py
    def move(self, direction):
        dir_x, dir_y = direction
        angle = calculate_angle(self.x, self.y, dir_x, dir_y)
        self.x += self.speed * np.cos(int(angle / 180 * np.pi))

    # return hit boxes of objects
    # for checking collision
    def hit_box(self, sizex, sizey):
        return pygame.Rect(self.x, self.y, sizex, sizey)


# other rigid objects (Earth, meteorites)
class NeutralObject(GameObject):
    def __init__(self, cords, speed, image):
        super().__init__(cords, 0, image)
        self.x = cords[0]
        self.y = cords[1]
        self.speed = speed
        self.image = image

    # there is no need in rotation
    def draw_object(self):
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
