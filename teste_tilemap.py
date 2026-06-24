import pygame

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load("imagem-fundo-selva.png").convert()

background = pygame.transform.scale(background,(WIDTH, HEIGHT))

player = pygame.Rect(100, 530, 50, 80)
GROUND_Y = 600
vel_y = -8
gravity = 0.5
on_ground = False
running = True
move_timer = 0

clock = pygame.time.Clock()

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

    if player.x == 1280:
        background = pygame.image.load("praia.jpg").convert()
        background = pygame.transform.scale(background,(WIDTH, HEIGHT))
        player.x = 0


    screen.blit(background, (0, 0))

    pygame.draw.rect(screen, (0, 100, 255), player)

    pygame.display.flip()

pygame.quit()
