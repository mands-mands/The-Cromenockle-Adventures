import sys
import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT

class Game:
    def __init__(self):
        pygame.init()  # inicia o pygame
        pygame.display.set_caption("The Cromenockle adventures")
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # define o tamanho da tela
        self.clock = pygame.time.Clock()  # define o fps do jogo


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)  # define o fps para 60
