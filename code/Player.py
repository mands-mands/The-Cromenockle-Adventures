import pygame
from code.Const import WIN_WIDTH, WIN_HEIGHT

class Player:
    def __init__(self, window, plataformas):
        self.window = window
        self.plataformas = plataformas
        self.pos_x = 50.0

        self.vida = 3
        self.invencivel = False  # após tomar dano fica invencível por um tempo
        self.inv_timer = 0  # contador de invencibilidade
        self.morrendo = False
        self.morte_timer = 0

        self.sheet = pygame.image.load("./assets/sprites/ethan.png").convert_alpha()

        self.frame_w = 32
        self.frame_h = 32

        self.animacoes = {
            'idle':     list(range(0, 9)),
            'correr':   list(range(9, 15)),
            'pulo':     [15],
            'machucado': list(range(16, 18)),
            'morte':    [20, 21, 22]
        }

        self.estado = 'idle'
        self.frame_atual = 0
        self.frame_timer = 0
        self.frame_velocidade = 15

        self.rect = pygame.Rect(50, WIN_HEIGHT - 120, 32, 48)
        self.vel_x = 0
        self.vel_y = 0
        self.no_chao = False
        self.virado = False  # False = direita, True = esquerda

    def get_frame(self):
        frames = self.animacoes[self.estado]
        idx = frames[self.frame_atual % len(frames)]
        frame = self.sheet.subsurface((idx * self.frame_w, 0, self.frame_w, self.frame_h))

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
            self.vel_x = -2 if self.no_chao else -3
            self.virado = True
            if self.no_chao:
                self.estado = 'correr'
        elif keys[pygame.K_RIGHT]:
            self.vel_x = 2 if self.no_chao else 3
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
        self.vel_y += 0.3
        if self.vel_y > 15:
            self.vel_y = 15

        # personagem se move horizontalmente primeiro
        self.pos_x += self.vel_x
        if self.pos_x < 0:
            self.pos_x = 0
        if self.pos_x + self.rect.width > WIN_WIDTH:
            self.pos_x = WIN_WIDTH - self.rect.width
        self.rect.x = int(self.pos_x)

        # personagem se move verticalmente depois
        self.no_chao = False
        self.rect.y += int(self.vel_y)

        # colisão com plataformas
        for plat in self.plataformas:
            if self.rect.colliderect(plat):
                # Verifica de onde veio antes da colisão
                prev_bottom = self.rect.bottom - int(self.vel_y)
                prev_top = self.rect.top - int(self.vel_y)

                if prev_bottom <= plat.top + 5:  # se for em cima, fica em cima
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.no_chao = True
                elif prev_top >= plat.bottom - 5:  # se for embaixo, fica em baixo
                    self.rect.top = plat.bottom
                    self.vel_y = 0

    def tomar_dano(self):
        if not self.invencivel:
            self.vida -= 1
            self.invencivel = True
            self.inv_timer = 0
            self.frame_atual = 0
            if self.vida <= 0:
                self.morrendo = True
                self.estado = 'morte'
            else:
                self.estado = 'machucado'

    def update(self):
        if self.morrendo:
            self.morte_timer += 1
            self.animar()
            return

        self.input()
        self.fisica()

        if self.invencivel:
            self.inv_timer += 1
            self.estado = 'machucado'
            if self.inv_timer > 90:
                self.invencivel = False
                self.estado = 'idle'

        self.animar()

    def morreu(self):
        return self.morrendo and self.morte_timer > 120  

    def draw(self):
        if self.morrendo and self.morte_timer % 10 < 5:
            return
        frame = self.get_frame()
        self.window.blit(frame, (self.rect.x, self.rect.y))