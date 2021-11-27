from src.racing_game.pygame_img import *
from src.racing_game.utils import *

def draw(win, images, player_car, npc_car, game_info):
    for img, pos in images:
        win.blit(img, pos)
    level_text = MAIN_FONT.render(f"Level: {game_info.level}", 1, (244, 244, 244))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))

    time_text = MAIN_FONT.render(f"Time: {game_info.level_time_time()}", 1, (244, 244, 244))
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))

    vel_text = MAIN_FONT.render(f"Km/h: {round(player_car.vel, 1)} px/s", 1, (244, 244, 244))
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


def handle_collide(player_car, npc_car, game_info):
    if player_car.collide(TRACK_BORDER_MASK) != None:
        print(f"Crash!!!!!!!!! {player_car.x}  {player_car.y}")
        player_car.bounce()

    player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    npc_finish_poi_collide = npc_car.collide(FINISH_MASK, *FINISH_POSITION)
    if npc_finish_poi_collide != None:
        blit_next_center(WIN, MAIN_FONT, "You Lost.....")
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