import pygame as pg
vec = pg.math.Vector2
import random
WIDTH = 1024
HEIGHT = 800
FPS = 20
BOARDX = 41
BOARDY = 32

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

Size = 25
foods = []

class Food:
    def __init__(self, pos):
        self.pos = pos

    def draw(self, iscreen):
        pg.draw.circle(screen, BLUE, [int(self.pos.x * Size + Size / 2), int(self.pos.y * Size + Size / 2)], int(Size / 2))

    def get_pos(self):
        return self.pos


class Snake():
    def __init__(self, pos):
        self.bodies = [pos + vec(0, 0), pos + vec(0, 1), pos + vec(0, 2), pos + vec(0, 3)]
        self.dir = vec(1, 0)

    def input(self):
        dir = vec()
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            if self.dir != vec(1, 0):
                dir = vec(-1, 0)
        if key[pg.K_RIGHT]:
            if self.dir != vec(-1, 0):
                dir = vec(1, 0)
        if key[pg.K_UP]:
            if self.dir != vec(0, 1):
                dir = vec(0, -1)
        if key[pg.K_DOWN]:
            if self.dir != vec(0, -1):
                dir = vec(0, 1)
        self.move(dir)

    def move(self, dir):
        if dir != vec():
            self.dir = dir

        l = len(self.bodies)
        for i in range(l - 1, 0, -1):
            self.bodies[i] = vec(self.bodies[i - 1])
        self.bodies[0] = vec(self.head() + self.dir)

    def in_snake_body(self, pos):
        for b in self.bodies:
            if b == pos:
                return True
        return False

    def eat_food(self, ifoods):
        food = None
        for f in ifoods:
            if f.get_pos() == self.head():
                food = f
                self.bodies.append(self.tail())
                break

        if food is not None:
            ifoods.remove(food)

    def check_die(self):
        head = self.head()
        # die boundary
        if head.x < 0 or head.x > BOARDX - 1 or head.y < 0 or head.y > BOARDY - 1:
            return True

        # die bodies
        l = len(self.bodies)
        for i in range(1, l):
            b = self.bodies[i]
            if self.head() == b:
                return True
        return  False

    def head(self):
        return self.bodies[0]

    def tail(self):
        l = len(self.bodies)
        return self.bodies[l - 1]

    def draw(self, iscreen):
        l = len(self.bodies)
        for i in range(l):
            b = self.bodies[i]
            if i % 2 == 0:
                color = BLACK
            else:
                color = RED
            pg.draw.rect(iscreen, color, [b.x * Size, b.y * Size, Size, Size])

def draw_board(iscreen):
    for i in range(0, BOARDX):
        pg.draw.line(iscreen, BLACK, [i * Size, 0], [i * Size, BOARDY * Size], 1)

    for i in range(0, BOARDY):
        pg.draw.line(iscreen, BLACK, [0, i * Size], [BOARDX * Size, i * Size], 1)

def gen_food(ifoods):
    if len(foods) < 100:
        if random.uniform(0, 1) < 0.2:
            randx = random.randint(0, BOARDX)
            randy = random.randint(0, BOARDY)

            # foods doesn't overlap
            for f in foods:
                if f.get_pos() == vec(randx, randy):
                    return;
            # foods doesn't overlap on snake
            if snake.in_snake_body(vec(randx, randy)):
                return

            food = Food(vec(randx, randy))
            ifoods.append(food)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('snake game')
clock = pg.time.Clock()
running = True
snake = Snake(vec(int(BOARDX / 2), int(BOARDY / 2)))

while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    snake.input()
    snake.eat_food(foods)
    gen_food(foods)
    if snake.check_die():
        running = False

    screen.fill(WHITE)
    draw_board(screen)
    snake.draw(screen)
    for f in foods:
        f.draw(screen)
    pg.display.update()
pg.quit()
