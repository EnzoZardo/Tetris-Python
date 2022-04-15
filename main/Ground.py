import pygame

class Ground:
    def __init__(self) -> None:    
        from settings import SCREEN_SIZE
        self.BORDER_COLOR = (100, 100, 150);
        self.GROUND_SIZE = (SCREEN_SIZE[0], 30);
        self.GROUND = pygame.Surface(self.GROUND_SIZE);
        self.GROUND.fill(self.BORDER_COLOR);
        self.r_GROUND = self.GROUND.get_rect();
        self.r_GROUND.x = 0;
        self.r_GROUND.y = SCREEN_SIZE[1] - self.GROUND_SIZE[1];
        self.rect_list = [self.r_GROUND];
    
    def get_rect_list(self):
        return self.rect_list;

    def draw(self):
        from settings import SCREEN, SCREEN_SIZE, DRAW_R
        SCREEN.blit(self.GROUND, (self.r_GROUND.x, self.r_GROUND.y));
        self.BORDER_COLOR = (100, 100, 150);
        DRAW_R(SCREEN, self.BORDER_COLOR, (0, 0, 60, SCREEN_SIZE[1] - 0.04 * SCREEN_SIZE[1]));
        DRAW_R(SCREEN, self.BORDER_COLOR, (SCREEN_SIZE[0] - 60, 0, 60, SCREEN_SIZE[1] - 0.04 * SCREEN_SIZE[1]));

    def update(self, *args):
        self.draw();