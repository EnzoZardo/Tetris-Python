import pygame
from Piece import *
from Ground import Ground
from copy import deepcopy
import Screen_tools

pygame.init();
pygame.display.set_caption("TETRIS");
SCREEN_SIZE = (600, 720);
SCREEN_COLOR = (0, 0, 0);
SCREEN = pygame.display.set_mode(SCREEN_SIZE);
CLOCK = pygame.time.Clock();
FPS = 16;
is_running = True;
GROUND = Ground();
TOOL = Screen_tools.Screen_tools();
tiles = [Piece(210, -220, pode_mover=False)];
list_y = [];
DRAW_L = pygame.draw.line;
DRAW_R = pygame.draw.rect;
DRAW_P = pygame.draw.polygon;

def is_closed():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False;
    return True;

def run_updates():
    draw_grid();
    GROUND.draw();
    for x in tiles:
        x.update(tiles);
        for g in x.get_rect_list():
            if (not(x.pode_mover)):
                list_y.append(g.y);
    full_line = verifica_linha();
    if (full_line != SCREEN_SIZE[1]):
        for _ in tiles:
            if (_.y <= full_line and full_line <= _.y + 30 * len(_.this_molde[_.ESTAGIO % 4]) + _.TILE_SIZE):
                for indice, x in enumerate(_.this_molde[_.ESTAGIO % 4]):
                    if _.y + indice * 30 == full_line:
                        _.pode_quebrar = True;               
            if (_.y < full_line and not(_.pode_quebrar)):
                _.y += _.GRAVIDADE;
    full_line = SCREEN_SIZE[1];
    list_y.clear();
    
def verifica_linha():
    for i in list_y:
        if list_y.count(i) == 16 and i > 0:
            return i;
    return SCREEN_SIZE[1];

def add_new_piece(lista: list):
    if (not(lista[-1].pode_mover)):
        lista.append(Piece(210, -60));

def draw_grid():
    for i in range(0, (SCREEN_SIZE[0]) // 30):
        DRAW_L(SCREEN, (40, 40, 40), (i * 30, 0), (i * 30, SCREEN_SIZE[1] - 30), 2);
    for x in range(0, (SCREEN_SIZE[1]) // 30):
        DRAW_L(SCREEN, (40, 40, 40), (60, x * 30), (SCREEN_SIZE[0] - 60, x * 30), 2);

def start_screen():
    if (not(TOOL.clicked)):
        TOOL.TETRIS(35, 60);
        return TOOL.button(165, 250, 270, 90, "PLAY", (255, 255, 255));
    return True;

def apply_settings():
    pygame.display.flip();
    SCREEN.fill(SCREEN_COLOR);
    CLOCK.tick(FPS);
    if (start_screen()):
        run_updates();
        add_new_piece(tiles);