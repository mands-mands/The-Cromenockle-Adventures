import sys
import pygame
from code.Const import WIN_WIDTH, WIN_HEIGHT

class Level:
    def __init__(self, window):
        self.window = window

        # Background
        self.fundo = pygame.image.load("./assets/scenario/level.png").convert()
        self.fundo = pygame.transform.scale(self.fundo, (WIN_WIDTH, WIN_HEIGHT))

        self.chao_img = pygame.image.load("./assets/scenario/chao.png").convert_alpha()
        self.plat_img = pygame.image.load("./assets/scenario/plataforma.png").convert_alpha()


        # Plataformas (x, y, largura, altura)
        self.plataformas = [
            pygame.Rect(0, WIN_HEIGHT - 70, WIN_WIDTH, 70),  # chão
            pygame.Rect(100, 480, 48, 20),                   # plataforma 1

        ]

    def desenhar_plataformas(self):
        for i, plat in enumerate(self.plataformas):
            if i == 0:  # chão usa imagem diferente
                img = self.chao_img
            else:  # plataformas elevadas
                img = self.plat_img
            x = plat.x
            while x < plat.x + plat.width:
                self.window.blit(img, (x, plat.y))
                x += img.get_width()

    def run(self):
        while True:
            # Fundo
            self.window.blit(self.fundo, (0, 0))

            # Plataformas
            self.desenhar_plataformas()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"