import pygame
import time
import math
import os
import sys
from utils import scale_image, blit_rotate_center, blit_next_center
pygame.font.init()
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

    MAIN_FONT = pygame.font.SysFont("HTK",44)

    FINISH = pygame.image.load("imgs/finish.png")
    FINISH_MASK = pygame.mask.from_surface(FINISH)
    FINISH_POSITION = (130,250)

    PATH = [(161, 180), (175, 99), (65, 101), (61, 335), (81, 502), (266, 690), (409, 685), (431, 502), (604, 556), (664, 737), (745, 585),
            (734, 408), (522, 356), (413, 267), (676, 244), (747, 119), (521, 64), (317, 77), (282, 259), (237, 407), (176, 257)]

    FPS = 60

    class Gameinfo:
        LEVELS = 10

        def __init__(self, level=1):
            self.level = level
            self.started = False
            self.level_start_time = 0

        def next_level(self):
            self.level = self.level + 1
            self.started  =False

        def reset(self):
            self.level = 1
            self.started = False
            self.level_start_time = 0

        def finish(self):
            return self.level > self.LEVELS

        def start_level(self):
            self.started = True
            self.level_start_time = time.time()

        def level_time_time(self):
            if not self.started:
                return 0
            return round(time.time() - self.level_start_time)


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

    class NPC_car(AbstractCar):
        IMG = RED_CAR
        START_POS= (150,200)

        def __init__(self,max_vel,rational_vel, path=[]):
            super().__init__(max_vel,rational_vel)
            self.path = path
            self.current_point = 0
            self.vel = max_vel

        def draw_point(self,win):
            for i in self.path:
                pygame.draw.circle(win,(255,0,0),i, 5)

        def draw(self, win):
            super().draw(win)
            self.draw_point(win)

        def caculate_angle(self):
            x,y =self.path[self.current_point]
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
                differenc_in_angle= differenc_in_angle - 360
            if differenc_in_angle > 0:
                self.angle = self.angle - min(self.rotation_vel, abs(differenc_in_angle))
            else:
                self.angle = self.angle + min(self.rotation_vel, abs(differenc_in_angle))

        def update_path_point(self):
            target = self.path[self.current_point]
            rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
            if rect.collidepoint(*target):
                self.current_point = self.current_point+1

        def move(self):
            if self.current_point >= len(self.path): return
            self.caculate_angle()
            self.update_path_point()
            super().move()

        def next_level(self, level):
            self.reset()
            self.vel = self.max_vel + (level - 1) * 0.2
            self.current_point = 0


    class PlayerCar(AbstractCar):
        IMG = RED_CAR
        START_POS= (180,200)

        def reduce_speed(self):
            self.vel = max(self.vel - self.accelation / 2, 0)
            self.move()

        def bounce(self):
            self.vel = self.vel * -1
            self.move()

    def draw(win, images,player_car, npc_car, game_info):
        for img, pos in images:
            win.blit(img,pos)
        level_text = MAIN_FONT.render(f"Level: {game_info.level}",1,(244,244,244))
        win.blit(level_text,(10,HEIGHT -level_text.get_height() - 70))

        time_text = MAIN_FONT.render(f"Time: {game_info.level_time_time()}", 1, (244, 244, 244))
        win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))

        vel_text = MAIN_FONT.render(f"Km/h: {round(player_car.vel,1)} px/s", 1, (244, 244, 244))
        win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))

        player_car.draw(WIN)
        npc_car.draw(WIN)
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

    def handle_collide(player_car,npc_car,game_info):
        if player_car.collide(TRACK_BORDER_MASK) != None:
            print(f"Crash!!!!!!!!! {player_car.x}  {player_car.y}")
            player_car.bounce()

        player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
        npc_finish_poi_collide = npc_car.collide(FINISH_MASK, *FINISH_POSITION)
        if npc_finish_poi_collide != None:
            blit_next_center(WIN,MAIN_FONT,"You Lost.....")
            pygame.display.update()
            pygame.time.wait(5000)
            game_info.reset()
            player_car.reset()
            npc_car.reset()
            print("computer win")

        if player_finish_poi_collide != None:
            if player_finish_poi_collide[1] == 0:
                player_car.bounce()
            else:
                game_info.next_level()
                player_car.reset()
                npc_car.next_level(game_info.level)
                print("Your car Win")

    run = True
    clock = pygame.time.Clock()
    images = [(GRASS,(0,0)), (TRACK, (0,0)), (FINISH,FINISH_POSITION),(TRACK_BORDER,(0,0))]
    player_car = PlayerCar(4,4)
    npc_car = NPC_car(4,4,PATH)
    game_info = Gameinfo()

    while run:
        clock.tick(FPS)
        draw(WIN, images, player_car, npc_car,game_info)

        while not game_info.started:
            blit_next_center(WIN,MAIN_FONT, f"HTK!!!!!!!!! {game_info.level}")
            pygame.display.update()
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    run = False
                    break
                if i.type == pygame.KEYDOWN:
                    game_info.start_level()

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run=False
                break

            # make point for npc car...
            # if i.type == pygame.MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()
            #     npc_car.path.append(pos)

        move_player(player_car)
        npc_car.move()
        handle_collide(player_car,npc_car,game_info)
        if game_info.finish():
            blit_next_center(WIN, MAIN_FONT, "You Lost.....")
            pygame.time.wait(5000)
            game_info.reset()
            player_car.reset()
            npc_car.reset()
            print("computer win")
        # * 가변인자 패킹!! 130 250을 인자로 넘김
        #if player_car.collide(FINISH_MASK, *FINISH_POSITION):


    print(npc_car.path)
    pygame.quit()

