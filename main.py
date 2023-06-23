import random
from easygui import *
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import pygame, sys
from button import Button

pygame.init()

pygame.display.set_caption("Меню")

BG = pygame.image.load("image/backend.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont("Verdana", 20)

SCREEN = pygame.display.set_mode((960, 460))


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Головне меню", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(800, 240))

        PLAY_BUTTON = Button(image=pygame.image.load("image/Play Rect.png"), pos=(240, 90),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("image/Quit Rect.png"), pos=(240, 370),
                             text_input="Вихід", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    playing = True
                    FPS = pygame.time.Clock()

                    HEIGHT = 464
                    WIDTH = 960

                    FONT = pygame.font.SysFont("Verdana", 20)

                    COLOR_WHITE = (255, 255, 255)

                    main_display = pygame.display.set_mode((WIDTH, HEIGHT))

                    bg = pygame.image.load('image/background.gif')
                    bgX = 0
                    bgX2 = bg.get_width()
                    cloud_move = 1
                    IMAGE_PATH = 'ship'
                    PLAYER_IMAGES = os.listdir(IMAGE_PATH)

                    player_size = (20, 20)
                    player = pygame.image.load('image/ship.png').convert_alpha()
                    player_rect = player.get_rect()
                    player_rect.left = main_display.get_rect().left
                    player_move_down = [0, 2]
                    player_move_right = [2, 0]
                    player_move_up = [0, -2]
                    player_move_left = [-2, 0]

                    def create_enemy():
                        enemy = pygame.image.load('image/asteroids.png').convert_alpha()
                        enemy_rect = pygame.Rect(WIDTH,
                                                 random.randint(enemy.get_height(), HEIGHT - enemy.get_height()),
                                                 *enemy.get_size())
                        enemy_move = [random.randint(-6, -4), 0]
                        return [enemy, enemy_rect, enemy_move]

                    def bonuses():
                        bonus = pygame.image.load('image/bonus.png').convert_alpha()
                        bonus_width = bonus.get_width()
                        bonus_rect = pygame.Rect(random.randint(bonus_width, WIDTH - bonus_width),
                                                 -bonus.get_height(), *bonus.get_size())
                        bonus_move = [0, random.randint(1, 5)]
                        return [bonus, bonus_rect, bonus_move]

                    CREATE_ENEMY = pygame.USEREVENT + 1
                    pygame.time.set_timer(CREATE_ENEMY, 1500)
                    CREATE_BONUS = pygame.USEREVENT + 2
                    pygame.time.set_timer(CREATE_BONUS, 3000)
                    CHANGE_IMAGE = pygame.USEREVENT + 3
                    pygame.time.set_timer(CHANGE_IMAGE, 1000)

                    enemies = []
                    bonuses_colection = []

                    score = 0

                    image_index = 0

                    while playing:
                            FPS.tick(120)

                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    main_menu()
                                if event.type == CREATE_ENEMY:
                                    enemies.append(create_enemy())
                                if event.type == CREATE_BONUS:
                                    bonuses_colection.append(bonuses())
                                if event.type == CHANGE_IMAGE:
                                    player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
                                    image_index += 1
                                    if image_index >= len(PLAYER_IMAGES):
                                        image_index = 0

                            bgX -= cloud_move
                            bgX2 -= cloud_move

                            if bgX < -bg.get_width():
                                bgX = bg.get_width()

                            if bgX2 < -bg.get_width():
                                bgX2 = bg.get_width()

                            main_display.blit(bg, (bgX, 0))
                            main_display.blit(bg, (bgX2, 0))

                            keys = pygame.key.get_pressed()

                            if keys[K_DOWN] and player_rect.bottom < HEIGHT:
                                player_rect = player_rect.move(player_move_down)

                            if keys[K_RIGHT] and player_rect.right < WIDTH:
                                player_rect = player_rect.move(player_move_right)

                            if keys[K_LEFT] and player_rect.left > 0:
                                player_rect = player_rect.move(player_move_left)

                            if keys[K_UP] and player_rect.top > 0:
                                player_rect = player_rect.move(player_move_up)

                            for enemy in enemies:
                                enemy[1] = enemy[1].move(enemy[2])
                                main_display.blit(enemy[0], enemy[1])

                                if player_rect.colliderect(enemy[1]):
                                    msgbox(f'Вас знищив метеорит! \nВаш рахунок зібраних космічних зірок: {score} шт.',
                                           image="image/giphy.gif")
                                    main_menu()

                            for bonus in bonuses_colection:
                                bonus[1] = bonus[1].move(bonus[2])
                                main_display.blit(bonus[0], bonus[1])

                                if player_rect.colliderect(bonus[1]):
                                    score += 1
                                    bonuses_colection.pop(bonuses_colection.index(bonus))

                            main_display.blit(FONT.render(str(score), True, COLOR_WHITE), (WIDTH - 50, 20))
                            main_display.blit(player, player_rect)

                            pygame.display.flip()

                            for enemy in enemies:
                                if enemy[1].right < 0:
                                    enemies.pop(enemies.index(enemy))

                            for bonus in bonuses_colection:
                                if bonus[1].top > HEIGHT:
                                    bonuses_colection.pop(bonuses_colection.index(bonus))
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
pygame.display.update()
