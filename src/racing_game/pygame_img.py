import pygame
from src.racing_game.utils import scale_image
pygame.font.init()

GRASS = scale_image(pygame.image.load("../../imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("../../imgs/track.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("../../imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

RED_CAR = scale_image(pygame.image.load("../../imgs/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("../../imgs/green-car.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

MAIN_FONT = pygame.font.SysFont("HTK",44)

FINISH = pygame.image.load("../../imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130,250)

PATH = [(161, 180), (175, 99), (65, 101), (61, 335), (81, 502), (266, 690), (409, 685), (431, 502), (604, 556), (664, 737), (745, 585),
        (734, 408), (522, 356), (413, 267), (676, 244), (747, 119), (521, 64), (317, 77), (282, 259), (237, 407), (176, 257)]

FPS = 60