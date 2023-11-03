import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
SNAKE_INITIAL_SPEED = 7
SNAKE_MAX_SPEED = 18
SPEED_INCREMENT = .2

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Load custom images
snake_head_img = pygame.image.load("resources/snake_head.png")
snake_body_img = pygame.image.load("resources/snake_body.png")
fruit_img = pygame.image.load("resources/fruit.png")
background_img = pygame.image.load("resources/background.png")

# Initialize the clock
clock = pygame.time.Clock()

# Initialize the Snake
snake = [(5, 5)]
snake_direction = (1, 0)
score = 0
speed = SNAKE_INITIAL_SPEED

# Initialize the Food
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Game over screen setup
font = pygame.font.Font(None, 36)
game_over_text = font.render("Game Over", True, (255, 255, 255))
retry_text = font.render("Press R to Retry", True, (255, 255, 255))
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
game_over = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Reset the game
                snake = [(5, 5)]
                snake_direction = (1, 0)
                score = 0
                speed = SNAKE_INITIAL_SPEED
                game_over = False
                food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, 1):
                    snake_direction = (0, -1)
                if event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    snake_direction = (0, 1)
                if event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    snake_direction = (-1, 0)
                if event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    snake_direction = (1, 0)

    if not game_over:
        # Move the snake
        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])

        # Check for collisions
        if new_head == food:
            score += 1
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            speed = min(SNAKE_MAX_SPEED, speed + SPEED_INCREMENT)
        else:
            snake.pop()

        if new_head in snake[1:] or new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
            game_over = True

        snake.insert(0, new_head)

        # Clear the screen
        screen.blit(background_img, (0, 0))

        # Draw the food
        screen.blit(fruit_img, (food[0] * GRID_SIZE, food[1] * GRID_SIZE))

        # Draw the snake
        for i, segment in enumerate(snake):
            if i == 0:
                # Draw the snake head
                screen.blit(snake_head_img, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
            else:
                # Draw the snake body
                screen.blit(snake_body_img, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))

        # Display the score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
    else:
        # Display game over screen
        screen.blit(game_over_text, game_over_rect)
        screen.blit(retry_text, retry_rect)

    # Update the display
    pygame.display.update()

    # Control game speed
    clock.tick(speed)
