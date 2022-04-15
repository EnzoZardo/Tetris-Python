import pygame
from molde_tetris import MOLDE_ALFABETO


class Screen_tools:
    def __init__(self) -> None:
        self.cores = ((0, 0, 255), (255, 255, 0), (150, 150, 255), (255, 0, 0), (150, 150, 150), (255, 255, 100), (255, 0, 255));
        self.cor_indice = 0;
        self.clicked = False;

    def TETRIS(self, x_pos, y_pos):
        from settings import SCREEN, DRAW_R, DRAW_P, SCREEN_SIZE
        for el in MOLDE_ALFABETO:   
            for indice, y in enumerate(el, 0):
                for ind, x in enumerate(y, 0):
                    if x.upper() == 'X':
                        DRAW_R(SCREEN, self.cores[self.cor_indice % (len(self.cores) - 1)], (x_pos + ind * 25, y_pos + indice * 25, 25, 25));
                    elif x.upper() == "T":
                        DRAW_P(SCREEN, self.cores[self.cor_indice % (len(self.cores) - 1)], [(x_pos + ind * 25, y_pos + indice * 25), (x_pos + ind * 25 + 24, y_pos + indice * 25 + 25), (x_pos + ind * 25, y_pos + indice * 25 + 25)]);
            self.cor_indice += 1;
            x_pos += 90;

    def button(self, x_pos: float, y_pos: float, w: float, h: int, text: str, colores: tuple):
        from settings import SCREEN, DRAW_R
        self.mouse_pos_x, self.mouse_pos_y = pygame.mouse.get_pos();
        pygame.font.init();
        DRAW_R(SCREEN, colores, (x_pos, y_pos, w, h));
        SCREEN.blit(pygame.font.SysFont(pygame.font.get_default_font(), 150).render(text, 1, (0, 0, 0)), (x_pos, y_pos));
        if (x_pos <= self.mouse_pos_x and self.mouse_pos_x <= x_pos + w and y_pos <= self.mouse_pos_y and self.mouse_pos_y <= y_pos + h):
            try:
                DRAW_R(SCREEN, (colores[0] - 50, colores[1] - 50, colores[2] - 100), (x_pos, y_pos, w, h));
            except:
                DRAW_R(SCREEN, colores, (x_pos, y_pos, w, h));
            SCREEN.blit(pygame.font.SysFont(pygame.font.get_default_font(), 150).render(text, 1, (0, 0, 0)), (x_pos, y_pos));
            if (pygame.mouse.get_pressed()[0]):
                self.clicked = True;
        return self.clicked;

