# MOVIMENTACAO DO GORDO
import pygame, sys
from pygame.locals import QUIT, KEYDOWN

clock = pygame.time.Clock()
parado = True
run_animation = False
pulando = False
altura = -5
posicaoSheet = 0
pos_x = 0
pos_y = 0
curr_frame = 0
anim_time = 0

pygame.init()  # ← MOVIDO PARA ANTES DO image.load

frames_parado = []
for i in range(1, 5):
    frames_parado.append(pygame.image.load(f'pasta_hero/gordo_0{i}.png'))

frames_correndo = []
for i in range(5, 14):
    frames_correndo.append(pygame.image.load(f'pasta_hero/gordo_0{i}.png'))

flip_parado = []
for f in frames_parado:
    flip_parado.append(pygame.transform.flip(f, True, False))

flip_correndo = []
for f in frames_correndo:
    flip_correndo.append(pygame.transform.flip(f, True, False))
virado = False
gordo_frames = frames_parado

screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption('Movimentação personagem')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_a:
                virado = True
            if event.key == pygame.K_d:
                virado = False
            if event.key == pygame.K_SPACE and pulando == False:
                pulando = True
                altura = -5

    clock.tick(60)
    dt = clock.get_time()
    keys = pygame.key.get_pressed()

    run_animation = False  # ← RESET a cada frame antes de verificar teclas

    if keys[pygame.K_d]:
        pos_x += 2
        run_animation = True
    if keys[pygame.K_a]:
        pos_x -= 2
        run_animation = True

    if not run_animation:  # ← era "else" ligado só ao K_a
        parado = True

    if run_animation:
        parado = False
        nova_lista = flip_correndo if virado else frames_correndo
        if nova_lista != gordo_frames:  # ← trocou de animação?
            curr_frame = 0              # ← reseta o frame
        gordo_frames = nova_lista
        anim_time += dt
        if anim_time / 500 > 0.3:
            curr_frame += 1
            if curr_frame >= len(gordo_frames):
                curr_frame = 0
            anim_time = 0

    if parado:
        nova_lista = flip_parado if virado else frames_parado
        if nova_lista != gordo_frames:  # ← trocou de animação?
            curr_frame = 0              # ← reseta o frame
        gordo_frames = nova_lista
        anim_time += dt
        if anim_time / 1000 > 0.3:
            curr_frame += 1
            if curr_frame >= len(gordo_frames):
                curr_frame = 0
            anim_time = 0

    screen.fill((255, 255, 255))
    screen.blit(gordo_frames[curr_frame], (pos_x, pos_y))  # ← sem crop, frame direto
    pygame.display.update()