from GameObject import GameObject


# Hero class
class Hero(GameObject):
    def __init__(self, cords, speed, image):
        super().__init__(cords, speed, image)
        self.x = cords[0]
        self.y = cords[1]
        self.speed = speed
        self.image = image

    # move hero
    def move(self, xy):
        self.x += xy[0]
        self.y += xy[1]


class SpaceEnemy(GameObject):
    def __init__(self, cords, speed, image, direction):
        super().__init__(cords, speed, image)
        self.x = cords[0]
        self.y = cords[1]
        self.speed = speed
        self.image = image
        # it is better to give enemies direction in init
        self.direction = direction

    # there is no need to give direction in function
    # all enemies fly in Earth direction
    def move(self):
        super().move(self.direction)

    def draw_object(self):
        super().draw_object(self.direction)
