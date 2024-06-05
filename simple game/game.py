import pygame
import time
from random import randint

N = 4
K = 2
BOK = 100

czerwony = (255, 0, 0)
zielony = (0, 255, 0)
niebieski = (0, 0, 255)
zolty = (255, 255, 0)

t = [[0 for _ in range(N)] for _ in range(N)]
kolory = [czerwony, zielony, niebieski, zolty]

def kwadrat(x, y):
    pygame.draw.rect(win, kolory[t[x][y]], (x * BOK, y * BOK, BOK - 1, BOK - 1))

pygame.init()
win = pygame.display.set_mode((N * BOK, N * BOK))
pygame.display.set_caption("Moja gra")
win.fill((0,0,0))

kwadrat(1,1)

pygame.display.update()

def zmien_pole(x,y):
    t[x][y] = (t[x][y] + 1 ) % K
    kwadrat(x, y)

def ruch(x, y):
    zmien_pole(x, y)
    zmien_pole((x-1) % N, y)
    zmien_pole((x+1) % N, y)
    zmien_pole(x, (y+1) % N)
    zmien_pole(x, (y-1) % N)
    pygame.display.update()

for _ in range(50):
    ruch(randint(0, N-1), randint(0, N-1))

pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        ruch(pos[0]//BOK, pos[1]//BOK)
        time.sleep(1)