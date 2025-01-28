import pygame
import random
import math


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


player_colors = [
    (255, 0, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
    (0, 255, 255),
    (255, 192, 203),
]


player_color_names = [
    "Красный",
    "Синий",
    "Желтый",
    "Оранжевый",
    "Фиолетовый",
    "Голубой",
    "Розовый"
]


fields = ['Травяное', 'Грунтовое', 'Мини-футбольное']


ball_speed = 5
player_speed = 5


class Player(pygame.sprite.Sprite):
    def __init__(self, color, controls, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.controls = controls
        self.speed = player_speed

    def update(self):
        keys = pygame.key.get_pressed()

        if self.controls == 'player1':
            if keys[pygame.K_w] and self.rect.top > 0:
                self.rect.y -= self.speed
            if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:
                self.rect.y += self.speed
            if keys[pygame.K_a] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
                self.rect.x += self.speed
        elif self.controls == 'player2':
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
                self.rect.y += self.speed
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
                self.rect.x += self.speed


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = 0
        self.speed_y = 0
        self.angle = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y = -self.speed_y

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x

    def bounce(self, player):

        if self.rect.colliderect(player.rect):
            ball_center = self.rect.center
            player_center = player.rect.center

            angle = math.atan2(
                ball_center[1] - player_center[1], ball_center[0] - player_center[0])
            self.angle = angle

            self.speed_x = ball_speed * math.cos(self.angle)
            self.speed_y = ball_speed * math.sin(self.angle)

            speed_multiplier = 1.2
            self.speed_x *= speed_multiplier
            self.speed_y *= speed_multiplier


def main_menu():
    font = pygame.font.Font(None, 36)

    menu_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Выберите параметры игры")

    sel_pol = 0
    selected_color1 = player_colors[0]
    selected_color2 = player_colors[1]
    selected_color1_n = player_color_names[0]
    selected_color2_n = player_color_names[1]
    selected_goals = 5

    running = True
    while running:
        menu_screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    sel_pol = (sel_pol - 1) % len(fields)
                elif event.key == pygame.K_DOWN:
                    sel_pol = (sel_pol + 1) % len(fields)
                elif event.key == pygame.K_RIGHT:


                    selected_color1_ind = player_color_names.index(
                        selected_color1_n)
                    selected_color1_ind = (
                        selected_color1_ind + 1) % len(player_color_names)
                    selected_color1_n = player_color_names[selected_color1_ind]
                    selected_color1 = player_colors[selected_color1_ind]
                elif event.key == pygame.K_LEFT:

                    selected_color1_ind = player_color_names.index(
                        selected_color1_n)
                    selected_color1_ind = (
                        selected_color1_ind - 1) % len(player_color_names)
                    selected_color1_n = player_color_names[selected_color1_ind]
                    selected_color1 = player_colors[selected_color1_ind]
                elif event.key == pygame.K_SPACE:

                    selected_color2_ind = player_color_names.index(
                        selected_color2_n)
                    selected_color2_ind = (
                        selected_color2_ind + 1) % len(player_color_names)
                    selected_color2_n = player_color_names[selected_color2_ind]
                    selected_color2 = player_colors[selected_color2_ind]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    selected_goals += 1
                    if selected_goals > 10:
                        selected_goals = 1

        field_text = font.render(
            f"Поле: {fields[sel_pol]}", True, WHITE)
        color_text1 = font.render(
            f"Цвет игрока 1: {selected_color1_n}", True, WHITE)
        color_text2 = font.render(
            f"Цвет игрока 2: {selected_color2_n}", True, WHITE)
        goals_text = font.render(
            f"Голов до победы: {selected_goals}", True, WHITE)
        start_text = font.render("Нажмите Enter для начала игры", True, WHITE)

        menu_screen.blit(field_text, (SCREEN_WIDTH // 2 -
                         field_text.get_width() // 2, 150))
        menu_screen.blit(color_text1, (SCREEN_WIDTH // 2 -
                         color_text1.get_width() // 2, 200))
        menu_screen.blit(color_text2, (SCREEN_WIDTH // 2 -
                         color_text2.get_width() // 2, 250))
        menu_screen.blit(goals_text, (SCREEN_WIDTH // 2 -
                         goals_text.get_width() // 2, 300))
        menu_screen.blit(start_text, (SCREEN_WIDTH // 2 -
                         start_text.get_width() // 2, 400))

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return fields[sel_pol], selected_color1, selected_color2, selected_goals

    pygame.quit()


def game_over_menu(score1, score2):
    font = pygame.font.Font(None, 36)

    menu_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Конец игры")

    result_text = f"Игра завершена! Счет: {score1} : {score2}"
    restart_text = "Нажмите Enter для перезапуска"

    running = True
    while running:
        menu_screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True

        result_render = font.render(result_text, True, WHITE)
        restart_render = font.render(restart_text, True, WHITE)

        menu_screen.blit(result_render, (SCREEN_WIDTH // 2 -
                         result_render.get_width() // 2, SCREEN_HEIGHT // 3))
        menu_screen.blit(restart_render, (SCREEN_WIDTH // 2 -
                         restart_render.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    pygame.quit()


def game_loop(field_type, player1_color, player2_color, max_goals):

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2D Футбол")


    all_sprites = pygame.sprite.Group()
    player1 = Player(player1_color, 'player1', 50, SCREEN_HEIGHT // 2)
    player2 = Player(player2_color, 'player2',
                     SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)
    ball = Ball()

    all_sprites.add(player1, player2, ball)

    clock = pygame.time.Clock()
    score1 = 0
    score2 = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        ball.bounce(player1)
        ball.bounce(player2)

        if ball.rect.left <= 0:
            score2 += 1
            ball.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball.speed_x = 0
            ball.speed_y = 0
        if ball.rect.right >= SCREEN_WIDTH:
            score1 += 1
            ball.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball.speed_x = 0
            ball.speed_y = 0

        if score1 >= max_goals or score2 >= max_goals:
            running = False

        screen.fill((0, 100, 0))

        pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

        pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, 0),
                         (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)

        goal_width = 100
        goal_depth = 20
        pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT //
                         2 - goal_width // 2, goal_depth, goal_width))
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - goal_depth,
                         SCREEN_HEIGHT // 2 - goal_width // 2, goal_depth, goal_width))

        all_sprites.draw(screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Счет: {score1} : {score2}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 -
                    score_text.get_width() // 2, 10))

        pygame.display.flip()

        clock.tick(FPS)

    if game_over_menu(score1, score2):
        game_loop(field_type, player1_color, player2_color, max_goals)

    pygame.quit()


field, color1, color2, goals = main_menu()
game_loop(field, color1, color2, goals)
