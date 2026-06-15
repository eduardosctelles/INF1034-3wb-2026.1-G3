import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo do Carrot")

# Cores
AZUL = (0, 0, 255)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# FPS e Relógio
FPS = 60
RELOGIO = pygame.time.Clock()

# Carregamento da fonte
FONTE = pygame.font.SysFont(None, 55)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Representação do personagem como um retângulo azul
        self.image = pygame.Surface((40, 60))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect(center=(LARGURA // 2, ALTURA - 100))
        
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
        if self.rect.bottom >= ALTURA - 50:
            self.rect.bottom = ALTURA - 50
            self.velocidade_y = 0
            self.no_chao = True

        # Limites da tela
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > LARGURA: self.rect.right = LARGURA

class Carrot(pygame.sprite.Sprite):
    def __init__(self, x_inicial):
        super().__init__()
        # Carrega o spritesheet. Substitua "Carrot-sheet.png" pelo caminho correto.
        try:
            self.sheet = pygame.image.load("Carrot-sheet.png").convert_alpha()
        except FileNotFoundError:
            # Fallback caso a imagem não seja encontrada para rodar o código
            self.sheet = pygame.Surface((50, 50))
            self.sheet.fill(VERMELHO) 
        
        # Configurações da Spritesheet
        self.sprite_width = 50   # Ajuste para a largura do seu frame
        self.sprite_height = 50  # Ajuste para a altura do seu frame
        self.image = self.sheet.subsurface((0, 0, self.sprite_width, self.sprite_height))
        
        self.rect = self.image.get_rect(topleft=(x_inicial, ALTURA - 100))
        
        # Movimentação do Carrot
        self.inicio_x = x_inicial
        self.distancia_maxima = 100 # Distância curta que ele anda de um lado pro outro
        self.velocidade = 2
        self.direcao = 1 # 1 = direita, -1 = esquerda
        
        # Estado de ataque
        self.atacando = False
        self.tempo_ataque = 0

    def update(self):
        # Lógica de andar de um lado para outro
        self.rect.x += self.velocidade * self.direcao
        if self.rect.x >= self.inicio_x + self.distancia_maxima:
            self.direcao = -1
        elif self.rect.x <= self.inicio_x - self.distancia_maxima:
            self.direcao = 1

        # Lógica de ataque e rotação (simulada mudando o estado ou frame)
        # Exemplo simples: inverte a direção ou muda para uma animação de ataque
        if self.atacando:
            self.tempo_ataque -= 1
            if self.tempo_ataque <= 0:
                self.atacando = False

    def iniciar_ataque(self):
        if not self.atacando:
            self.atacando = True
            self.tempo_ataque = 30 # Duração do ataque (em frames)

# --- Configurações Iniciais ---
def resetar_jogo():
    global player, carrot, grupo_sprites
    player = Player()
    carrot = Carrot(LARGURA // 2 + 100)
    grupo_sprites = pygame.sprite.Group()
    grupo_sprites.add(player)
    grupo_sprites.add(carrot)

resetar_jogo()

# --- Loop Principal ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Resetar o jogo caso aperte R
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not player.vivo:
                resetar_jogo()

    # Atualizações
    if player.vivo:
        grupo_sprites.update()

        # Detecção de colisão entre o Personagem e o Carrot
        if player.rect.colliderect(carrot.rect):
            # Regra: Se o personagem pular em cima do carrot (velocidade caindo/descendo)
            if player.velocidade_y > 0 and player.rect.bottom <= carrot.rect.bottom:
                carrot.kill() # O carrot "morre"
                # Joga o player pra cima (quicar)
                player.velocidade_y = -10
            else:
                # O carrot ataca e mata o player
                carrot.iniciar_ataque()
                player.vivo = False

    # Desenho
    TELA.fill(PRETO)
    
    # Chão
    pygame.draw.rect(TELA, BRANCO, (0, ALTURA - 50, LARGURA, 50))

    # Desenha todos os sprites
    grupo_sprites.draw(TELA)

    # Exibe Game Over
    if not player.vivo:
        texto_morte = FONTE.render("VOCE MORREU - APERTE R", True, VERMELHO)
        texto_rect = texto_morte.get_rect(center=(LARGURA // 2, ALTURA // 3))
        TELA.blit(texto_morte, texto_rect)

    pygame.display.flip()
    RELOGIO.tick(FPS)