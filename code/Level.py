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
        pygame.mixer.music.stop()
        pygame.mixer.music.load("./assets/sound/level.mp3")
        pygame.mixer.music.play(-1)

        # Background
        self.fundo = pygame.image.load("./assets/scenario/level.png").convert()
        self.fundo = pygame.transform.scale(self.fundo, (WIN_WIDTH, WIN_HEIGHT))

        self.chao_img = pygame.image.load("./assets/scenario/chao.png").convert_alpha()
        self.plat_img = pygame.image.load("./assets/scenario/plataforma.png").convert_alpha()
        self.plat_img = pygame.transform.scale(self.plat_img, (110, 40))
        # Carrega corações
        self.heart_img = pygame.image.load("./assets/ui/heart.png").convert_alpha()
        self.heart_img = pygame.transform.scale(self.heart_img, (32, 32))  # aumenta pra ficar visível

        self.paper_hud = pygame.image.load("./assets/sprites/paper.png").convert_alpha()
        self.paper_hud = pygame.transform.scale(self.paper_hud, (28, 28))

        self.torre_img = pygame.image.load("./assets/scenario/torre.png").convert_alpha()
        self.torre_img = pygame.transform.scale(self.torre_img, (80, 120))
        self.torre_rect = self.torre_img.get_rect(bottomleft=(0, 130))
        self.torre_colisao = pygame.Rect(30, 105, 30, 25)  # só na porta da torre


        # Plataformas (x, y, largura, altura)
        self.plataformas = [
            pygame.Rect(0, WIN_HEIGHT - 70, WIN_WIDTH, 70),  # chão
            pygame.Rect(450, 480, 110, 20),  # plataforma 1 — era 48, agora 110
            pygame.Rect(80, 400, 330, 20),  # plataforma 2 — era 288
            pygame.Rect(0, 310, 110, 20),  # plataforma 3
            pygame.Rect(180, 250, 110, 5),  # plataforma 4
            pygame.Rect(370, 230, 110, 5),  # plataforma 5
            pygame.Rect(560, 170, 330, 5),  # plataforma 6
            pygame.Rect(430, 80, 110, 5),  # plataforma 7
            pygame.Rect(210, 80, 110, 5),  # plataforma 8
            pygame.Rect(0, 130, 110, 5),  # plataforma 9


        ]

        self.player = Player(self.window, self.plataformas)
        self.inimigos = [
            Enemy(self.window, 600, WIN_HEIGHT - 134, 700, 2, True),
            Enemy(self.window, 300, WIN_HEIGHT - 134, 700, 3),
            Enemy(self.window, 180, WIN_HEIGHT - 310, 150, 3),
            Enemy(self.window, 700, WIN_HEIGHT - 540, 150, 3),
        ]

        # No __init__ após self.player
        self.papeis = [
            Paper(self.window, 24, 280),  # posição 1
            Paper(self.window, 760, 140),  # posição 2
            Paper(self.window, 730, 545),  # posição 3
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
            self.window.blit(self.heart_img, (WIN_WIDTH - 170 + i * 55, 10))

        papeis_coletados = sum(1 for p in self.papeis if p.coletado)
        self.window.blit(self.paper_hud, (WIN_WIDTH - 70, 60))
        fonte = pygame.font.SysFont("Lucida Sans Typewriter", 22)
        txt = fonte.render(f"{papeis_coletados}/3", True, (255, 255, 255))
        self.window.blit(txt, (WIN_WIDTH - 40, 63))

    def run(self):
        while True:
            # Fundo
            self.window.blit(self.fundo, (0, 0))

            # Plataformas
            self.desenhar_plataformas()
            self.desenhar_hud()

            # Desenha torre
            self.window.blit(self.torre_img, self.torre_rect)

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
            papeis_coletados = sum(1 for p in self.papeis if p.coletado)
            if self.player.rect.colliderect(self.torre_colisao) and papeis_coletados == 3:
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