from abstract_car import AbstractCar
from src import pygame_img


class PlayerCar(AbstractCar):
    IMG = pygame_img.RED_CAR
    START_POS = (180, 200)

    def reduce_speed(self):
        self.vel = max(self.vel - self.accelation / 2, 0)
        self.move()

    def bounce(self):
        self.vel = self.vel * -1
        self.move()