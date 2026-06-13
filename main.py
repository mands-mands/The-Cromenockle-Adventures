import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))

running = True

while running:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False

    screen.fill("black")

    pygame.display.flip()

pygame.quit()
quit()
