import pygame

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

cenarios = [pygame.transform.scale(pygame.image.load("imagem-fundo-selva.png").convert(), (WIDTH, HEIGHT)),pygame.transform.scale(pygame.image.load("praia.jpg").convert(), (WIDTH, HEIGHT)),pygame.transform.scale(pygame.image.load("imagem_fundo_pantano.png").convert(), (WIDTH, HEIGHT))] 
cenario = 0
background = cenarios[cenario]
player = pygame.Rect(100, 530, 50, 80)

GROUND_Y = 600
vel_y = 0
gravity = 0.5
on_ground = False

running = True

fade = pygame.Surface((WIDTH, HEIGHT))
fade.fill((0, 0, 0))


def troca_mapa():
    global cenario #muda a variavel q se encontra fora da função
    global background

    #Fade da troca de mapa para preto, efeito fade pra ficar maneiro
    for alpha in range(0, 256, 5):

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 100, 255), player)

        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))

        pygame.display.flip()
        pygame.time.delay(10)

    cenario += 1

    if cenario >= len(cenarios):
        cenario = 0

    background = cenarios[cenario]
    player.left = 0

    #Saída do fade, efeito maneiro
    for alpha in range(255, -1, -5):

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 100, 255), player)

        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))

        pygame.display.flip()
        pygame.time.delay(10)


while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player.x -= 4

    if keys[pygame.K_d]:
        player.x += 4

    if keys[pygame.K_SPACE] and on_ground:
        vel_y = -10
        on_ground = False

    vel_y += gravity
    player.y += vel_y

    if player.bottom >= GROUND_Y:
        player.bottom = GROUND_Y
        vel_y = 0
        on_ground = True

    if player.right >= WIDTH:
        troca_mapa()

    # desenho do mapa
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (0, 100, 255), player)

    pygame.display.flip()

pygame.quit()