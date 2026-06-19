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
        while True:
            menu = Menu(self.window)
            resultado = menu.run()
            if resultado == "iniciar":
                level = Level(self.window)
                level.run()
            pygame.display.update()
            self.clock.tick(60)