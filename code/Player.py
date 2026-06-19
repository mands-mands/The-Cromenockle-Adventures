import pygame
from code.Const import WIN_WIDTH, WIN_HEIGHT

class Player:
    def __init__(self, window, plataformas):
        self.window = window
        self.plataformas = plataformas

        # Carrega sprite sheet
        self.sheet = pygame.image.load("./assets/sprites/ethan.png").convert_alpha()

        # Tamanho de cada frame
        self.frame_w = 32
        self.frame_h = 32

        # Animações — índices dos frames
        self.animacoes = {
            'idle':     list(range(0, 9)),    # frames 0 a 8
            'correr':   list(range(9, 15)),   # frames 9 a 14
            'pulo':     [15],                 # frame 15
            'machucado': list(range(16, 18)), # frames 16 a 17
        }

        # Estado atual
        self.estado = 'idle'
        self.frame_atual = 0
        self.frame_timer = 0
        self.frame_velocidade = 35  # troca de frame a cada 35 ticks

        # Posição e movimento
        self.rect = pygame.Rect(50, WIN_HEIGHT - 120, 32, 48)
        self.vel_x = 0
        self.vel_y = 0
        self.no_chao = False
        self.virado = False  # False = direita, True = esquerda

    def get_frame(self):
        frames = self.animacoes[self.estado]
        idx = frames[self.frame_atual % len(frames)]
        frame = self.sheet.subsurface((idx * self.frame_w, 0, self.frame_w, self.frame_h))
        # Escala pra ficar maior na tela
        frame = pygame.transform.scale(frame, (64, 64))
        if self.virado:
            frame = pygame.transform.flip(frame, True, False)
        return frame

    def animar(self):
        self.frame_timer += 1
        if self.frame_timer >= self.frame_velocidade:
            self.frame_timer = 0
            frames = self.animacoes[self.estado]
            self.frame_atual = (self.frame_atual + 1) % len(frames)

    def input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_LEFT]:
            self.vel_x = -1 if self.no_chao else -2
            self.virado = True
            if self.no_chao:
                self.estado = 'correr'
        elif keys[pygame.K_RIGHT]:
            self.vel_x = 1 if self.no_chao else 2
            self.virado = False
            if self.no_chao:
                self.estado = 'correr'
        else:
            if self.no_chao:
                self.estado = 'idle'

        if keys[pygame.K_SPACE] and self.no_chao:
            self.vel_y = -8
            self.no_chao = False
            self.estado = 'pulo'

    def fisica(self):
        # Gravidade
        self.vel_y += 0.15
        if self.vel_y > 15:
            self.vel_y = 15

        # Move horizontalmente
        self.rect.x += self.vel_x

        # Limita nas bordas da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIN_WIDTH:
            self.rect.right = WIN_WIDTH

        # Move verticalmente
        self.rect.y += int(self.vel_y)

        # Colisão com plataformas
        self.no_chao = False
        for plat in self.plataformas:
            if self.rect.colliderect(plat):
                if self.vel_y > 0:  # caindo
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.no_chao = True
                elif self.vel_y < 0:  # subindo
                    self.rect.top = plat.bottom
                    self.vel_y = 0

    def update(self):
        self.input()
        self.fisica()
        self.animar()

    def draw(self):
        frame = self.get_frame()
        self.window.blit(frame, (self.rect.x, self.rect.y))