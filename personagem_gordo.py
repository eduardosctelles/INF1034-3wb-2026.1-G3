# MOVIMENTACAO DO GORDO
import pygame, sys
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP

clock = pygame.time.Clock()
parado = True
run_animation = False
pulando = False
soco = False
altura = -5
posicaoSheet = 0
pos_x = 0
pos_y = 515
curr_frame = 0
anim_time = 0
fundo = pygame.image.load("imagem-fundo-selva.png")


pygame.init()  # ← MOVIDO PARA ANTES DO image.load

frames_parado = []
for i in range(2, 4):
    frames_parado.append(pygame.image.load(f'pasta_hero/gordo_0{i}.png'))

frames_correndo = []
for i in range(5, 14):
    frames_correndo.append(pygame.image.load(f'pasta_hero/gordo_0{i}.png'))

frames_soco = []
for i in range(14,18):
    frames_soco.append(pygame.image.load(f'pasta_hero/gordo_0{i}.png'))

flip_parado = []
for frames in frames_parado:
    flip_parado.append(pygame.transform.flip(frames, True, False))

flip_correndo = []
for frames in frames_correndo:
    flip_correndo.append(pygame.transform.flip(frames, True, False))

flip_soco = []
for frames in frames_soco:
    flip_soco.append(pygame.transform.flip(frames,True, False))

virado = False
gordo_frames = frames_parado

screen = pygame.display.set_mode((1280, 720))
background = pygame.transform.scale(fundo, (1280, 720))
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
            # if event.key == pygame.K_r:
            #     soco = True
        # if event.type == MOUSEBUTTONDOWN:
        #     if event.button == 1:
        #         soco = True

    #Primeira parte do colider
    # old_pos_x = pos_x
    # old_pos_y = pos_y

    clock.tick(60)
    dt = clock.get_time()
    keys = pygame.key.get_pressed()


    run_animation = False  

    if keys[pygame.K_d]:
        pos_x += 2
        run_animation = True
    if keys[pygame.K_a]:
        pos_x -= 2
        run_animation = True
    if keys[pygame.K_r]:
        soco = True

    if not run_animation:  
        parado = True

    if run_animation:
        parado = False
        soco = False
        nova_lista = flip_correndo if virado else frames_correndo
        if nova_lista != gordo_frames:  
            curr_frame = 0              
        gordo_frames = nova_lista
        anim_time += dt
        if anim_time / 500 > 0.3:
            curr_frame += 1
            if curr_frame >= len(gordo_frames):
                curr_frame = 0
            anim_time = 0

    if parado:
        nova_lista = flip_parado if virado else frames_parado
        if nova_lista != gordo_frames:  
            curr_frame = 0              
        gordo_frames = nova_lista
        anim_time += dt
        if anim_time / 1000 > 0.3:
            curr_frame += 1
            if curr_frame >= len(gordo_frames):
                curr_frame = 0
            anim_time = 0

    if soco:
        nova_lista = flip_soco if virado else frames_soco
        if nova_lista != gordo_frames:
            curr_frame = 0
        gordo_frames = nova_lista
        anim_time += dt
        if anim_time / 300 > 0.1:
            curr_frame += 1
            if curr_frame >= len(gordo_frames):
                curr_frame = 0
        anim_time = 0
        soco = False
        
       #Segunda parte do colider 
       # collider_jogador = pygame.Rect(pos_x, pos_y, 64, 64) 
       #Terceira parte do colider 
       # if collider_jogador.colliderect(collider_caixa):
       #    pos_x = old_pos_x
       #    pos_y = old_pos_y


    screen.blit(background, (0, 0))
    screen.blit(gordo_frames[curr_frame], (pos_x, pos_y))  
    pygame.display.update()