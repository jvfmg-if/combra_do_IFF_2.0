import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo Simples - Evite o Inimigo!")

# Definir cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def LerAtual():
    atual = []
    with open("flaskr/atual.txt", "r") as archive:
        linha = archive.readline()
        nome, senha, inuteis = linha.split(",")
        atual.append((nome, senha))


    fonte = pygame.font.Font(None, 50)
    msg = fonte.render(f"{atual[0][0],atual[0][1]}", True, (0, 0, 0))

    return msg

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 60

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

        # Limitar o jogador à tela
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - 50:
            self.rect.x = SCREEN_WIDTH - 50
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > SCREEN_HEIGHT - 50:
            self.rect.y = SCREEN_HEIGHT - 50

# Classe do inimigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 50)
        self.rect.y = random.randint(0, SCREEN_HEIGHT // 2)
        self.speed_x = random.choice([-4, 4])
        self.speed_y = random.choice([-4, 4])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Inverter direção ao colidir com as bordas
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH - 50:
            self.speed_x *= -1
        if self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT - 50:
            self.speed_y *= -1

# Inicializar jogador e inimigo
player = Player()
enemy = Enemy()

# Criar grupos de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)

# Configurar o relógio para controlar FPS
clock = pygame.time.Clock()

# Loop principal do jogo
running = True
while running:
    msg = LerAtual()
    screen.blit(msg, (300, 300))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizar as posições dos sprites
    all_sprites.update()


    # Verificar colisão entre jogador e inimigo
    if pygame.sprite.collide_rect(player, enemy):
        print("Game Over!")
        running = False

    # Preencher o fundo da tela
    screen.fill(WHITE)

    # Desenhar todos os sprites
    all_sprites.draw(screen)

    # Atualizar a tela
    pygame.display.flip()
    pygame.display.update()
    # Controlar a taxa de quadros por segundo (FPS)
    clock.tick(60)

# Encerrar o Pygame
pygame.quit()