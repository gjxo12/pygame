import math
import pygame
from src import utils


class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.accelation = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        utils.blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_foward(self):
        self.vel = min(self.vel + self.accelation, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.accelation, -self.max_vel / 2)
        self.move()

    def move(self):
        # self.x += self.vel
        radian = math.radians(self.angle)
        vertical = math.cos(radian) * self.vel
        horizon = math.sin(radian) * self.vel
        self.x = self.x - horizon
        self.y = self.y - vertical

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0