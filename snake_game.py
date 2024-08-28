import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the display
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
black = pygame.Color(0, 0, 139)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# Clock
clock = pygame.time.Clock()

# Snake
snake_block = 10
snake_speed = 15

# Food
foodx = 0  # Initialize foodx and foody globally
foody = 0

# Score
score_font = pygame.font.SysFont("comicsansms", 35)


# Game Over
def game_over():
    global snake_list, snake_length, foodx, foody  # Declare them as global

    game_over_font = pygame.font.SysFont("comicsansms", 22)
    game_over_surface = game_over_font.render("Game Over! Press Q to quit, any other key to play again.", True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width / 2, height / 4)
    screen.blit(game_over_surface, game_over_rect)
    show_score(0, red, "comicsansms", 20)
    pygame.display.flip()

    waiting_for_keypress = True
    while waiting_for_keypress:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Quit if 'q' is pressed
                    pygame.quit()
                    sys.exit()
                else:  # Any other key restarts the game
                    waiting_for_keypress = False
                    snake_list = []
                    snake_length = 1
                    # Update the global foodx and foody
                    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
                    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
                    game_loop()


# Show Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score : " + str(snake_length - 1), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (width / 10, 15)
    else:
        score_rect.midtop = (width / 2, height / 1.25)
    screen.blit(score_surface, score_rect)


# Game Loop
def game_loop():
    global snake_list, snake_length, foodx, foody

    game_over_flag = False
    game_close = False

    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []  # Initialize snake_list at the beginning of each game
    snake_length = 1

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0  # Initialize food position at the beginning of each game
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over_flag:
        while game_close:
            game_over()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_flag = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(black)
        pygame.draw.rect(screen, red, [foodx, foody, snake_block, snake_block])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        for x in snake_list:
            pygame.draw.rect(screen, green, [x[0], x[1], snake_block, snake_block])

        show_score(1, white, "comicsansms", 20)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


game_loop()  # Start the game initially