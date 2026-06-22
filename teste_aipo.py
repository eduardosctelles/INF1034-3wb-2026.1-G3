import pygame, sys
from pygame.locals import QUIT,KEYDOWN

clock = pygame.time.Clock()


animation_aipo = True

posicaoSheet_aipo = 0
pos_x_aipo = 700
pos_y_aipo = 200
curr_frame_aipo = 0
anim_time_aipo = 0
spritesheet_aipo = pygame.image.load('AEvilery-Sheet.png')
flip_aipo = pygame.transform.flip(spritesheet_aipo,True,False)
aipo = flip_aipo


pygame.init()
screen = pygame.display.set_mode((700,500))
pygame.display.set_caption('teste aipo')
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pos_x_aipo -= 3

    if pos_x_aipo <= -32:
        pos_x_aipo = 732

            
    clock.tick(60)
    dt = clock.get_time()
    

    if animation_aipo :
        posicaoSheet_aipo = 0
        anim_time_aipo+=dt
        anim_time_sec_mm = anim_time_aipo/300
        if anim_time_sec_mm > 0.3:
            curr_frame_aipo+=1
            if curr_frame_aipo > 10:
                curr_frame_aipo = 0
            anim_time_aipo = 0  

          
    #Desenho dos elementos 
    screen.fill((255,255,255))

    screen.blit(aipo,(pos_x_aipo,pos_y_aipo),(32*(curr_frame_aipo%13)+64,posicaoSheet_aipo,32,32))

    pygame.display.update()