# MOVIMENTACAO DO GORDO

import pygame, sys
from pygame.locals import QUIT,KEYDOWN

clock = pygame.time.Clock()

parado = True
run_animation= False
pulando = False

altura = -5
posicaoSheet = 0
pos_x = 0
pos_y = 0
curr_frame = 0
anim_time = 0
spritesheet = pygame.image.load('gordo.png')
flip = pygame.transform.flip(spritesheet,True,False)
gordo = spritesheet

pygame.init()
screen = pygame.display.set_mode((700,500))
pygame.display.set_caption('Movimentação personagem')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_a: #Mudar a direção do boneco se for para a esquerda ( ele olha pra esquerda )
                gordo = flip
            if event.key == pygame.K_d: #Muda a direção de volta dse ele tiver olhando pro outro lado
                gordo = spritesheet
            if event.key == pygame.K_SPACE and pulando == False: #Espaço pra pular / nao pode fazer double jump
                pulando = True
                altura = -5 #altura do pulo

    clock.tick(60)
    dt = clock.get_time()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]: #D para ir pra direita
        pos_x+=2
        run_animation = True
    
    if keys[pygame.K_a]: #A para ir pra esquerda
        pos_x-=2
        run_animation = True
    
    else: # Se não tá indo pra direita ou esquerda, ele ta parado
        parado = True
    

    if run_animation: #animação pra correr
        parado = False
        posicaoSheet = 192
        
        anim_time+=dt
        anim_time_sec = anim_time/500
        if anim_time_sec > 0.3:
            curr_frame+=1
            if curr_frame > 10:
                curr_frame = 0
                run_animation = False
            anim_time = 0  
    
    if pulando: # animação do pulo
        pos_y += altura #posição recebe a "altura"/velocidade que no inicio é negativa, então ela vai diminuindo cada vez mais
        altura += 0.5 #enquanto os frames passam, a altura vai aumentando de valor, uma hora ela vira positiva
                    # de 0.5 em 0.5, a altura aumenta e se adiciona a pos_y, o que faz com q ela aumente tbm chegando até 0
    if pos_y >= 0: # quando pos_y = 0 = chao, o pulo acaba
        pos_y = 0
        pulando = False
    
    if parado: #parado, animação parada
        posicaoSheet=0
        #mudar a posição na sheet pra onde ele tem a animacao dele parado
        anim_time+=dt
        anim_time_sec = anim_time/1000
        if anim_time_sec > 0.3:
            curr_frame+=1
            if curr_frame > 3:
                curr_frame = 0
                run_animation = False
            anim_time = 0    
            
    #Desenho dos elementos 
    screen.fill((255,255,255))

    screen.blit(gordo,(pos_x,pos_y),(72*(curr_frame%3),posicaoSheet,60,60))
    
    pygame.display.update()