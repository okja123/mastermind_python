import copy
import math
from random import randint
import pygame
import sys
import hashlib
import time
NBR_COLOR = 9
#COLOR = [i for i in range(NBR_COLOR)]
COLOR = [1,9,2,3,4,5]
SIZE = 4
MAX_ATTEMPT = 10
WINDOW_SIZE = 400
WHITE = (192, 192, 192)
BLACK = (0, 0, 0)

def scoring(tab,secret):
    global WIN
    secretcpy = copy.deepcopy(secret)
    tabcpy = copy.deepcopy(tab)
    lensecret , lentab = len(secret) - 1,len(tab) - 1
    score = [0,0]
    for i in range(lentab+1):
        if tab[lentab - i] == secret[lentab - i]:
            score[0] += 1
            secretcpy.pop(lentab - i)
            tabcpy.pop(lentab - i)
    if score[0] == SIZE :
        WIN = pygame.event.Event(pygame.USEREVENT + 1 )
        pygame.event.post(WIN)
    lensecret , lentab = len(secretcpy) - 1,len(tabcpy) - 1
    for i in tabcpy:
        lensecret = len(secretcpy) - 1
        for j in range(lensecret+1) :
            if i == secretcpy[lensecret-j] :
                score[1] += 1 
                secretcpy.pop(lensecret-j)
                break
    return score
    

def event_color_is_clicked(i):
    if len(GAME[CURRENT_ATTEMPT_INDEX][0])<SIZE:
        GAME[CURRENT_ATTEMPT_INDEX][0].append(i)
    else:
        GAME[CURRENT_ATTEMPT_INDEX][0].append(i)
        GAME[CURRENT_ATTEMPT_INDEX][0].pop(0)
    update_game()
def draw_color_pallette():
    gap = 10
    radius = 10
    rect = pygame.Rect(13,80, (radius * 2 + gap)* len(COLOR), 20)
    SCREEN.fill(WHITE,rect)
    for i in range(len(COLOR)):
        hash_bytes = hashlib.md5(str(COLOR[i]).encode()).digest()
        r, g, b = hash_bytes[0], hash_bytes[1], hash_bytes[2]
        pygame.draw.circle(SCREEN, (r, g, b), (15 + (radius * 2+ gap)* i + radius ,80+ radius), radius)
        pygame.draw.circle(SCREEN, BLACK, (15 + (radius * 2+ gap)* i + radius ,80+ radius), radius, 1)
        EVENT_AREA.append((("circle",(15 + (radius * 2+ gap)* i + radius ,80+ radius),radius),event_color_is_clicked,COLOR[i]))

def draw_attempt(attempt,pos):
    if len(attempt)>SIZE:
        raise Exception("trop de couleur dan lattempt")
    gap = 8
    radius = gap
    rect = pygame.Rect(pos[0],pos[1], (radius * 2 + gap)* SIZE,gap*2)
    SCREEN.fill(WHITE,rect)
    for i in range(SIZE):
        if i < len(attempt):
            hash_bytes = hashlib.md5(str(attempt[i]).encode()).digest()
            r, g, b = hash_bytes[0], hash_bytes[1], hash_bytes[2]
            pygame.draw.circle(SCREEN, (r, g, b), (pos[0]  + (radius * 2+ gap)* i + radius ,pos[1] + radius), radius)
        else:
            pygame.draw.circle(SCREEN, WHITE, (pos[0] + (radius * 2+ gap)* i + radius ,pos[1] + radius), radius)
        pygame.draw.circle(SCREEN, BLACK, (pos[0] + (radius * 2+ gap)* i + radius ,pos[1] + radius), radius, 1)

def draw_responce(responce,pos):
    respponce_temp = copy.deepcopy(responce)
    gap = 6
    radius = gap
    rect = pygame.Rect(pos[0],pos[1], (radius * 2 + gap)* SIZE,gap*2)
    SCREEN.fill(WHITE,rect)
    for i in range(SIZE):
        if respponce_temp[0] > 0:
            respponce_temp[0]-=1
            resp_color = (0,128,0)
        elif respponce_temp[1] > 0 :
            respponce_temp[1]-=1
            resp_color = (255,255,255)
        else:
            resp_color = WHITE
        pygame.draw.circle(SCREEN, resp_color, (pos[0] + (radius * 2+ gap)* i + radius ,pos[1] + radius), radius)
        pygame.draw.circle(SCREEN, BLACK, (pos[0] + (radius * 2+ gap)* i + radius ,pos[1] + radius), radius, 1)  

def update_game():
    gap = 20
    for i in range(len(GAME)):
        draw_attempt(GAME[i][0],(14,107+gap*i))
        if GAME[i][1] is not None:
            draw_responce(GAME[i][1],(200,107+gap*i))
def is_shape_colliding(shape,pos):
    if shape[0] == "circle":
        d = math.sqrt((shape[1][0] - pos[0])**2+(shape[1][1] - pos[1])**2)
        return shape[2] > d
    if shape[0] == "rect":
        return (shape[1][0] <= pos[0] and pos[0] <= shape[2][0]) and (shape[1][1] <= pos[1] and pos[1] <= shape[2][1])
    return False
def update_Clock():
    rect = pygame.Rect(272,45, 64, 20)
    text_surface = FONT.render(str(int(time.process_time())), False, (0, 0, 0))
    SCREEN.fill(WHITE,rect)
    SCREEN.blit(text_surface, (272,45))
def handle_click(pos):
    for elt in EVENT_AREA : 
        if is_shape_colliding(elt[0],pos):
            elt[1](elt[2])
def event_try_clicked(i):
    global CURRENT_ATTEMPT_INDEX
    print(SECRET)
    if len(GAME[CURRENT_ATTEMPT_INDEX][0]) != SIZE:
        return
    GAME[CURRENT_ATTEMPT_INDEX][1] = scoring(GAME[CURRENT_ATTEMPT_INDEX][0],SECRET)
    CURRENT_ATTEMPT_INDEX += 1
    update_game()
def draw_win():
    image = pygame.image.load("./img/win.jpg").convert_alpha()
    SCREEN.fill((255, 255, 255))
    SCREEN.blit(image, (0, 0))
def main():
    global SCREEN, CLOCK , GAME , FONT , EVENT_AREA , CURRENT_ATTEMPT_INDEX , SECRET , RUNNING , WIN
    WIN = False
    SECRET = [COLOR[randint(0,len(COLOR)-1)] for _ in range(SIZE)]
    EVENT_AREA = [(("rect",(8,48),(78,68)),event_try_clicked,0)]
    CURRENT_ATTEMPT_INDEX = 0
    GAME = [[[],None] for _ in range(MAX_ATTEMPT)]
    pygame.init()
    pygame.font.init()
    SCREEN = pygame.display.set_mode((335, 431))
    CLOCK = pygame.time.Clock()
    FONT = pygame.font.SysFont('Comic Sans MS', 30)
    image = pygame.image.load("./img/Ecran.jpg").convert_alpha()
    SCREEN.fill((255, 255, 255))
    SCREEN.blit(image, (0, 0))
    rect = pygame.Rect(10,100,222,320)
    SCREEN.fill(WHITE,rect)

    update_Clock()
    draw_color_pallette()
    update_game()
    RUNNING = True
    while RUNNING:
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            elif event.type == pygame.USEREVENT + 1 :
                draw_win()
            elif event.type == pygame.MOUSEBUTTONDOWN:
               handle_click(event.pos)
      CLOCK.tick(600)
      update_Clock()
      pygame.display.flip()
    if WIN :
        print("win")
    else :
        print("lose")
    pygame.quit()
    sys.exit()

main()