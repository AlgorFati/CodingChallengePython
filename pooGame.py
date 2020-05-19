import pygame as pg
vec = pg.math.Vector2
import random

WIDTH = 1024
HEIGHT = 800
FPS = 60
WHITE = (255, 255, 255)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('poo game')
clock = pg.time.Clock()
running = True
poos = pg.sprite.Group()

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('player.png')
        self.rect = self.image.get_rect()
        self.set_pos(vec(WIDTH/2, 700))

    def set_pos(self, pos):
        self.pos = pos
        self.rect.center = self.pos

    def update(self):
        vel = vec()
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            vel.x = -5
        if key[pg.K_RIGHT]:
            vel.x = 5
        self.set_pos(self.pos + vel)

    def check_collide(self, sprite):
        return self.rect.colliderect(sprite.rect)

class Poo(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('poo.png')
        self.image = pg.transform.scale(self.image, (50, 45))
        self.rect = self.image.get_rect()
        self.set_pos(vec(random.uniform(0, 1) * WIDTH, random.uniform(0, 1) * 100))

    def set_pos(self, pos):
        self.pos = pos
        self.rect.center = self.pos

    def update(self):
        self.set_pos(self.pos + vec(0, 5))
        # die
        if self.pos.y > 700:
            self.kill()

def addPoo():
    if random.uniform(0, 1) < 0.1:
        poo = Poo()
        poos.add(poo)

player = Player()
players = pg.sprite.Group()
players.add(player)

while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    player.update()
    addPoo()

    for p in poos:
        p.update()
        if player.check_collide(p):
            running = False

    screen.fill(WHITE)
    players.draw(screen)
    poos.draw(screen)
    pg.display.update()

pg.quit()