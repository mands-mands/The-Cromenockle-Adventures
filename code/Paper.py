import pygame

class Paper:
    def __init__(self, window, x, y):
        self.window = window
        self.img = pygame.image.load("./assets/sprites/paper.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (32, 32))
        self.rect = self.img.get_rect(topleft=(x, y))
        self.coletado = False

    def draw(self):
        if not self.coletado:
            self.window.blit(self.img, self.rect)