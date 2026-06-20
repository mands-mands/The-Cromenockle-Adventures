import sys
import pygame
from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Menu import Menu
from code.Level import Level

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("The Cromenockle adventures")
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            menu = Menu(self.window)
            resultado = menu.run()
            if resultado == "iniciar":
                while True:
                    level = Level(self.window)
                    resultado_level = level.run()
                    if resultado_level == "game_over":
                        resultado_go = self.tela_game_over()
                        if resultado_go == "reiniciar":
                            continue  # reinicia o level sem voltar pro menu
                        else:
                            break  # volta pro menu
            clock.tick(60)

    def tela_game_over(self):
        fonte = pygame.font.SysFont("Lucida Sans Typewriter", 60, bold=True)
        fonte_sub = pygame.font.SysFont("Lucida Sans Typewriter", 25)

        botao = pygame.Rect(WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2 + 60, 300, 55)

        while True:
            self.window.fill((0, 0, 0))

            # Texto game over
            txt = fonte.render("GAME OVER", True, (255, 50, 50))
            self.window.blit(txt, (WIN_WIDTH // 2 - txt.get_width() // 2, WIN_HEIGHT // 2 - 80))

            # Botão jogar novamente com hover
            mouse_pos = pygame.mouse.get_pos()
            hover = botao.collidepoint(mouse_pos)
            cor_botao = (255, 220, 50) if hover else (255, 255, 255)
            pygame.draw.rect(self.window, cor_botao, botao, border_radius=8)
            pygame.draw.rect(self.window, (0, 0, 0), botao, 2, border_radius=8)
            btn_txt = fonte_sub.render("JOGAR NOVAMENTE", True, (0, 0, 0))
            self.window.blit(btn_txt, (botao.centerx - btn_txt.get_width() // 2,
                                       botao.centery - btn_txt.get_height() // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return "reiniciar"
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if botao.collidepoint(event.pos):
                        return "reiniciar"