
import pygame
from sys import exit
from random import randrange

pygame.init()


SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont(None, 15)
pygame.display.set_caption('game')

clock = pygame.time.Clock()


class Player:
    def __init__(self):
        self.coor = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.size = 20
        self.color = (0, 255, 255)
        self.surface = pygame.Surface((self.size, self.size))
        self.surface.fill(self.color)        
        self.vx = 0
        self.vy = 0
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.vy = -2
        if keys[pygame.K_s]:
            self.vy = 2
        if keys[pygame.K_a]:
            self.vx = -2
        if keys[pygame.K_d]:
            self.vx = 2
        self.coor = (self.coor[0] + self.vx, self.coor[1] + self.vy)
        self.vy, self.vx = 0, 0

#directions 0123, u d l r 
class Bullet:
    def __init__(self, pl_coor, direction):
        self.coor = (pl_coor[0] + 10, pl_coor[1] + 10)
        self.size = 6
        self.color = (255, 255, 255)
        self.surface = pygame.Surface((self.size, self.size))
        self.surface.fill(self.color)
        if direction == 0:
            self.vx = 0
            self.vy = -5
        if direction == 1:
            self.vx = 0
            self.vy = 5
        if direction == 2:
            self.vx = -5
            self.vy = 0
        if direction == 3:
            self.vx = 5
            self.vy = 0
        if direction == 4:
            self.vx = 0
            self.vy = 0
    def move(self):
        self.coor = (self.coor[0] + self.vx, self.coor[1] + self.vy)
    def check(self, obj):
        if self.coor[0] > obj.coor[0] and self.coor[0] + self.size < obj.coor[0] + obj.size:
            if self.coor[1] > obj.coor[1] and self.coor[1] + self.size < obj.coor[1] + obj.size:
                return True
            
class Enemy:
    def __init__(self):
        self.coor = (randrange(SCREEN_WIDTH), randrange(SCREEN_HEIGHT))
        self.size = 20
        self.color = (255, 0, 0)
        self.surface = pygame.Surface((self.size, self.size))
        self.surface.fill(self.color)        
        self.speed = 1
    def move(self, pl_coor):
        if pl_coor[0] > self.coor[0]:
            self.coor = (self.coor[0] + self.speed, self.coor[1])
        if pl_coor[1] > self.coor[1]:
            self.coor = (self.coor[0], self.coor[1] + self.speed)
        if pl_coor[0] < self.coor[0]:
            self.coor = (self.coor[0] - self.speed, self.coor[1])
        if pl_coor[1] < self.coor[1]:
            self.coor = (self.coor[0], self.coor[1] - self.speed)
        if pl_coor[0] - self.coor[0] <= 2 and pl_coor[1] - self.coor[1] <= 2:
            if self.coor[0] - pl_coor[0] <= 2 and self.coor[1] - pl_coor[1] <= 2:

        #if round(pl_coor[0], -10) == round(self.coor[0], -10) and round(pl_coor[1] - 10) == round(self.coor[1], -10):
                pygame.quit()
class fastEnemy(Enemy):
    def __init__(self):
        self.coor = (randrange(SCREEN_WIDTH), randrange(SCREEN_HEIGHT))
        self.size = 20
        self.color = (200, 200, 200)
        self.surface = pygame.Surface((self.size, self.size))
        self.surface.fill(self.color)        
        self.speed = 3
        
        

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

running = True
player = Player()
bullets = []
enemies = []
level = 1
sec_event = pygame.USEREVENT + 1
pygame.time.set_timer(sec_event, 500)






while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == sec_event:
            level = level + 1
            if level > len(enemies):
                if randrange(10) == 0:
                    enemies.append(fastEnemy())
                else: 
                    enemies.append(Enemy())
    screen.fill('Black')
    player.move()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_i]:
        bullets.append(Bullet(player.coor, 0))
    if keys[pygame.K_k]:
        bullets.append(Bullet(player.coor, 1))
    if keys[pygame.K_j]:
        bullets.append(Bullet(player.coor, 2))
    if keys[pygame.K_l]:
        bullets.append(Bullet(player.coor, 3))
    for item in enemies:
        item.move(player.coor)
        screen.blit(item.surface, item.coor)
        for bullet in bullets:
            if bullet.coor[0] < 0 or bullet.coor[1] < 0:
                bullets.remove(bullet)
            if bullet.coor[0] > SCREEN_WIDTH or bullet.coor[1] > SCREEN_HEIGHT:
                bullets.remove(bullet)
            if bullet.check(item):
                if bullet in bullets:
                    bullets.remove(bullet)
                if item in enemies:
                    enemies.remove(item)
                level = level + 1
    for item in bullets:
        item.move()
        screen.blit(item.surface, item.coor)
    screen.blit(player.surface, player.coor)
    draw_text(str(level), font, 'White', (SCREEN_WIDTH - 50), (SCREEN_HEIGHT - 50))
    pygame.display.update()
    clock.tick(60)
pygame.quit()

