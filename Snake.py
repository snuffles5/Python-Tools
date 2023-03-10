import pygame
import random

# Define constants for the game window size and the size of the snake and food
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20

# Define constants for the colors used in the game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
INITIAL_SNAKE_LENGTH = 1
# Initialize Pygame and create the game window
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# Define the Snake class
class Snake:
    def __init__(self):
        self.length = INITIAL_SNAKE_LENGTH
        self.positions = [(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)]
        self.direction: tuple = (0, 0) #random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.is_started = False

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
            self.is_started = True

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x * CELL_SIZE, cur[1] + y * CELL_SIZE)
        if new in self.positions[1:] and self.is_started:
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
        return True

    def reset(self):
        self.length = INITIAL_SNAKE_LENGTH
        self.positions = [(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)]
        # Define the possible directions of movement as (x, y) tuples
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        # Choose a random direction
        self.direction = random.choice(directions)

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, WHITE, r)
            pygame.draw.rect(surface, GREEN, r, 1)

# Define the Food class
class Food:
    def __init__(self):
        x = random.randrange(CELL_SIZE, WINDOW_WIDTH - CELL_SIZE, CELL_SIZE)
        y = random.randrange(CELL_SIZE, WINDOW_HEIGHT - CELL_SIZE, CELL_SIZE)
        self.position = (x, y)
        self.color = BLUE

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)

# Define the game loop
def main():
    clock = pygame.time.Clock()
    game_over = False
    snake = Snake()
    food = Food()
    score = 0
    best_score = 0

    # Load the best score from file if it exists
    try:
        with open("best_score.txt", "r") as file:
            best_score = int(file.read())
    except FileNotFoundError:
        pass

    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                elif event.key == pygame.K_UP:
                    snake.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.turn((1, 0))

        # Move the snake
        move = snake.move()
        if not move:
            game_over = True

        # Check for collisions with the food
        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 10
            food = Food()

        # Check for collisions with the walls
        if snake.get_head_position()[0] < 0 or snake.get_head_position()[0] > WINDOW_WIDTH - CELL_SIZE:
            game_over = True
        elif snake.get_head_position()[1] < 0 or snake.get_head_position()[1] > WINDOW_HEIGHT - CELL_SIZE:
            game_over = True

        # Draw the game
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        pygame.display.set_caption(f"Snake Game | Score: {score} | Best Score: {best_score}")
        pygame.display.update()

        # Update the best score if necessary
        is_break_record = False
        if score > best_score:
            best_score = score
            is_break_record = True


        # Handle game over
        if game_over:
            # Write the best score to file
            with open("best_score.txt", "w") as file:
                file.write(str(best_score))

            # Prompt the user to play again and show the score
            score_font = pygame.font.SysFont(None, 48)
            score_text = f"Your score is {score}."
            font_score_text = score_font.render(score_text, True, WHITE)
            score_text_rect = font_score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 20))
            screen.blit(font_score_text, score_text_rect)

            motivation_font = pygame.font.SysFont(None, 40)
            motivation_text = ""
            if is_break_record:
                motivation_text = "You break the record!"
            else:
                motivation_text = "Keep trying! you gonna get it next time!"
            font_motivation_text = motivation_font.render(motivation_text, True, WHITE)
            motivation_text_rect = font_motivation_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 20))
            screen.blit(font_motivation_text, motivation_text_rect)
            
            secondary_font = pygame.font.SysFont(None, 32)
            secondary_text = "Game Over! Press R to Restart or Q to Quit"
            font_secondary_text = secondary_font.render(secondary_text, True, WHITE)
            secondary_text_rect = font_secondary_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 200))
            screen.blit(font_secondary_text, secondary_text_rect)
            
            pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            quit()
                        elif event.key == pygame.K_r:
                            main()

        speed = 20
        # Wait for 1/{speed}th of a second
        clock.tick(speed)

    # Quit Pygame and exit the program
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
