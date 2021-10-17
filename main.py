import pygame
import time
import math
import os
import sys
from utils import scale_image, blit_rotate_center

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    try:
        os.chdir(sys._MEIPASS)
        print(f"{sys._MEIPASS}   {os.chdir(sys._MEIPASS)}" )
    except:
        os.chdir(os.getcwd())
        print(f"{os.chdir(os.getcwd())}")

    GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
    TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)

    TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
    TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

    RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
    GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)

    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racing Game!")

    FINISH = pygame.image.load("imgs/finish.png")
    FINISH_MASK = pygame.mask.from_surface(FINISH)
    FINISH_POSITION = (130,250)

    FPS = 60

    class AbstractCar:
        def __init__(self,max_vel,rotation_vel):
            self.img = self.IMG
            self.max_vel = max_vel
            self.vel = 0
            self.rotation_vel = rotation_vel
            self.angle = 0
            self.x ,self.y = self.START_POS
            self.accelation = 0.1

        def rotate(self, left=False, right = False):
            if left:
                self.angle += self.rotation_vel
            elif right:
                self.angle -= self.rotation_vel

        def draw(self, win):
            blit_rotate_center(win, self.img,(self.x,self.y),self.angle)

        def move_foward(self):
            self.vel = min(self.vel + self.accelation,self.max_vel)
            self.move()

        def move_backward(self):
            self.vel = max(self.vel - self.accelation,  -self.max_vel / 2)
            self.move()

        def move(self):
            #self.x += self.vel
            radian = math.radians(self.angle)
            vertical = math.cos(radian) * self.vel
            horizon = math.sin(radian) * self.vel
            self.x = self.x - horizon
            self.y = self.y - vertical

        def collide(self, mask, x=0, y=0):
            car_mask = pygame.mask.from_surface(self.img)
            offset = (int(self.x - x),int(self.y - y))
            poi = mask.overlap(car_mask, offset)
            return poi

        def reset(self):
            self.x, self.y = self.START_POS
            self.angle=0
            self.vel = 0


    class PlayerCar(AbstractCar):
        IMG = RED_CAR
        START_POS= (180,200)

        def reduce_speed(self):
            self.vel = max(self.vel - self.accelation / 2, 0)
            self.move()

        def bounce(self):
            self.vel = self.vel * -1
            self.move()

    def draw(win, images,player_car):
        for img, pos in images:
            win.blit(img,pos)
        player_car.draw(WIN)
        pygame.display.update()

    def move_player(player_car):
        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_a]:
            player_car.rotate(left=True)
        if keys[pygame.K_d]:
            player_car.rotate(right=True)
        if keys[pygame.K_w]:
            moved = True
            player_car.move_foward()
        if keys[pygame.K_s]:
            moved = True
            player_car.move_backward()
        if not moved:
            player_car.reduce_speed()

    run = True
    clock = pygame.time.Clock()
    images = [(GRASS,(0,0)), (TRACK, (0,0)), (FINISH,FINISH_POSITION),(TRACK_BORDER,(0,0))]
    player_car = PlayerCar(4,4)

    while run:
        clock.tick(FPS)
        draw(WIN, images, player_car)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run=False
                break
        move_player(player_car)
        if player_car.collide(TRACK_BORDER_MASK) != None:
            print(f"Crash!!!!!!!!! {player_car.x}  {player_car.y}")
            player_car.bounce()

        # * 가변인자 패킹!! 130 250을 인자로 넘김
        #if player_car.collide(FINISH_MASK, *FINISH_POSITION):



    pygame.quit()

