import pygame
import math
import random

pygame.init()

# ==========================
# CONFIG
# ==========================

WIDTH = 1280
HEIGHT = 720

GROUND_Y = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tomate Explosivo")

clock = pygame.time.Clock()

# ==========================
# TOMATE SPRITESHEET
# ==========================

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

# Apenas a linha 5
for col in range(4):
    frame = get_tomato_frame(col, 5)

    if frame.get_bounding_rect().width > 0:
        explosion_frames.append(frame)

print("Frames da explosão:", len(explosion_frames))

# ==========================
# GORDO SPRITESHEET
# ==========================

player_sheet = pygame.image.load("gordo.png").convert_alpha()

PLAYER_FRAME_W = 74
PLAYER_FRAME_H = 96

WALK_FRAMES = 6 
DEATH_FRAMES = 10

def get_player_frame(col, row):

    frame = pygame.Surface(
        (PLAYER_FRAME_W, PLAYER_FRAME_H),
        pygame.SRCALPHA
    )

    frame.blit(
        player_sheet,
        (0, 0),
        (
            col * PLAYER_FRAME_W,
            row * PLAYER_FRAME_H,
            PLAYER_FRAME_W,
            PLAYER_FRAME_H
        )
    )

    return frame

walk_frames = []

for col in range(WALK_FRAMES):
    walk_frames.append(
        get_player_frame(col, 0)
    )

death_frames = []

for col in range(DEATH_FRAMES):
    death_frames.append(
        get_player_frame(col, 2)
    )

# ==========================
# PLAYER
# ==========================

class Player:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 60, 80)

        self.speed = 6

        self.vel_y = 0

        self.gravity = 0.8
        self.jump_force = -15

        self.on_ground = False

        self.dead = False

        self.direction = 1

        self.frame = 0
        self.anim_timer = 0

        self.death_frame = 0

    def update(self):

        if self.dead:

            self.anim_timer += 1

            if self.anim_timer >= 8:

                self.anim_timer = 0

                if self.death_frame < len(death_frames) - 1:
                    self.death_frame += 1

            return

        keys = pygame.key.get_pressed()

        moving = False

        if keys[pygame.K_a]:

            self.rect.x -= self.speed
            self.direction = -1
            moving = True

        if keys[pygame.K_d]:

            self.rect.x += self.speed
            self.direction = 1
            moving = True

        if keys[pygame.K_SPACE] and self.on_ground:

            self.vel_y = self.jump_force
            self.on_ground = False

        self.vel_y += self.gravity

        self.rect.y += self.vel_y

        if self.rect.bottom >= GROUND_Y:

            self.rect.bottom = GROUND_Y
            self.vel_y = 0
            self.on_ground = True

        if moving:

            self.anim_timer += 1

            if self.anim_timer >= 6:

                self.anim_timer = 0
                self.frame = 0

        else:

            self.frame = 0

    def draw(self, screen):

        if self.dead:

            frame = death_frames[
                min(
                    self.death_frame,
                    len(death_frames)-1
                )
            ]

        else:

            frame = walk_frames[self.frame]

        frame = pygame.transform.scale(
            frame,
            (90, 120)
        )

        if self.direction == -1:

            frame = pygame.transform.flip(
                frame,
                True,
                False
            )

        screen.blit(
            frame,
            (
                self.rect.centerx - 45,
                self.rect.centery - 60
            )
        )

# ==========================
# TOMATE
# ==========================

class Tomato:

    def __init__(self, x, y):

        self.shake_x = 0
        self.shake_y = 0

        self.rect = pygame.Rect(x, y, 64, 64)

        self.start_x = x

        self.speed = 2

        self.direction = 1

        self.patrol_distance = 100

        self.alive = True

        self.countdown_started = False

        self.countdown = 120

        self.exploding = False

        self.idle_frame = 0
        self.idle_timer = 0

        self.explosion_frame = 0
        self.explosion_timer = 0

        self.explosion_radius = 140

    def update(self, player):

        if not self.alive:
            return

        if not self.countdown_started:

            self.rect.x += self.speed * self.direction

            if self.rect.x > self.start_x + self.patrol_distance:
                self.direction = -1

            if self.rect.x < self.start_x - self.patrol_distance:
                self.direction = 1

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
            # tremor
            self.shake_x = random.randint(-3, 3)
            self.shake_y = random.randint(-2, 2)

            self.countdown -= 1

            # acelera a animação conforme a explosão se aproxima
            if self.countdown < 60:
                idle_speed = 4
            else:
                idle_speed = 8

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

    def draw(self, screen):

        if not self.alive:
            return

        if not self.exploding:

            frame = idle_frames[self.idle_frame]

            if self.direction == -1:
                frame = pygame.transform.flip(
                    frame,
                    True,
                    False
                )

            size = 200

            if self.countdown_started:

                if (self.countdown // 10) % 2 == 0:
                    size = 160

            frame = pygame.transform.scale(
                frame,
                (size, size)
            )

            screen.blit(
                frame,
                (
                    self.rect.centerx - size//2,
                    self.rect.centery - size//2
                )
            )

        else:

            frame = explosion_frames[
                min(
                    self.explosion_frame,
                    len(explosion_frames)-1
                )
            ]

            frame = pygame.transform.scale(
                frame,
                (180, 180)
            )

            screen.blit(
                frame,
                (
                    self.rect.centerx - 90,
                    self.rect.centery - 90
                )
            )

# ==========================
# OBJETOS
# ==========================

player = Player(100, 500)

tomato = Tomato(
    700,
    GROUND_Y - 64
)

font = pygame.font.SysFont(None, 50)

# ==========================
# LOOP
# ==========================

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:

                player = Player(100, 500)

                tomato = Tomato(
                    700,
                    GROUND_Y - 64
                )

    player.update()
    tomato.update(player)

    screen.fill((30, 30, 30))

    pygame.draw.rect(
        screen,
        (70, 170, 70),
        (
            0,
            GROUND_Y,
            WIDTH,
            HEIGHT - GROUND_Y
        )
    )

    tomato.draw(screen)
    player.draw(screen)

    if player.dead:

        texto = font.render(
            "VOCE MORREU - APERTE R",
            True,
            (255, 255, 255)
        )

        screen.blit(texto, (350, 80))

    pygame.display.flip()

pygame.quit()
