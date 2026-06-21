import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from code.Const import WIN_WIDTH, WIN_HEIGHT, COR_AMARELO, COR_BRANCO, COR_PRETO, HISTORIA

class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load("./assets/scenario/menu.png")
        self.surf = pygame.transform.scale(self.surf, (WIN_WIDTH, WIN_HEIGHT))
        self.rect = self.surf.get_rect()

    def run(self):
        pygame.mixer.music.load("./assets/sound/menu.mp3")
        pygame.mixer.music.play(-1)

        botao = pygame.Rect(WIN_WIDTH // 2 - 100, 490, 200, 55)

        while True:
            # 1. Fundo
            self.window.blit(source=self.surf, dest=self.rect)

            # 2. Título
            self.menu_text(90, "The Cromenockle", COR_AMARELO, (WIN_WIDTH / 2, 140))
            self.menu_text(60, "A D V E N T U R E S", COR_AMARELO, (WIN_WIDTH / 2, 190))

            # 3. História
            y = 240
            for linha in HISTORIA:
                self.menu_text(20, linha, COR_BRANCO, (WIN_WIDTH / 2, y), italic=True)
                y += 28

            # 4. Controles
            self.menu_text(25, "CONTROLES", COR_AMARELO, (WIN_WIDTH / 2, 400))
            self.menu_text(20, "<- -> (Mover)       ESPAÇO (Pular)       ESC (Sair)", COR_BRANCO, (WIN_WIDTH / 2, 435))

            # 5. Botão INICIAR com hover
            mouse_pos = pygame.mouse.get_pos()
            hover = botao.collidepoint(mouse_pos)
            cor_botao = COR_AMARELO if hover else COR_BRANCO
            pygame.draw.rect(self.window, cor_botao, botao, border_radius=8)
            pygame.draw.rect(self.window, COR_PRETO, botao, 2, border_radius=8)
            self.menu_text(32, "INICIAR", COR_PRETO, botao.center)

            # 6. Atualiza tela
            pygame.display.flip()

            # 7. Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        return "iniciar"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if botao.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        return "iniciar"

    def menu_text(self, text_size: int, text: str, text_color: tuple,
                  text_center_pos: tuple, italic=False):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter",
                                              size=text_size, italic=italic)
        # Sombra preta
        sombra_surf: Surface = text_font.render(text, True, COR_PRETO).convert_alpha()
        sombra_rect: Rect = sombra_surf.get_rect(center=(text_center_pos[0] + 2, text_center_pos[1] + 2))
        self.window.blit(source=sombra_surf, dest=sombra_rect)
        # Texto principal
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)