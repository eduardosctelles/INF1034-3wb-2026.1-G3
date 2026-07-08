import pygame, sys, math, random
from pygame.locals import QUIT, KEYDOWN
clock = pygame.time.Clock()

pygame.init()
aparece = False
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
passou = False
flash_timer = 0
GROUND_Y = 515

texto = pygame.font.Font("Lato-regular.ttf", 35)
bolha = pygame.image.load("bolha_de_fala.png")
screen = pygame.display.set_mode((1280, 720))

cenarios = [pygame.transform.scale(pygame.image.load("imagem-fundo-selva.png").convert(), (1280, 720)),pygame.transform.scale(pygame.image.load("praia.jpg").convert(), (1280, 720)),pygame.transform.scale(pygame.image.load("imagem_fundo_pantano.png").convert(), (1280, 720))]
cenario = 0
background = cenarios[cenario]
fade = pygame.Surface((1280, 720))
fade.fill((0, 0, 0))

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

# ---- Cenoura (mapa 2) ----
try:
    carrot_sheet = pygame.image.load("Carrot-sheet.png").convert_alpha()
except FileNotFoundError:
    carrot_sheet = pygame.Surface((448, 384))
    carrot_sheet.fill((255, 0, 0))

carrot_walk_frames = [carrot_sheet.subsurface((coluna * 64, linha * 64, 64, 64)) for linha in range(2) for coluna in range(7)]


def criar_cenoura():
    return {"x": 900, "y": GROUND_Y, "inicio_x": 900, "distancia_maxima": 100,
            "velocidade": 2, "direcao": 1, "frame": 0, "anim_timer": 0, "viva": True}


cenoura = criar_cenoura()

# ---- Aipo (mapa 3) ----
spritesheet_aipo = pygame.image.load('AEvilery-Sheet.png')
aipo_img = pygame.transform.flip(spritesheet_aipo, True, False)
curr_frame_aipo = 0
anim_time_aipo = 0
aipos = []
aipos_spawnados = 0
LIMITE_AIPOS = 3
AIPO_TAMANHO = 48
AIPO_HITBOX = 26
AIPO_OFFSET = (AIPO_TAMANHO - AIPO_HITBOX) // 2


def aipo_hitbox(aipo_info):
    return pygame.Rect(aipo_info["x"] + AIPO_OFFSET, aipo_info["y"] + AIPO_OFFSET, AIPO_HITBOX, AIPO_HITBOX)

# ---- Presunto (mapa 3) ----
presunto_sheet = pygame.image.load("presunto.png").convert_alpha()
presunto_frames = [presunto_sheet.subsurface((col * 32, 0, 32, 32)) for col in range(3)]
presunto_frame = 0
presunto_anim_timer = 0
presunto_rect = pygame.Rect(1000, 442, 64, 64)
vitoria = False


# Variáveis de tempo (em milissegundos)
tempo_atual = 0
tempo_troca = pygame.time.get_ticks() + 2000 # Troca após 2 segundos
estado = 1 # Controla qual texto deve aparecer

fonte_de_fala = texto.render("To cheio de fome...", True, (0, 0, 0))
fonte_de_fala2 = texto.render("Não tem nada pra comer", True, (0, 0, 0))
fonte_de_fala3 = texto.render("Queria um presunto...", True, (0, 0, 0))

font_game_over = pygame.font.SysFont('Arial', 100, bold=True)
texto_game_over = font_game_over.render("HAM OVER", True, (255, 255, 255))
font_vitoria = pygame.font.SysFont('Arial', 130, bold=True)


def troca_mapa():
    global cenario, background, pos_x

    for alpha in range(0, 256, 5):
        screen.blit(background, (0, 0))
        screen.blit(gordo_frames[curr_frame], (pos_x, pos_y))
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

    cenario += 1
    if cenario >= len(cenarios):
        cenario = 0
    background = cenarios[cenario]
    pos_x = 0

    for alpha in range(255, -1, -5):
        screen.blit(background, (0, 0))
        screen.blit(gordo_frames[curr_frame], (pos_x, pos_y))
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)


def atualiza_cenoura():
    global game_over

    if not cenoura["viva"]:
        return

    cenoura["x"] += cenoura["velocidade"] * cenoura["direcao"]
    if cenoura["x"] >= cenoura["inicio_x"] + cenoura["distancia_maxima"]:
        cenoura["direcao"] = -1
    elif cenoura["x"] <= cenoura["inicio_x"] - cenoura["distancia_maxima"]:
        cenoura["direcao"] = 1

    cenoura["anim_timer"] += 1
    if cenoura["anim_timer"] >= 5:
        cenoura["anim_timer"] = 0
        cenoura["frame"] = (cenoura["frame"] + 1) % len(carrot_walk_frames)

    cenoura_rect = pygame.Rect(cenoura["x"], cenoura["y"], 64, 64)
    player_rect = pygame.Rect(pos_x, pos_y, 64, 64)
    if player_rect.colliderect(cenoura_rect):
        game_over = True


def desenha_cenoura():
    if not cenoura["viva"]:
        return
    frame_img = pygame.transform.scale(carrot_walk_frames[cenoura["frame"]], (128, 128))
    center_x = cenoura["x"] + 32
    center_y = cenoura["y"] + 32
    screen.blit(frame_img, (center_x - 64, center_y - 64))


def atualiza_aipos():
    global curr_frame_aipo, anim_time_aipo, game_over, aipos_spawnados

    for aipo_info in aipos:
        aipo_info["x"] -= 3
    aipos[:] = [a for a in aipos if a["x"] > -32]
    if aipos_spawnados < LIMITE_AIPOS and (len(aipos) == 0 or aipos[-1]["x"] < 300):
        aipos.append({"x": 1280, "y": GROUND_Y})
        aipos_spawnados += 1

    anim_time_aipo += dt
    if anim_time_aipo / 300 > 0.3:
        curr_frame_aipo += 1
        if curr_frame_aipo > 10:
            curr_frame_aipo = 0
        anim_time_aipo = 0

    player_rect = pygame.Rect(pos_x, pos_y, 64, 64)
    for aipo_info in aipos:
        aipo_rect = aipo_hitbox(aipo_info)
        if player_rect.colliderect(aipo_rect):
            game_over = True


def desenha_aipos():
    for aipo_info in aipos:
        origem = (32 * (curr_frame_aipo % 13) + 64, 0, 32, 32)
        frame_img = pygame.transform.scale(aipo_img.subsurface(origem), (AIPO_TAMANHO, AIPO_TAMANHO))
        screen.blit(frame_img, (aipo_info["x"], aipo_info["y"]))


def atualiza_presunto():
    global presunto_frame, presunto_anim_timer
    presunto_anim_timer += dt
    if presunto_anim_timer >= 200:
        presunto_anim_timer = 0
        presunto_frame = (presunto_frame + 1) % len(presunto_frames)


def desenha_presunto():
    frame_img = pygame.transform.scale(presunto_frames[presunto_frame], (96, 96))
    center_x = presunto_rect.x + 32
    center_y = presunto_rect.y + 32
    screen.blit(frame_img, (center_x - 48, center_y - 48))


def registrar_vitoria():
    try:
        arquivo = open("contagem_vitorias.txt", "r")
        contagem = int(arquivo.read().strip())
        arquivo.close()
    except (FileNotFoundError, ValueError):
        contagem = 0

    contagem += 1
    arquivo = open("contagem_vitorias.txt", "w")
    arquivo.write(str(contagem))
    arquivo.close()


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
    old_pos_x = pos_x

    screen.fill((255, 255, 255))

    tempo_atual = pygame.time.get_ticks()
    #coisa da bolha do personagem
    if dt == 16:
        aparece = True

    if not game_over and not vitoria:
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
            nova_lista = flip_correndo if virado else frames_correndo
            if nova_lista != gordo_frames:
                curr_frame = 0
            gordo_frames = nova_lista
            anim_time += dt
            if anim_time >= 150:
                curr_frame = (curr_frame + 1) % len(gordo_frames)
                anim_time = 0
        if not run_animation and not soco:
            nova_lista = flip_parado if virado else frames_parado
            if nova_lista != gordo_frames:
                curr_frame = 0
            gordo_frames = nova_lista
            anim_time += dt
            if anim_time >= 300:
                curr_frame = (curr_frame + 1) % len(gordo_frames)
                anim_time = 0
        if soco:
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
                    if cenario == 0:
                        tom_rect = pygame.Rect(tom_x, tom_y, tom_w, tom_h)
                        if colider_soco.colliderect(tom_rect) and tom_alive:
                            tom_alive = False
                            tom_morto_por_soco = True
                    if cenario == 1 and cenoura["viva"]:
                        cenoura_rect = pygame.Rect(cenoura["x"], cenoura["y"], 64, 64)
                        if colider_soco.colliderect(cenoura_rect):
                            cenoura["viva"] = False
                    if cenario == 2:
                        aipos[:] = [a for a in aipos if not colider_soco.colliderect(aipo_hitbox(a))]
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
        if cenario == 0 and tom_alive and not tom_morto_por_soco:
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

        if cenario == 1:
            atualiza_cenoura()

        if cenario == 2:
            atualiza_aipos()
            atualiza_presunto()
            if pygame.Rect(pos_x, pos_y, 64, 64).colliderect(presunto_rect):
                if not vitoria:
                    registrar_vitoria()
                vitoria = True

    #Colider do personagem com a parede da esquerda
    if pos_x < 0:
        pos_x = old_pos_x

    if pos_x + 64 >= 1280:
        troca_mapa()

    screen.blit(background, (0, 0))
    screen.blit(gordo_frames[curr_frame], (pos_x, pos_y))

    if pos_x < 300 and passou == False and aparece == True:
        screen.blit(bolha, (pos_x, pos_y - 300))
    elif pos_x >= 300:
        passou = True

    if cenario == 0 and tom_alive:
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

    if cenario == 1:
        desenha_cenoura()

    if cenario == 2:
        desenha_aipos()
        desenha_presunto()

    if game_over:
        flash_timer += dt
        alpha = 180 + int(60 * math.sin(flash_timer / 150))
        overlay = pygame.Surface((1280, 720))
        overlay.fill((255, 0, 0))
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        texto_rect = texto_game_over.get_rect(center=(640, 360))
        screen.blit(texto_game_over, texto_rect)
    elif vitoria:
        texto_vitoria = font_vitoria.render("VITÓRIA!", True, (255, 255, 0))
        texto_vitoria_rect = texto_vitoria.get_rect(center=(640, 360))
        screen.blit(texto_vitoria, texto_vitoria_rect)
        
    if pos_x < 300 and passou == False:
        if estado == 1:
            screen.blit(fonte_de_fala, (pos_x + 115, 360))
            if tempo_atual >= tempo_troca:
                estado = 2
                tempo_troca = tempo_atual + 2000 # Próxima troca em 2 segundos
        elif estado == 2:
            screen.blit(fonte_de_fala2, (pos_x + 70, 360))
            if tempo_atual >= tempo_troca:
                estado = 3
                tempo_troca = tempo_atual + 2000 # Retorna ao primeiro após 2 segundos
        elif estado == 3:
            screen.blit(fonte_de_fala3, (pos_x + 95, 360))
            if tempo_atual >= tempo_troca:
                estado = 1
                tempo_troca = tempo_atual + 2000

    pygame.display.update()