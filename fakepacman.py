import pygame, sys
from pygame.draw import circle
from pygame.locals import *
import random
import json

pygame.init()
score = 0
move_speed = 5

def load(file):
    global rect_list
    global list_of_dots
    global list_of_pellets

    infile = open(file, 'r')
    level_text = infile.read()
    level = json.loads(level_text)
    rect_list = level["walls"]
    list_of_dots = level["dots"]
    list_of_pellets = level["giants"]

def collision_detect(rect1, rect2):
    if rect1["x"] < rect2["x"] + rect2["w"] and \
        rect1["x"] + rect1["w"] > rect2["x"]and \
        rect1["y"] < rect2["y"] + rect2["h"] and \
        rect1["h"] + rect1["y"] > rect2["y"]:
        return True
    else:
        return False

def swap_dict_tup(rectangle):
    rect_tup = (rectangle["x"], rectangle["y"], rectangle["w"], rectangle["h"])
    
    return rect_tup

def dot_rectangle(dotx, doty, dotr):
    dot_pos = (dotx, doty)
    rect = {"x": dot_pos[0]- dotr, "y": dot_pos[1]- dotr, "w": 2*dotr, "h": 2*dotr}
    return rect

class Player():
    def __init__(self, pos):
    
        self.pos = pos
        self.rad = 15
        self.direction = K_UP
    
    def move(self, list_of_walls, dot_list, pellet_list):
        keys = pygame.key.get_pressed()
        old_pos = self.pos 
        global score 
        if keys[K_DOWN]:
            self.direction = K_DOWN
            self.pos = (self.pos[0], self.pos[1]+move_speed)
        if keys[K_UP]:
            self.direction = K_UP
            
            self.pos = (self.pos[0], self.pos[1]-move_speed)
        if keys[K_LEFT]:
            self.direction = K_LEFT
            
            self.pos = (self.pos[0]- move_speed, self.pos[1])
        if keys[K_RIGHT]:
            self.direction = K_RIGHT
            
            self.pos = (self.pos[0] + move_speed, self.pos[1])
        if keys[K_w]:
            print(self.pos)
        if keys[K_r]:
            load('wall.txt')

        player_rect = dot_rectangle(self.pos[0], self.pos[1], self.rad)
    
        for wall in list_of_walls:
            if collision_detect(player_rect, wall):
                self.pos = old_pos
        for dot in dot_list:
            pill_rect = dot_rectangle(dot["x"], dot["y"], dot["r"])
            if collision_detect(player_rect, pill_rect):
                dot_list.remove(dot)
                score += 1
        for pellet in pellet_list:
            pell_rect = dot_rectangle(pellet["x"], pellet["y"], pellet["r"])
            if collision_detect(player_rect, pell_rect):
                pellet_list.remove(pellet)
                score += 5

            
    def draw(self, display_screen):
        open_factor = (pygame.time.get_ticks() % 1000) / 1000
        pygame.draw.circle(display_screen, YELLOW, self.pos, self.rad)
        jaw_open = self.rad * (open_factor - 0.5) * 2
        if self.direction == K_UP:
            pygame.draw.polygon(display_screen, BLACK, [(self.pos[0], self.pos[1]), (self.pos[0] + jaw_open, self.pos[1] - self.rad), (self.pos[0] - jaw_open, self.pos[1] - self.rad)])
        elif self.direction == K_DOWN:
            pygame.draw.polygon(display_screen, BLACK, [(self.pos[0], self.pos[1]), (self.pos[0] + jaw_open, self.pos[1] + self.rad), (self.pos[0] - jaw_open, self.pos[1] + self.rad)])
        elif self.direction == K_LEFT:
            pygame.draw.polygon(display_screen, BLACK, [(self.pos[0], self.pos[1]), (self.pos[0] - self.rad, self.pos[1] + jaw_open), (self.pos[0] - self.rad, self.pos[1] - jaw_open)])
        elif self.direction == K_RIGHT:
            pygame.draw.polygon(display_screen, BLACK, [(self.pos[0], self.pos[1]), (self.pos[0] + self.rad, self.pos[1] + jaw_open), (self.pos[0] + self.rad, self.pos[1] - jaw_open)])
        



FPS = 30
FramePerSec = pygame.time.Clock()

YELLOW = (255,255,0)
BLACK = (0, 0, 0)
BLUE = (0,0,255)
WHITE = (255,255,255)
display_screen = pygame.display.set_mode((400, 400))
#display_screen.fill(BLACK)



#pygame.draw.circle(display_screen, YELLOW, (100, 100), 30)

infile = open('wall.txt', 'r')
level_text = infile.read()
level = json.loads(level_text)
rect_list = level["walls"]
list_of_dots = level["dots"]
list_of_pellets = level["giants"]

#print(x, y, w, h)
#rect_list = [{"x": 200, "y": 350, "w": 100, "h": 50}, {"x": 200, "y": 0, "w": 80, "h": 40}, {"x": 0, "y": 200, "w": 90, "h": 70}]
p1 = Player((200, 350))
while True:
    p1.move(rect_list, list_of_dots, list_of_pellets)
    pygame.display.set_caption('Pacman Test - Score: ' + str(score))
    display_screen.fill(BLACK)
    p1.draw(display_screen)
    #pygame.draw.rect(display_screen, RED, (200, 350, 100, 50))
    for item in rect_list:
        pygame.draw.rect(display_screen, BLUE, swap_dict_tup(item))
    for item in list_of_dots:
        pygame.draw.circle(display_screen, WHITE, (item["x"], item["y"]), item["r"])
    for pellet in list_of_pellets:
        pygame.draw.circle(display_screen, YELLOW, (pellet["x"], pellet["y"]), pellet["r"])
    pygame.display.update()
    FramePerSec.tick(FPS)
    for event in pygame.event.get():
        if event.type == quit:
            pygame.quit()
            sys.exit()
    
