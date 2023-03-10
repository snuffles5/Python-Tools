import pygame
import random
import math

# Define constants for the game window size and the size of the snake and food
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 1

# Define constants for the colors used in the game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Triangle")

class Triangle:
    def __init__(self):
        self.set_base_points()
        self.set_first_point()

    def set_base_points(self):
        GAP: float = 100
        self.aPoint: (float, float) = (GAP, WINDOW_HEIGHT - GAP)
        self.bPoint: (float, float)  = (WINDOW_WIDTH - GAP, WINDOW_HEIGHT - GAP)
        self.cPoint: (float, float)  = (self.bPoint[0] - ((self.bPoint[0] - self.aPoint[0]) / 2), GAP) #  130 - ((130 - 80) / 2)
        self.positions = [self.aPoint, self.bPoint, self.cPoint]

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, WHITE, r)

    def set_first_point(self):
        x1, y1 = self.aPoint
        x2, y2 = self.bPoint
        x3, y3 = self.cPoint

        # Step 1: Calculate the area of the triangle
        area = 0.5 * abs((x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)))

        # Step 2: Choose two random numbers between 0 and 1
        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)

        # Step 3: Calculate sqrt(r1)
        sqrt_r1 = math.sqrt(r1)

        # Steps 4 and 5: Calculate the coordinates of the random point
        x = (1 - sqrt_r1) * x1 + (sqrt_r1 * (1 - r2)) * x2 + (sqrt_r1 * r2) * x3
        y = (1 - sqrt_r1) * y1 + (sqrt_r1 * (1 - r2)) * y2 + (sqrt_r1 * r2) * y3

        # Return the random point as a tuple
        self.positions.append((x, y))
        return (x, y)

    def midpoint(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        return (x, y)

    def set_next_point(self):
        prev_point = self.positions[-1]
        random_base_point = random.choice(self.positions[0:3])
        curr_point = self.midpoint(prev_point, random_base_point)
        self.positions.append(curr_point)
        return curr_point

def main():
    clock = pygame.time.Clock()
    game_over = False
    triangle = Triangle()
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        triangle.set_next_point()

        # Draw the game
        screen.fill(BLACK)
        triangle.draw(screen)
        pygame.display.set_caption(f"Number of points {len(triangle.positions)}")
        pygame.display.update()

        speed = 360
        # Wait for 1/{speed}th of a second
        clock.tick(speed)

    # Quit Pygame and exit the program
    pygame.quit()
    quit()
if __name__ == "__main__":
    main()