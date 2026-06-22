import pygame, sys, math, random
from pygame.locals import QUIT, KEYDOWN
clock = pygame.time.Clock()
pygame.init()
parado = True
run_animation = False
pulando = False
soco = False
altura = -5
pos_x = 0
pos_y = 515
curr_frame = 0
anim_time = 0
virado = False
game_over = False
flash_timer = 0
GROUND_Y = 515

fundo = pygame.image.load("imagem-fundo-selva.png")
screen = pygame.display.set_mode((1280, 720))
background = pygame.transform.scale(fundo, (1280, 720))
pygame.display.set_caption('Movimentação personagem')
frames_parado = []

for i in range(2, 4):
    frames_parado.append(pygame.image.load(f'pasta_hero/gordo_0{i}.png'))
frames_correndo = []
for i in range(5, 14):
    frames_correndo.append(pygame.image.load(f'pasta_hero/gordo_0{i}.png'))
frames_soco = []
for i in range(14, 18):
    frames_soco.append(pygame.image.load(f'pasta_hero/gordo_0{i}.png'))

flip_parado = [pygame.transform.flip(f, True, False) for f in frames_parado]
flip_correndo = [pygame.transform.flip(f, True, False) for f in frames_correndo]
flip_soco = [pygame.transform.flip(f, True, False) for f in frames_soco]

gordo_frames = frames_parado
tomato_sheet = pygame.image.load("Tomato-Sheet.png").convert_alpha()

FRAME_W = 96
FRAME_H = 96

def get_tomato_frame(col, row):
    frame = pygame.Surface((FRAME_W, FRAME_H), pygame.SRCALPHA)
    frame.blit(tomato_sheet, (0, 0), (col * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H))
    return frame

idle_frames = [get_tomato_frame(col, 0) for col in range(8)]

explosion_frames = []

for col in range(4):
    frame = get_tomato_frame(col, 5)
    if frame.get_bounding_rect().width > 0:
        explosion_frames.append(frame)

tom_x = 500
tom_y = GROUND_Y
tom_w = 64
tom_h = 64
tom_start_x = 500
tom_ground_y = GROUND_Y
tom_speed = 2
tom_direction = 1
tom_patrol_distance = 150
tom_alive = True
tom_countdown_started = False
tom_countdown = 90
tom_exploding = False
tom_idle_frame = 0
tom_idle_timer = 0
tom_explosion_frame = 0
tom_explosion_timer = 0
tom_explosion_radius = 140
tom_morto_por_soco = False
tom_pulo_y = 0
tom_pulo_vel = -7
tom_gravidade = 0.3
tom_no_ar = False
tom_shake_x = 0
tom_shake_y = 0

font_game_over = pygame.font.SysFont('Arial', 100, bold=True)
texto_game_over = font_game_over.render("HAM OVER", True, (255, 255, 255))

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
            if event.key == pygame.K_SPACE and not pulando:
                pulando = True
                altura = -5

    clock.tick(60)
    dt = clock.get_time()
    keys = pygame.key.get_pressed()

    if not game_over:
        run_animation = False
        if keys[pygame.K_d]:
            pos_x += 2
            run_animation = True
        if keys[pygame.K_a]:
            pos_x -= 2
            run_animation = True
        if keys[pygame.K_r]:
            soco = True
        if run_animation and not soco:
            parado = False
            nova_lista = flip_correndo if virado else frames_correndo
            if nova_lista != gordo_frames:
                curr_frame = 0
            gordo_frames = nova_lista
            anim_time += dt
            if anim_time >= 150:
                curr_frame = (curr_frame + 1) % len(gordo_frames)
                anim_time = 0
        if not run_animation and not soco:
            parado = True
            nova_lista = flip_parado if virado else frames_parado
            if nova_lista != gordo_frames:
                curr_frame = 0
            gordo_frames = nova_lista
            anim_time += dt
            if anim_time >= 300:
                curr_frame = (curr_frame + 1) % len(gordo_frames)
                anim_time = 0
        if soco:
            parado = False
            nova_lista = flip_soco if virado else frames_soco
            if nova_lista != gordo_frames:
                curr_frame = 0
                gordo_frames = nova_lista
                anim_time = 0
            anim_time += dt
            if anim_time >= 100:
                anim_time = 0
                curr_frame += 1
                if curr_frame == 2:
                    alcance = 50
                    if virado:
                        colider_soco = pygame.Rect(pos_x - alcance, pos_y, alcance + 64, 64)
                    else:
                        colider_soco = pygame.Rect(pos_x, pos_y, 64 + alcance, 64)
                    tom_rect = pygame.Rect(tom_x, tom_y, tom_w, tom_h)
                    if colider_soco.colliderect(tom_rect) and tom_alive:
                        tom_alive = False
                        tom_morto_por_soco = True
                if curr_frame >= len(gordo_frames):
                    curr_frame = 0
                    soco = False
                    gordo_frames = flip_parado if virado else frames_parado
        if pulando:
            pos_y += altura
            altura += 0.3
            if pos_y >= GROUND_Y:
                pos_y = GROUND_Y
                pulando = False
                altura = -5
        if tom_alive and not tom_morto_por_soco:
            if not tom_countdown_started:
                tom_x += tom_speed * tom_direction
                if tom_x > tom_start_x + tom_patrol_distance:
                    tom_direction = -1
                if tom_x < tom_start_x - tom_patrol_distance:
                    tom_direction = 1
                if not tom_no_ar:
                    tom_no_ar = True
                    tom_pulo_vel = -7
                tom_pulo_vel += tom_gravidade
                tom_pulo_y += tom_pulo_vel
                if tom_pulo_y >= 0:
                    tom_pulo_y = 0
                    tom_no_ar = False
                tom_y = tom_ground_y + tom_pulo_y
            if not tom_exploding:
                speed = 8
                if tom_countdown_started:
                    if tom_countdown < 60:
                        speed = 4
                    if tom_countdown < 30:
                        speed = 2
                tom_idle_timer += 1
                if tom_idle_timer >= speed:
                    tom_idle_timer = 0
                    tom_idle_frame = (tom_idle_frame + 1) % len(idle_frames)
            player_rect = pygame.Rect(pos_x, pos_y, 64, 64)
            tom_rect = pygame.Rect(tom_x, tom_y, tom_w, tom_h)
            if not tom_countdown_started:
                if tom_rect.colliderect(player_rect):
                    tom_countdown_started = True
            if tom_countdown_started and not tom_exploding:
                tom_shake_x = random.randint(-3, 3)
                tom_shake_y = random.randint(-2, 2)
                tom_countdown -= 1
                if tom_countdown <= 0:
                    tom_exploding = True
                    distancia = math.hypot(
                        player_rect.centerx - tom_rect.centerx,
                        player_rect.centery - tom_rect.centery
                    )
                    if distancia <= tom_explosion_radius:
                        game_over = True
            if tom_exploding:
                tom_explosion_timer += 1
                if tom_explosion_timer >= 4:
                    tom_explosion_timer = 0
                    tom_explosion_frame += 1
                    if tom_explosion_frame >= len(explosion_frames):
                        tom_alive = False

    screen.blit(background, (0, 0))
    screen.blit(gordo_frames[curr_frame], (pos_x, pos_y))
    if tom_alive:
        if not tom_exploding:
            frame = idle_frames[tom_idle_frame]
            if tom_direction == 1:
                frame = pygame.transform.flip(frame, True, False)
            size = 150
            if tom_countdown_started and (tom_countdown // 10) % 2 == 0:
                size = 130
            frame = pygame.transform.scale(frame, (size, size))
            offset_x = tom_shake_x if tom_countdown_started else 0
            offset_y = tom_shake_y if tom_countdown_started else 0
            tom_center_x = tom_x + tom_w // 2
            tom_center_y = tom_y + tom_h // 2
            screen.blit(frame, (tom_center_x - size // 2 + offset_x, tom_center_y - size // 2 + offset_y))
        else:
            frame = explosion_frames[min(tom_explosion_frame, len(explosion_frames) - 1)]
            frame = pygame.transform.scale(frame, (220, 220))
            tom_center_x = tom_x + tom_w // 2
            tom_center_y = tom_y + tom_h // 2
            screen.blit(frame, (tom_center_x - 110, tom_center_y - 110))
    if game_over:
        flash_timer += dt
        alpha = 180 + int(60 * math.sin(flash_timer / 150))
        overlay = pygame.Surface((1280, 720))
        overlay.fill((255, 0, 0))
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        texto_rect = texto_game_over.get_rect(center=(640, 360))
        screen.blit(texto_game_over, texto_rect)

    pygame.display.update()