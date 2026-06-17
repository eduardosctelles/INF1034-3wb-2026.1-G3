import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Cenoura Giratória")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 55)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(400, 500))
        
        # Física e Movimentação
        self.velocidade_x = 5
        self.velocidade_y = 0
        self.gravidade = 0.8
        self.forca_pulo = -15
        self.no_chao = False
        self.vivo = True

    def update(self):
        if not self.vivo:
            return

        keys = pygame.key.get_pressed()
        
        # Andar para a esquerda e direita
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade_x
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade_x

        # Pular
        if keys[pygame.K_SPACE] and self.no_chao: # Ou K_UP
            self.velocidade_y = self.forca_pulo
            self.no_chao = False

        # Gravidade
        self.velocidade_y += self.gravidade
        self.rect.y += self.velocidade_y

        # Colisão com o chão
        if self.rect.bottom >= 550:
            self.rect.bottom = 550
            self.velocidade_y = 0
            self.no_chao = True

        # Limites da tela
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > 800: self.rect.right = 600

class Carrot(pygame.sprite.Sprite):
    def __init__(self, x_inicial):
        super().__init__()
        try:
            self.sheet = pygame.image.load("Carrot-sheet.png").convert_alpha()
        except FileNotFoundError:
            # Fallback caso a imagem não seja encontrada para rodar o código
            self.sheet = pygame.Surface((50, 50))
            self.sheet.fill(255, 0, 0) 
        
        # Configurações da Spritesheet
        self.sprite_width = 64   # Ajuste para a largura do seu frame
        self.sprite_height = 64  # Ajuste para a altura do seu frame
        self.image = self.sheet.subsurface((0, 0, self.sprite_width, self.sprite_height))
        self.image = pygame.transform.scale(self.image, (128, 128))
        
        self.rect = self.image.get_rect(topleft=(x_inicial, 500))

        walk_frames = []
        
        for linha in range(2):
            for coluna in range(7):
                frame = self.sheet.subsurface(
                    (coluna * 64, linha * 64, 64, 64)
                )
                walk_frames.append(frame)
        
        spin_frames = []

        for linha in [2, 3]:
            for coluna in range(7):
                frame = self.sheet.subsurface(
                    (coluna * 64, linha * 64, 64, 64)
                )
                spin_frames.append(frame)
        
        death_frames = []

        for coluna in range(7):
                frame = self.sheet.subsurface(
                    (coluna * 64, 5 * 64, 64, 64)
                )
                death_frames.append(frame)
        
        # Movimentação da Cenoura
        self.inicio_x = x_inicial
        self.distancia_maxima = 100 # Distância curta que ele anda de um lado pro outro
        self.velocidade = 2
        self.direcao = 1 # 1 = direita, -1 = esquerda
        
    def update(self):
        # Lógica de andar de um lado para outro
        self.rect.x += self.velocidade * self.direcao
        if self.rect.x >= self.inicio_x + self.distancia_maxima:
            self.direcao = -1
        elif self.rect.x <= self.inicio_x - self.distancia_maxima:
            self.direcao = 1

        

# Configurações Iniciais
def resetar_jogo():
    global player, carrot, grupo_sprites
    player = Player()
    carrot = Carrot(500)
    grupo_sprites = pygame.sprite.Group()
    grupo_sprites.add(player)
    grupo_sprites.add(carrot)

resetar_jogo()

# Loop Principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Resetar o jogo caso aperte R
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not player.vivo:
                resetar_jogo()

    if player.vivo:
        grupo_sprites.update()

        # Detecção de colisão entre o Personagem e o Carrot
        if player.rect.colliderect(carrot.rect):
            if player.velocidade_y > 0 and player.rect.bottom <= carrot.rect.bottom:
                carrot.kill()
                player.velocidade_y = -10
            else:
                carrot.iniciar_ataque()
                player.vivo = False

    screen.fill((0, 0, 0))
    
    pygame.draw.rect(screen, (255, 255, 255), (0, 550, 800, 50))

    grupo_sprites.draw(screen)

    # Exibe Game Over
    if not player.vivo:
        texto_morte = fonte.render("VOCE MORREU - APERTE R", True, 255, 0, 0)
        texto_rect = texto_morte.get_rect(center=(400, 200))
        screen.blit(texto_morte, texto_rect)

    pygame.display.flip()
    clock.tick(60)
