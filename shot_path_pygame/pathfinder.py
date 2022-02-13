from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
import pygame,sys

class pathfinder:
    def __init__(self,matrix):
        self.matrix = matrix
        self.grid = Grid(matrix = matrix)
        self.mouse_pos = [1,1]
        self.bg_surf = pygame.image.load('select.png').convert_alpha()
        self.path=[]
        self.room = pygame.sprite.GroupSingle(Room())

    def draw_active_cell(self):
        self.mouse_pos = pygame.mouse.get_pos()
        row , col =  self.mouse_pos[1]//4 ,self.mouse_pos[0]//4
        crent_cell_value = self.matrix[row][col]
        if crent_cell_value == 1:
            rect = pygame.Rect((col*4 , row*4),(4,4))
            screen.blit(self.bg_surf,rect)

    def draw_path(self):
        if self.path:
            points = []
            for point in self.path:
                x = point[1]*4 + 5
                y = point[0]*4 + 5
                points.append((x,y))
            pygame.draw.lines(screen,'#4a4a4a',False,points,5)

    def creat_path(self):
        x , y = self.room.sprite.get_pos()
        start = self.grid.node(x,y)
        n1= self.mouse_pos[1]//4
        n2 =self.mouse_pos[0]//4
        end = self.grid.node( n1,n2)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.path , runs = finder.find_path(start,end,self.grid)
        print(self.path[-1])
        self.grid.cleanup()
        self.room.sprite.set_path(self.path)

    def update(self):
        self.draw_active_cell()
        self.draw_path()

        self.room.update()
        self.room.draw(screen)

class Room(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('car.png').convert_alpha()
        self.rect = self.image.get_rect(center = (50,50))

        self.pos = self.rect.center
        self.speed = 0.06
        self.direction = pygame.math.Vector2(0,0)
        self.path = []
        self.collision_rect = []
        

    def get_pos(self):
        col = self.rect.centerx // 4
        row = self.rect.centery // 4
        return (col,row)

    def set_path(self ,path):
        self.path = path
        self.create_collision_rect()
        self.get_direction()
    
    def create_collision_rect(self):
        if self.path:
            self.collision_rect = []
            for point in self.path:
                x = point[1]*4 
                y = point[0]*4 
                rect = pygame.Rect((x-4,y-4),(4,4))
                self.collision_rect.append(rect)

    def get_direction(self):
        try:
            if self.collision_rect[0]:
                start = pygame.math.Vector2(self.pos)
                end = pygame.math.Vector2(self.collision_rect[0].center)
                self.direction = (end - start).normalize()
            else:
                start = pygame.math.Vector2(0,0)
                self.path = []
        except:
            start = pygame.math.Vector2(0,0)
            self.path = []
    
    def chack_collisions(self):
        for rect in self.collision_rect:
            if rect.collidepoint(self.pos):
                del self.collision_rect[0]
                self.get_direction()

    def update(self):
        try:
            self.pos += self.direction * self.speed
            self.chack_collisions()
            self.rect.center = self.pos
            print(self.pos,"   ",self.path[-1],"   ",self.direction)
        except:
            self.rect.center = self.pos
            print(10)

pygame.init()
screen = pygame.display.set_mode((260,190))
clock =  pygame.time.Clock()

bg_surf = pygame.image.load('test5.png').convert()

matrix = [[1 for _ in range(120)] for _ in range(120) ]


pathfinder = pathfinder(matrix)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pathfinder.creat_path()
    screen.blit(bg_surf,(0,0))
    pathfinder.update()
    pygame.display.update()
    clock.tick(60)