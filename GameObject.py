from main import *


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

    def move(self, direction):
        dir_x, dir_y = direction
        angle = calculate_angle(self.x, self.y, dir_x, dir_y)
        self.x += self.speed * np.cos(int(angle / 180 * np.pi))
