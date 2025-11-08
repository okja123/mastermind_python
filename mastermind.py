import copy
import math
from random import randint
import time
import pygame
import sys
import hashlib
class Point:
    def __init__(self, x , y):
        self.x = x
        self.y = y

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def __contains__(self, point):
        dist = math.hypot(point.x - self.x, point.y - self.y)
        return dist <= self.radius

class Rectangle:
    def __init__(self, x, y, length, width):
        self.x, self.y = x, y
        self.length, self.width = length, width

    def __contains__(self, point):
        return self.x <= point.x <= self.x + self.length and self.y <= point.y <= self.y + self.width
    

class MasterMind : 
    def __init__(self, attempt_possible, attempt_size,colors,secret):
        self.result = [(0,0) for _ in range(attempt_possible)] 
        self.attempt = [None] * attempt_possible
        self.current_attempt = [None] * attempt_size
        self.current_attempt_size = 0
        self.attempt_possible = attempt_possible
        self.attempt_size = attempt_size
        self.colors = colors
        self.starting_time = time.time()
        self.ending_time = None
        self.is_ended = False
        self.secret = secret

    def __init__(self, colors , attempt_possible = 10, attempt_size  = 4):
        self.result = [(0,0) for _ in range(attempt_possible)] 
        self.attempt = [None] * attempt_possible
        self.current_attempt = [None] * attempt_size
        self.current_attempt_size = 0
        self.current_attempt_index = 0
        self.attempt_possible = attempt_possible
        self.attempt_size = attempt_size
        self.colors = colors
        self.starting_time = time.time()
        self.ending_time = None
        self.is_ended = False
        self.is_won = False
        self.secret = [colors[randint(0,len(colors)-1)] for _ in range(attempt_size)]
    
    def set_color(self,color):
        if color not in self.colors :
            raise Exception("wrong color")
        for i in range(len(self.current_attempt)):
            if self.current_attempt[i] is None :
                self.current_attempt[i] = color
                self.current_attempt_size +=1
                break

    def remove_color(self,i):
        if i > self.attempt_size :
            raise IndexError
        self.current_attempt_size -= 1
        self.current_attempt[i] = None

    def test_current_attempt(self):
        if self.current_attempt_size != self.attempt_size :
            return
        attempt_copy = copy.deepcopy(self.current_attempt)
        secret_copy = copy.deepcopy(self.secret)
        result = [0,0]
        for i in range(self.attempt_size):
            if self.secret[self.attempt_size-i-1] == attempt_copy[self.attempt_size-i-1]:
                attempt_copy.pop(self.attempt_size-i-1)
                secret_copy.pop(self.attempt_size-i-1)
                result[0]+=1

        if result[0] == self.attempt_size :
            self.is_ended = True
            self.is_won = True
            self.ending_time = time.time()
            return
        
        for color in secret_copy:
            if color in attempt_copy:
                result[1] += 1
                attempt_copy.remove(color)

        self.attempt[self.current_attempt_index] = self.current_attempt
        self.result[self.current_attempt_index] = result
        self.current_attempt_index += 1
        self.current_attempt = [None] * self.attempt_size
        self.current_attempt_size = 0

        if self.current_attempt_index == self.attempt_possible :
            self.is_ended = True
            self.is_won = False
            self.ending_time = time.time()
        
    def get_state_of_game(self):
        return (self.attempt,self.result)
    
    def get_current_attempt(self):
        return self.current_attempt
    
class InterfaceGraphique_MasterMind:
    WHITE = (192, 192, 192)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RADIUS = 10

    def __init__(self, screen, clock):
        self.games = []
        self.current_game = None
        self.screen = screen
        self.clock = clock
        self.event_area = []
        self.current_attempt_event_area = []
        
    def start_new_game(self):
        new_game = MasterMind([1,2,3,4,5])
        self.games.append(new_game)
        self.current_game = new_game
        self.event_area = [(Rectangle(5,5,72-5,27-5),self.event_try_clicked,[])]
    
    def draw_main_frame(self):
        image = pygame.image.load("./.venv/img/Ecran.jpg").convert_alpha()
        self.screen.blit(image, (0, 0))
    
    def draw_color_palette(self):
        start_pos = (8,40)
        for i in range(len(self.current_game.colors)):
            h = hashlib.md5(str(self.current_game.colors[i]).encode()).digest()
            r, g, b = h[0], h[1], h[2]
            circle_pos = (start_pos[0] + self.RADIUS * 3 * i + self.RADIUS , start_pos[1] + self.RADIUS)
            pygame.draw.circle(self.screen, (r, g, b) , circle_pos , self.RADIUS)
            pygame.draw.circle(self.screen, self.BLACK, circle_pos , self.RADIUS, 1)
            self.event_area.append(((Circle(circle_pos[0],circle_pos[1],self.RADIUS)),self.event_color_clicked,[self.current_game.colors[i]]))

    def draw_attempt(self,pos,index):
        if self.current_game.attempt[index] is None:
            for i in range(self.current_game.attempt_size):
                circle_pos = (pos[0] + self.RADIUS * 3 * i + self.RADIUS , pos[1] + self.RADIUS)
                pygame.draw.circle(self.screen, self.BLACK, circle_pos , self.RADIUS, 1)
        else:    
            for i in range(self.current_game.current_attempt_size):
                color = self.current_game.attempt[index][i]
                h = hashlib.md5(str(color).encode()).digest()
                r, g, b = h[0], h[1], h[2]
                circle_pos = (pos[0] + self.RADIUS * 3 * i + self.RADIUS , pos[1] + self.RADIUS)
                pygame.draw.circle(self.screen, (r, g, b) , circle_pos , self.RADIUS)
                pygame.draw.circle(self.screen, self.BLACK, circle_pos , self.RADIUS, 1)

    def draw_responce(self,pos,index):
        responce_temp = list(self.current_game.result[index])
        for i in range(self.current_game.attempt_size):
            if responce_temp[0] > 0:
                responce_temp[0]-=1
                resp_color = (0,128,0)
            elif responce_temp[1] > 0 :
                responce_temp[1]-=1
                resp_color = (255,255,255)
            else:
                resp_color = self.WHITE
            circle_pos = (pos[0] + self.RADIUS * 3 * i * 0.5 + self.RADIUS , pos[1] + self.RADIUS)
            pygame.draw.circle(self.screen, resp_color, circle_pos, self.RADIUS*0.5)
            pygame.draw.circle(self.screen, self.BLACK,circle_pos , self.RADIUS*0.5, 1)  

    def update_current_attempt(self):
        start_pos = (8,80 + self.RADIUS * 3 * self.current_game.current_attempt_index)
        self.current_attempt_event_area = []
        for i in range(self.current_game.attempt_size):
            if self.current_game.current_attempt[i] is not None :
                color = self.current_game.current_attempt[i]
                h = hashlib.md5(str(color).encode()).digest()
                r, g, b = h[0], h[1], h[2]
            else :
               r, g, b = self.WHITE 
            circle_pos = (start_pos[0] + self.RADIUS * 3 * i + self.RADIUS , start_pos[1] + self.RADIUS)
            pygame.draw.circle(self.screen, (r, g, b) , circle_pos , self.RADIUS)
            pygame.draw.circle(self.screen, self.BLACK, circle_pos , self.RADIUS, 1)
            
            if self.current_game.current_attempt[i] is not None :
                self.current_attempt_event_area.append((Circle(circle_pos[0],circle_pos[1],self.RADIUS),self.event_remove_color_clicked,[i]))

    def draw_win(self):
        image = pygame.image.load("./.venv/img/win.jpg").convert_alpha()
        self.screen.fill((255, 255, 255))
        self.screen.blit(image, (0, 0))

    def draw_lose(self):
        image = pygame.image.load("./.venv/img/lose.jpg").convert_alpha()
        self.screen.fill((255, 255, 255))
        self.screen.blit(image, (0, 0))

    def draw_clock(self):
        start_pos = (286,7)
        rect = pygame.Rect(start_pos[0],start_pos[1], 60, 20)
        text_surface = pygame.font.SysFont('Comic Sans MS', 15).render(str(int(time.time()-self.current_game.starting_time)), False, (0, 0, 0))
        self.screen.fill(self.WHITE,rect)
        self.screen.blit(text_surface, (start_pos[0],start_pos[1]))


    def update_game(self):
        if self.current_game.is_ended :
            return
        start_pos = (8,80)
        for i in range(self.current_game.attempt_possible):
            current_pos = [start_pos[0] , start_pos[1] + self.RADIUS * 3 * i]
            self.draw_attempt(current_pos,i)
            current_pos = [start_pos[0]+ self.RADIUS * 3 * self.current_game.attempt_size , start_pos[1] + self.RADIUS * 3 * i + self.RADIUS * 0.5]
            self.draw_responce(current_pos,i)
        self.draw_clock()
    
    def event_color_clicked(self,arg):
        self.current_game.set_color(arg[0])

    def event_remove_color_clicked(self,arg):
        self.current_attempt_event_area.pop(arg[1])
        self.current_game.remove_color(arg[0])

    def event_try_clicked(self,arg):
        self.current_game.test_current_attempt()
        if self.current_game.is_ended:
            self.event_area = [(Rectangle(119,319,199-119,347-319),self.event_restart_clicked,[])]
            self.game_ended([])

    def event_restart_clicked(self,arg):
        self.start_new_game()
        self.draw_main_frame()
        self.draw_color_palette()

    def game_ended(self,arg):
        if self.current_game.is_won :
            self.draw_win()
        else :
            self.draw_lose()

    def handle_click(self,pos):
        as_changed = False
        for i in range(len(self.event_area)) : 
            if pos in self.event_area[i][0]:
                as_changed = True
                arg = self.event_area[i][2]
                arg.append(i)
                self.event_area[i][1](arg)
                break

        for i in range(len(self.current_attempt_event_area)): 
            if pos in self.current_attempt_event_area[i][0]:
                as_changed = True
                arg = self.current_attempt_event_area[i][2]
                arg.append(i)
                self.current_attempt_event_area[i][1](arg)
                break

        if self.current_game.is_ended:
            return
        if as_changed :
            self.update_current_attempt()


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((350, 450))
    clock = pygame.time.Clock()
    i_graphique = InterfaceGraphique_MasterMind(screen,clock)
    i_graphique.start_new_game()
    i_graphique.draw_main_frame()
    i_graphique.draw_color_palette()

    UPDATE_GAME_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(UPDATE_GAME_EVENT, 1000) 
    i_graphique.update_game()

    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            elif event.type == UPDATE_GAME_EVENT:
                i_graphique.update_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                i_graphique.handle_click(Point(event.pos[0],event.pos[1]))
        pygame.display.flip()
    pygame.quit()
    sys.exit()

main()