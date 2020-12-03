import pygame
import random

pygame.init()

# Window settings
display_width = 1280
display_height = 720
display = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Pong')

FPS = 60
clock = pygame.time.Clock()

# Define game Objects
ball = pygame.Rect(display_width // 2 - 15, display_height // 2 - 15, 30, 30)
player = pygame.Rect(display_width - 20, display_height // 2 - 70, 10, 140)
player_ai = pygame.Rect(10, display_height // 2 - 70, 10, 140)

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Game settings
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
player_ai_speed = 7

# Text and Font
player_score = 0
player_ai_score = 0

game_font = pygame.font.Font(None, 100)


def ball_animation():
    global ball_speed_x, ball_speed_y,\
        player_score, player_ai_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= display_height:
        ball_speed_y = -ball_speed_y

    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= display_width:
        player_ai_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1

    if ball.colliderect(player_ai) and ball_speed_x < 0:
        if abs(ball.left - player_ai.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player_ai.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player_ai.bottom) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1


def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (display_width // 2, display_height // 2)

    if current_time - score_time < 1000:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= display_height:
        player.bottom = display_height


def player_ai_animation():
    if player_ai.top < ball.y:
        player_ai.top += player_ai_speed
    if player_ai.bottom > ball.y:
        player_ai.bottom -= player_ai_speed
    if player_ai.top <= 0:
        player_ai.top = 0
    if player_ai.bottom >= display_height:
        player_ai.bottom = display_height


# Timer
score_time = True


def run_game():
    global player_speed
    game = True
    while game:
        # Events in game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_speed += 7
                if event.key == pygame.K_UP:
                    player_speed -= 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_speed -= 7
                if event.key == pygame.K_UP:
                    player_speed += 7

        # Game animation
        ball_animation()
        player_animation()
        player_ai_animation()

        # Draw game objects
        display.fill(black)
        pygame.draw.rect(display, white, player)
        pygame.draw.rect(display, white, player_ai)
        pygame.draw.ellipse(display, white, ball)
        pygame.draw.aaline(display, white, (640, 0), (640, 720))

        # Ball start after 1-2 second
        if score_time:
            ball_restart()

        # Draw Player and AI score (Text)
        p_text = game_font.render(f"{player_score}", False, white)
        display.blit(p_text, (display_width - 320, display_height // 20))

        p_ai_text = game_font.render(f"{player_ai_score}", False, white)
        display.blit(p_ai_text, (320, display_height // 20))

        # Window update
        pygame.display.update()
        clock.tick(FPS)


run_game()
