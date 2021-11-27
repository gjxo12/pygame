from abstract_car import AbstractCar
from src.racing_game import pygame_img
import pygame
import math

class NPC_car(AbstractCar):
    IMG = pygame_img.RED_CAR
    START_POS = (150, 200)

    def __init__(self, max_vel, rational_vel, path=[]):
        super().__init__(max_vel, rational_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_point(self, win):
        for i in self.path:
            pygame.draw.circle(win, (255, 0, 0), i, 5)

    def draw(self, win):
        super().draw(win)
        self.draw_point(win)

    def caculate_angle(self):
        x, y = self.path[self.current_point]
        x_diff = x - self.x
        y_diff = y - self.y
        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)
        if y > self.y:
            desired_radian_angle = desired_radian_angle + math.pi

        differenc_in_angle = self.angle - math.degrees(desired_radian_angle)
        if differenc_in_angle >= 180:
            differenc_in_angle = differenc_in_angle - 360
        if differenc_in_angle > 0:
            self.angle = self.angle - min(self.rotation_vel, abs(differenc_in_angle))
        else:
            self.angle = self.angle + min(self.rotation_vel, abs(differenc_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point = self.current_point + 1

    def move(self):
        if self.current_point >= len(self.path): return
        self.caculate_angle()
        self.update_path_point()
        super().move()

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0