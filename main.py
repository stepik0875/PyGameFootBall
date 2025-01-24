import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

ball_speed = 5
player_speed = 5

fields = ['Травяное', 'Грунтовое', 'Мини-футбольное']
field_type = fields[0]
player1_color = RED
player2_color = BLUE

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
            if keys[pygame.K_w]: self.rect.y -= self.speed
            if keys[pygame.K_s]: self.rect.y += self.speed
            if keys[pygame.K_a]: self.rect.x -= self.speed
            if keys[pygame.K_d]: self.rect.x += self.speed
        elif self.controls == 'player2':
            if keys[pygame.K_UP]: self.rect.y -= self.speed
            if keys[pygame.K_DOWN]: self.rect.y += self.speed
            if keys[pygame.K_LEFT]: self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]: self.rect.x += self.speed

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = 0
        self.speed_y = 0
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y = -self.speed_y
        
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x

def game_loop():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2D Футбол")
    
    all_sprites = pygame.sprite.Group()
    player1 = Player(player1_color, 'player1', 50, SCREEN_HEIGHT // 2)
    player2 = Player(player2_color, 'player2', SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)
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

        if pygame.sprite.collide_rect(player1, ball):
            if ball.speed_x == 0 and ball.speed_y == 0:
                ball.speed_x = random.choice([-ball_speed, ball_speed])
                ball.speed_y = random.choice([-ball_speed, ball_speed])

        if pygame.sprite.collide_rect(player2, ball):
            if ball.speed_x == 0 and ball.speed_y == 0:
                ball.speed_x = random.choice([-ball_speed, ball_speed])
                ball.speed_y = random.choice([-ball_speed, ball_speed])

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

        screen.fill(GREEN)
        all_sprites.draw(screen)
        
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"{score1} : {score2}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
