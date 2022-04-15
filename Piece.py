import pygame
from molde import MOLDE
from random import randint
import copy

class Piece:
    def __init__(self, x, y, molde=MOLDE, pode_mover=True) -> None:
        self.x = x;
        self.y = y;
        self.COLOR = ((0, 0, 255), (255, 255, 0), (150, 150, 255), (255, 0, 0), (150, 150, 150), (255, 255, 100), (255, 0, 255));
        self.molde = copy.deepcopy(molde);
        self.PIECE_NUMBER = randint(0, len(self.molde) - 1);
        self.this_molde = self.molde[self.PIECE_NUMBER].copy();
        self.GRAVIDADE = 15;
        self.VELOCIDADE = 30;
        self.TILE_SIZE = 30;
        self.QUADRADO = pygame.Surface((30, 30));
        self.QUADRADO.fill(self.COLOR[self.PIECE_NUMBER]);
        self.ESTAGIO = 0;
        self.pode_mover = pode_mover;
        self.BATEU = False;
        self.pode_quebrar = False;

    def draw(self):
        from settings import SCREEN
        for indice, y in enumerate(self.this_molde[self.ESTAGIO % 4], 0):
            for ind, x in enumerate(y, 0):
                if x.upper() == 'X':
                    SCREEN.blit(self.QUADRADO, (self.x + ind * self.TILE_SIZE, self.y + indice * self.TILE_SIZE));

    def turn(self, that_list):
        self.KEY = pygame.key.get_pressed();
        if (self.KEY[pygame.K_SPACE] and self.pode_mover):
            self.ESTAGIO += 1;
            if (self.get_colisao(that_list)):
                self.ESTAGIO -= 2;
                while(self.get_colisao(that_list)):
                    self.y -= self.GRAVIDADE;

    def move(self, that_list):
        from settings import SCREEN_SIZE
        self.KEY = pygame.key.get_pressed();
        if (self.KEY[pygame.K_RIGHT] and self.pode_mover and self.get_max_x() + self.TILE_SIZE < SCREEN_SIZE[0] - 60):
            self.x += self.VELOCIDADE;
            if (self.get_colisao(that_list)):
                self.x -= self.VELOCIDADE;
        if (self.KEY[pygame.K_LEFT] and self.pode_mover and self.get_min_x() > 60):
            self.x -= self.VELOCIDADE;
            if (self.get_colisao(that_list)):
                self.x += self.VELOCIDADE;

    def aplica_gravidade(self):
        from settings import SCREEN_SIZE
        if (self.pode_mover):
            self.y += self.GRAVIDADE;
        else:
            self.pode_mover = False;
        
    def get_rect_list(self):
        self.rect_list = [];
        for indice, y in enumerate(self.this_molde[self.ESTAGIO % 4], 0):
            for ind, x in enumerate(y, 0):
                if x.upper() == 'X':
                    self.r_QUADRADO = self.QUADRADO.get_rect()
                    self.r_QUADRADO.x = self.x + ind * self.TILE_SIZE;
                    self.r_QUADRADO.y = self.y + indice * self.TILE_SIZE;
                    self.rect_list.append(self.r_QUADRADO);
        return (self.rect_list);

    def get_min_x(self):
        self.min = self.get_rect_list()[0].x;
        for x in self.get_rect_list():
            if (self.min > x.x):
                self.min = x.x;
        return self.min;

    def get_max_x(self):
        self.max = self.get_rect_list()[0].x;
        for x in self.get_rect_list():
            if (self.max < x.x):
                self.max = x.x;
        return self.max;

    def get_min_y(self):
        self.min = self.get_rect_list()[0].y if len(self.get_rect_list()) > 0 else self.y;
        for x in self.get_rect_list():
            if (self.min > x.y):
                self.min = x.y;
        return self.min;

    def get_max_y(self):
        self.max = self.get_rect_list()[0].y if len(self.get_rect_list()) > 0 else self.y + self.TILE_SIZE * len(self.this_molde[self.ESTAGIO % 4]);
        for x in self.get_rect_list():
            if (self.max < x.y):
                self.max = x.y;
        return self.max;

    def ajusta_pos_y(self):
        from settings import GROUND
        if (not(self.pode_mover) and self.get_max_y() + self.TILE_SIZE > GROUND.r_GROUND.y):
            self.y -= 1;
        elif (not(self.pode_mover) and self.get_min_y() % 30 != 0):
            self.actual_pos = self.y;
            self.to_add = 0
            while ((self.actual_pos + self.to_add) % 30 != 0):
                self.to_add += 1;
            self.y += self.to_add;

    def verifica_fantasma(self):
        if (self.pode_mover):
            from settings import SCREEN_SIZE
            if (self.get_min_x() < 60):
                self.x += self.VELOCIDADE;
            if (self.get_max_x() + self.TILE_SIZE > SCREEN_SIZE[0] - 60):
                self.x -= self.VELOCIDADE;

    def get_colisao(self, that_list):
        for element in that_list:
            self.colisao(element);
        if (self.BATEU):
            self.BATEU = False;
            return True;
        return False
    
    def colisao(self, that: object):
        self.GROUND_colisao();
        if (that != self):
            self.this = self.get_rect_list();
            self.that = that.get_rect_list();
            for x in self.this:
                for i in self.that:
                    if (x.colliderect(i)):
                        self.freio();
                        self.BATEU = True;
            self.this.clear();
            self.that.clear();

    def GROUND_colisao(self):
        from settings import GROUND
        for element in self.get_rect_list()[::-1]:
            if (element.colliderect(GROUND.r_GROUND)):
                self.freio();

    def freio(self):
        if (self.pode_mover):
            self.y -= self.GRAVIDADE;
            self.pode_mover = False;

    def separe_lines(self, that_list: list):
        for indice, y in enumerate(self.this_molde[self.ESTAGIO % 4], 0):
            for ind, x in enumerate(y, 0):
                if x.upper() == 'X':
                    that_list.append(Piece(self.x + ind * self.TILE_SIZE, self.y + indice * self.TILE_SIZE, [["X"], ["X"], ["X"], ["X"]], False));

    def quebrou(self, that_list: list):
        if (self.pode_quebrar):
            that_list.remove(self);
            self.pode_quebrar = False;

    def update(self, that_list):
        self.draw();
        self.turn(that_list);
        self.move(that_list);
        self.aplica_gravidade();
        self.verifica_fantasma();
        self.get_colisao(that_list);
        self.ajusta_pos_y();        
        self.quebrou(that_list);
