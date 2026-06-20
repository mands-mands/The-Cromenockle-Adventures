import sys
import pygame
from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Player import Player
from code.Enemy import Enemy
from code.Paper import Paper

class Level:
    def __init__(self, window):
        self.clock = pygame.time.Clock()
        self.window = window

        # Background
        self.fundo = pygame.image.load("./assets/scenario/level.png").convert()
        self.fundo = pygame.transform.scale(self.fundo, (WIN_WIDTH, WIN_HEIGHT))

        self.chao_img = pygame.image.load("./assets/scenario/chao.png").convert_alpha()
        self.plat_img = pygame.image.load("./assets/scenario/plataforma.png").convert_alpha()
        self.plat_img = pygame.transform.scale(self.plat_img, (96, 30))
        # Carrega corações
        self.heart_img = pygame.image.load("./assets/ui/heart.png").convert_alpha()
        self.heart_img = pygame.transform.scale(self.heart_img, (48, 48))  # aumenta pra ficar visível


        # Plataformas (x, y, largura, altura)
        self.plataformas = [
            pygame.Rect(0, WIN_HEIGHT - 70, WIN_WIDTH, 70),  # chão
            pygame.Rect(450, 480, 48, 5), # plataforma 1
            pygame.Rect(80, 400, 288, 5),  # plataforma 2
            pygame.Rect(0, 310, 48, 5),  # plataforma 2


        ]

        self.player = Player(self.window, self.plataformas)
        self.inimigos = [
            Enemy(self.window, 600, WIN_HEIGHT - 134, 700, 2, True),
            Enemy(self.window, 300, WIN_HEIGHT - 134, 700, 3),
            Enemy(self.window, 180, WIN_HEIGHT - 310, 150, 3),
        ]

        # No __init__ após self.player
        self.papeis = [
            Paper(self.window, 24, 280),  # posição 1
            Paper(self.window, 450, 200),  # posição 2
            Paper(self.window, 650, 350),  # posição 3
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

    def desenhar_hud(self):
        # Desenha corações conforme vida do player
        for i in range(self.player.vida):
            self.window.blit(self.heart_img, (10 + i * 55, 10))


    def run(self):
        while True:
            # Fundo
            self.window.blit(self.fundo, (0, 0))

            # Plataformas
            self.desenhar_plataformas()
            self.desenhar_hud()

            self.player.update()
            self.player.draw()

            for inimigo in self.inimigos:
                inimigo.update(self.player.rect)
                inimigo.draw()
                if self.player.rect.colliderect(inimigo.rect_dano):
                    self.player.tomar_dano()

            # Após self.player.draw()
            for papel in self.papeis:
                papel.draw()
                if not papel.coletado and self.player.rect.colliderect(papel.rect):
                    papel.coletado = True

            # Verifica vitória
            if all(p.coletado for p in self.papeis):
                return "vitoria"

            if self.player.morreu():
                pygame.display.flip()
                return "game_over"

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"