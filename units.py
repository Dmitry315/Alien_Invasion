from main import *
from GameObject import *


class Hero(GameObject):
    def __init__(self, cords, speed, image):
        super().__init__(cords, speed, image)
        self.x = cords[0]
        self.y = cords[1]
        self.speed = speed
        self.image = image

    def move(self, xy):
        self.x += xy[0]
        self.y += xy[1]
