# MOVIMENTACAO DO GORDO
import pygame, sys
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP
import math 
import random

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

game_over = False
flash_timer = 0

pygame.init()

frames_parado = []
for i in range(2, 4):
    frames_parado.append(pygame.image.load(f'pasta_hero/gordo_0{i}.png'))

frames_correndo = []
for i in range(5, 14):
    frames_correndo.append(pygame.image.load(f'pasta_hero/gordo_0{i}.png'))

frames_soco = []
for i in range(14, 18):
    frames_soco.append(pygame.image.load(f'pasta_hero/gordo_0{i}.png'))

flip_parado = []
for frames in frames_parado:
    flip_parado.append(pygame.transform.flip(frames, True, False))

flip_correndo = []
for frames in frames_correndo:
    flip_correndo.append(pygame.transform.flip(frames, True, False))

flip_soco = []
for frames in frames_soco:
    flip_soco.append(pygame.transform.flip(frames, True, False))

virado = False
gordo_frames = frames_parado

screen = pygame.display.set_mode((1280, 720))
background = pygame.transform.scale(fundo, (1280, 720))
pygame.display.set_caption('Movimentação personagem')

font_game_over = pygame.font.SysFont('Arial', 100, bold=True)
texto_game_over = font_game_over.render("GAME OVER", True, (255, 255, 255))

GROUND_Y = 515

tomato_sheet = pygame.image.load("Tomato-Sheet.png").convert_alpha()

FRAME_W = 96
FRAME_H = 96


def get_tomato_frame(col, row):

    frame = pygame.Surface(
        (FRAME_W, FRAME_H),
        pygame.SRCALPHA
    )

    frame.blit(
        tomato_sheet,
        (0, 0),
        (
            col * FRAME_W,
            row * FRAME_H,
            FRAME_W,
            FRAME_H
        )
    )

    return frame


idle_frames = []

for col in range(8):
    idle_frames.append(
        get_tomato_frame(col, 0)
    )

explosion_frames = []

for col in range(4):
    frame = get_tomato_frame(col, 5)

    if frame.get_bounding_rect().width > 0:
        explosion_frames.append(frame)


class Tomato:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 64, 64)

        self.start_x = x
        self.ground_y = y

        self.speed = 2

        self.direction = 1

        self.patrol_distance = 150

        self.alive = True

        self.countdown_started = False

        self.countdown = 90

        self.exploding = False

        self.idle_frame = 0
        self.idle_timer = 0

        self.explosion_frame = 0
        self.explosion_timer = 0

        self.explosion_radius = 140

        self.morto_por_soco = False

        self.pulo_y = 0
        self.pulo_vel = -7
        self.gravidade = 0.3
        self.no_ar = False

        self.shake_x = 0
        self.shake_y = 0

    def update(self, player):

        if not self.alive:
            return

        if self.morto_por_soco:
            return

        if not self.countdown_started:

            self.rect.x += self.speed * self.direction

            if self.rect.x > self.start_x + self.patrol_distance:
                self.direction = -1

            if self.rect.x < self.start_x - self.patrol_distance:
                self.direction = 1

            if not self.no_ar:
                self.no_ar = True
                self.pulo_vel = -7

            self.pulo_vel += self.gravidade
            self.pulo_y += self.pulo_vel

            if self.pulo_y >= 0:
                self.pulo_y = 0
                self.no_ar = False

            self.rect.y = self.ground_y + self.pulo_y

        if not self.exploding:

            speed = 8

            if self.countdown_started:

                if self.countdown < 60:
                    speed = 4

                if self.countdown < 30:
                    speed = 2

            self.idle_timer += 1

            if self.idle_timer >= speed:

                self.idle_timer = 0

                self.idle_frame += 1
                self.idle_frame %= len(idle_frames)

        if not self.countdown_started:

            if self.rect.colliderect(player.rect):
                self.countdown_started = True

        if self.countdown_started and not self.exploding:
            self.shake_x = random.randint(-3, 3)
            self.shake_y = random.randint(-2, 2)

            self.countdown -= 1

            if self.countdown <= 0:

                self.exploding = True

                distancia = math.hypot(
                    player.rect.centerx - self.rect.centerx,
                    player.rect.centery - self.rect.centery
                )

                if distancia <= self.explosion_radius:
                    player.dead = True

        if self.exploding:

            self.explosion_timer += 1

            if self.explosion_timer >= 4:

                self.explosion_timer = 0
                self.explosion_frame += 1

                if self.explosion_frame >= len(explosion_frames):
                    self.alive = False

    def recebe_soco(self):
        self.alive = False
        self.morto_por_soco = True

    def draw(self, screen):

        if not self.alive:
            return

        if not self.exploding:

            frame = idle_frames[self.idle_frame]

            if self.direction == 1:
                frame = pygame.transform.flip(
                    frame,
                    True,
                    False
                )

            size = 150

            if self.countdown_started:

                if (self.countdown // 10) % 2 == 0:
                    size = 130

            frame = pygame.transform.scale(
                frame,
                (size, size)
            )

            offset_x = self.shake_x if self.countdown_started else 0
            offset_y = self.shake_y if self.countdown_started else 0

            screen.blit(
                frame,
                (
                    self.rect.centerx - size // 2 + offset_x,
                    self.rect.centery - size // 2 + offset_y
                )
            )

        else:

            frame = explosion_frames[
                min(
                    self.explosion_frame,
                    len(explosion_frames) - 1
                )
            ]

            frame = pygame.transform.scale(
                frame,
                (220, 220)
            )

            screen.blit(
                frame,
                (
                    self.rect.centerx - 110,
                    self.rect.centery - 110
                )
            )


tomato = Tomato(500, GROUND_Y)


class Player:
    def __init__(self):
        self.dead = False

    @property
    def rect(self):
        return pygame.Rect(pos_x, pos_y, 64, 64)


player = Player()

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

        if not run_animation:
            parado = True

        if run_animation and not soco:
            parado = False
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

        if parado and not soco:
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
            parado = False
            nova_lista = flip_soco if virado else frames_soco
            if nova_lista != gordo_frames:
                curr_frame = 0
            gordo_frames = nova_lista
            anim_time += dt
            if anim_time / 300 > 0.1:
                curr_frame += 1

                if curr_frame == 2:
                    alcance = 50
                    if virado:
                        colider_soco = pygame.Rect(
                            pos_x - alcance, pos_y, alcance + 64, 64
                        )
                    else:
                        colider_soco = pygame.Rect(
                            pos_x, pos_y, 64 + alcance, 64
                        )

                    if colider_soco.colliderect(tomato.rect) and tomato.alive:
                        tomato.recebe_soco()

                if curr_frame >= len(gordo_frames):
                    curr_frame = 0
                    soco = False
            anim_time = 0

           #Segunda parte do colider 
           # collider_jogador = pygame.Rect(pos_x, pos_y, 64, 64) 
           #Terceira parte do colider 
           # if collider_jogador.colliderect(collider_caixa):
           #    pos_x = old_pos_x
           #    pos_y = old_pos_y

        tomato.update(player)

        if player.dead:
            game_over = True

    screen.blit(background, (0, 0))
    screen.blit(gordo_frames[curr_frame], (pos_x, pos_y))
    tomato.draw(screen)

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