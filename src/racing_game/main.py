import os
import sys
import logging
from src.racing_game.npc_car import *
from src.racing_game.player_car import *
from src.racing_game.play import *
from src.racing_game.gameinfo import *
from src.racing_game.pygame_img import *
from src.racing_game.utils import blit_next_center
import pygame
# Press the green button in the gutter to run the script.

log = logging.getLogger(__name__)
# log.setLevel(logging.INFO)

logging.basicConfig(filename="test.log",
                    filemode='a',
                    format='%(asctime)s,%(module)s %(filename)s %(funcName)s %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
log.info("Running")

if __name__ == '__main__':
    try:
        os.chdir(sys._MEIPASS)
       #log.info(f"{sys._MEIPASS} , {os.chdir(sys._MEIPASS)}")
    except:
        os.chdir(os.getcwd())
        #log.info(f"{os.chdir(os.getcwd())}")

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

