import pygame, sys
from pygame.locals import QUIT,KEYDOWN

clock = pygame.time.Clock()


animation_aipo = True

posicaoSheet_aipo = 0
curr_frame_aipo = 0
anim_time_aipo = 0
spritesheet_aipo = pygame.image.load('AEvilery-Sheet.png')
flip_aipo = pygame.transform.flip(spritesheet_aipo,True,False)
aipo = flip_aipo
collider_inimigos = []
aipos = [{"x": 700, "y": 200}]


pygame.init()
screen = pygame.display.set_mode((700,500))
pygame.display.set_caption('teste aipo')
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    for aipo_info in aipos:
        aipo_info["x"] -= 3

    aipos = [a for a in aipos if a["x"] > -32]        

    if len(aipos) == 0 or aipos[-1]["x"] < 300:
        aipos.append({"x": 700,"y": 200})

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
    for aipo_info in aipos: 

        collider_aipo = pygame.Rect(aipo_info["x"],aipo_info["y"],32,32)

        pygame.draw.rect(screen,(0, 0, 255),collider_aipo,2)

        screen.blit(aipo,(aipo_info["x"], aipo_info["y"]),(32 * (curr_frame_aipo % 13) + 64,posicaoSheet_aipo,32,32))

    pygame.display.update()