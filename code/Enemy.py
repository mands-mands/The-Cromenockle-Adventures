import pygame
from code.Const import WIN_WIDTH, WIN_HEIGHT

class Enemy:
    def __init__(self, window, x, y, alcance=400, vel_x=2, virado=False):
        self.window = window
        self.x = float(x)
        # Carrega sprite sheet
        self.sheet = pygame.image.load("./assets/sprites/ghost.png").convert_alpha()
        self.rect_dano = pygame.Rect(x + 25, y + 25, 30, 35)  # retângulo menor no centro

        # Tamanho de cada frame
        self.frame_w = 64
        self.frame_h = 64

        # Animações
        self.animacoes = {
            'idle':   list(range(0, 4)),    # frames 0 a 3
            'move':   list(range(4, 8)),    # frames 4 a 7
            'attack': list(range(13, 16)),  # frames 13 a 15
            'hit':    list(range(20, 22)),  # frames 20 a 21
        }

        # Estado
        self.estado = 'move'
        self.frame_atual = 0
        self.frame_timer = 0
        self.frame_velocidade = 10

        # Posição e movimento
        self.rect = pygame.Rect(x, y, 64, 64)
        self.virado = virado
        self.vel_x = vel_x

        if virado:
            self.vel_x = -abs(vel_x)
        else:
            self.vel_x = abs(vel_x)

            # Limite de patrulha (anda 150px pra cada lado)
        self.origem_x = x
        self.alcance = alcance

        # Ataque
        self.atacando = False
        self.ataque_timer = 0

    def get_frame(self):
        frames = self.animacoes[self.estado]
        idx = frames[self.frame_atual % len(frames)]
        frame = self.sheet.subsurface((idx * self.frame_w, 0, self.frame_w, self.frame_h))
        frame = pygame.transform.scale(frame, (80, 80))
        if self.virado:
            frame = pygame.transform.flip(frame, True, False)
        return frame

    def animar(self):
        self.frame_timer += 1
        if self.frame_timer >= self.frame_velocidade:
            self.frame_timer = 0
            frames = self.animacoes[self.estado]
            self.frame_atual = (self.frame_atual + 1) % len(frames)

    def mover(self):
        if self.atacando:
            return

        self.x += self.vel_x
        self.rect.x = int(self.x)

        # Inverte direção ao atingir o limite
        if self.rect.x >= min(self.origem_x + self.alcance, WIN_WIDTH - self.rect.width):
            self.vel_x = -abs(self.vel_x)
            self.virado = True

        elif self.rect.x <= max(self.origem_x - self.alcance, 0):
            self.vel_x = abs(self.vel_x)
            self.virado = False

    def verificar_ataque(self, player_rect):
        distancia = abs(self.rect.centerx - player_rect.centerx)
        if distancia < 2 and abs(self.rect.centery - player_rect.centery) < 2:
            if not self.atacando:
                self.atacando = True
                self.estado = 'attack'
                self.ataque_timer = 0
                return True
        return False

    def update(self, player_rect):
        self.mover()
        self.verificar_ataque(player_rect)
        self.rect_dano.centerx = self.rect.centerx
        self.rect_dano.centery = self.rect.centery

        # Para de atacar após a animação completar
        if self.atacando:
            self.ataque_timer += 1
            if self.ataque_timer > 60:
                self.atacando = False
                self.estado = 'move'

        self.animar()

    def draw(self):
        frame = self.get_frame()
        self.window.blit(frame, (self.rect.x, self.rect.y))