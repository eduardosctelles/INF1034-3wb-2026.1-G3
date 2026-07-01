import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))

background = pygame.image.load("imagem-fundo-selva.png").convert()

background = pygame.transform.scale(background,(1280, 720))
running = True

clock = pygame.time.Clock()

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    pygame.display.flip()

pygame.quit()
