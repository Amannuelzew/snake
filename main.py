import pygame
import random
# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GREEN = (90, 90, 90)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
move_velocity = 20
GAP = 40
time = pygame.time.get_ticks()-move_velocity
turn = True
playing = False
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Set up game clock
# clock = pygame.time.Clock()


def grid():
    for y in range(30):
        if y % 2 == 0:
            turn = True
        for x in range(30):
            if turn:
                if x % 2 == 0:
                    pygame.draw.rect(screen, GRAY, (GAP*x, GAP*y, GAP, GAP))
                else:
                    pygame.draw.rect(screen, LIGHT_GREEN,
                                     (GAP*x, GAP*y, GAP, GAP))
            else:
                if x % 2 == 0:
                    pygame.draw.rect(screen, LIGHT_GREEN,
                                     (GAP*x, GAP*y, GAP, GAP))
                else:
                    pygame.draw.rect(screen, GRAY, (GAP*x, GAP*y, GAP, GAP))
        turn = False


class Segment():
    def __init__(self) -> None:
        self.segment = []
        for x in range(40, 80, GAP):
            self.segment.append((x, 120))


class Snake():
    def __init__(self) -> None:
        self.body = Segment().segment
        self.current = 2

    def collide(self):
        # check for collision
        for segment in self.body[0:-1]:
            if self.body[-1] == segment:
                return False
        return True

    def draw(self):
        for segment in self.body:
            if segment == self.body[-1]:
                pygame.draw.rect(
                    screen, GREEN, (segment[0], segment[1], GAP, GAP))
            else:
                pygame.draw.rect(
                    screen, BLACK, (segment[0], segment[1], GAP, GAP))

    def move(self):
        global playing
        # move the snake
        if self.current == 1:
            for i, _ in enumerate(self.body[0:-1]):
                self.body[i] = (self.body[i+1][0], self.body[i+1][1])
            self.body[-1] = (self.body[-1][0], self.body[-1][1]-GAP)

        elif self.current == 2:
            for i, _ in enumerate(self.body[0:-1]):
                self.body[i] = (self.body[i+1][0], self.body[i+1][1])
            self.body[-1] = (self.body[-1][0]+GAP, self.body[-1][1])

        elif self.current == 3:
            for i, _ in enumerate(self.body[0:-1]):
                self.body[i] = (self.body[i+1][0], self.body[i+1][1])
            self.body[-1] = (self.body[-1][0], self.body[-1][1]+GAP)

        elif self.current == 4:
            for i, _ in enumerate(self.body[0:-1]):
                self.body[i] = (self.body[i+1][0], self.body[i+1][1])
            self.body[-1] = (self.body[-1][0]-GAP, self.body[-1][1])
        # check if the snake moves out of the window
        if self.body[-1][0] >= 600:
            self.body[-1] = (0, self.body[-1][1])
        elif self.body[-1][0] < 0:
            self.body[-1] = (600, self.body[-1][1])
        elif self.body[-1][1] >= 600:
            self.body[-1] = (self.body[-1][0], 0)
        elif self.body[-1][1] < 0:
            self.body[-1] = (self.body[-1][0], 600)
        # check the head moves in to its body
        if not snakes.collide():
            playing = False

    # change orientation
    def change(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.current != 3:
            self.current = 1

        elif keys[pygame.K_RIGHT] and self.current != 4:
            self.current = 2

        elif keys[pygame.K_DOWN] and self.current != 1:
            self.current = 3

        elif keys[pygame.K_LEFT] and self.current != 2:
            self.current = 4

        # move to the right


class Fruit():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, GAP, GAP))


snakes = Snake()

fruit = Fruit(GAP*5, GAP*7)

# Game loop
running = True
while running:

    screen.fill(WHITE)
    grid()
    clock = pygame.time.Clock()
    pygame.time.delay(50)

    snakes.draw()
    if playing:
        snakes.move()
        snakes.change()

        if snakes.body[-1][0] == fruit.x and snakes.body[-1][1] == fruit.y:
            print("score", len(snakes.body))
            if snakes.current == 2:
                snakes.body.append((fruit.x+40, fruit.y))
            elif snakes.current == 4:
                snakes.body.append((fruit.x-40, fruit.y))
            elif snakes.current == 1:
                snakes.body.append((fruit.x, fruit.y-40))
            else:
                snakes.body.append((fruit.x, fruit.y+40))
            while True:
                rand_x = random.randint(0, 14)
                rand_y = random.randint(0, 14)
                for segment in snakes.body:
                    if segment == (GAP*rand_x, GAP * rand_y):
                        break
                else:
                    break
            fruit = Fruit(GAP*rand_x, GAP*rand_y)
        fruit.draw()

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(8)
    # Handle events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not playing:

            if event.dict.get('key') == pygame.K_SPACE:
                playing = True


# Quit Pygame
pygame.quit()
