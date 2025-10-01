#Instale as bibliotecas
#REGRA: use o comando cd flaskr pra essa pasta, aí ss vc inicia o código.
#Rode em um terminal dedicado



import pygame,sys,random
from pygame import display
from pygame.constants import MOUSEWHEEL
import webbrowser
import os
import time
import copy
from time import sleep
import requests

def chdir_bom(caminho):

  os.chdir(caminho)
  return caminho


working_directory = os.getcwd()
print(working_directory)
working_directory = chdir_bom(fr"{working_directory}/flaskr")
print(working_directory)

#Double points
double_point = bool()
double_point_active = bool()
double_point_duration = 5
momento = 0
gold_pos = ()

#Haste
haste = bool()
haste_pos = ()
haste_active = bool()
momento_haste = 0
haste_duration = 5

#Inverted
inverted = bool()
inverted_pos = ()
inverted_active = bool()
momento_inverted = 0
inverted_duration = 3

#Return by Death
return_ativado = False
special_pos = ()
pode_morrer = True
pause = bool()

def shutdown_flask():
    try:
        requests.post('http://127.0.0.1:5000/shutdown')
        print("Servidor Flask desligado com sucesso.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao tentar desligar o Flask: {e}")

#link
url = "http://127.0.0.1:5000/auth/register"

# Define as dimensões da tela (600x600)
screen = pygame.display.set_mode((600, 600))

#Variavel do placar
aba_placar = False
aba_creditos = False

# Define as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREEN2 = (67, 146, 55)
RED = (255, 0, 0)
BLUE = (0,0,255)

#Tela
pygame.display.set_caption("Snake")
screen.fill(WHITE)

#Chao da tela
chao = pygame.image.load("fundo/chaodois.png")
#Direções
up = 0
right = 1
left = 2
down = 3
stop = 4
my_direction = 4
my_direction_save = int()
old_direction = int()

#FPS
clock = pygame.time.Clock()
fps = 100
contador=0

#Carinhas da cobra
cima = pygame.image.load("carinhas/cimaa.png")
direita = pygame.image.load("carinhas/direitaa.png")
esquerda = pygame.image.load("carinhas/esquerdaa.png")
baixo = pygame.image.load("carinhas/baixoo.png")

carinha = [cima, direita, esquerda, baixo]
qual = 0
qual_save = 0
#Vericia se a cobra pode começar a se mexer
pode_comecar = False

#Tamanho
tam = 40

#Cobra
inicial = [(280,200), (280,240), (280, 280)]
cobra_save = [()]
snake_pos = inicial
cobra = pygame.image.load("cobra/cobra.png")
velocidade = 120
velocidade_save = int()
#Maçã
apple_pos_save = ()
apple_pos2_save = ()
apple_pos = ((280, 160))
apple_pos2 = apple_pos2 = (random.randint(0, 14) * tam, random.randint(0, 14) * tam)
apple = pygame.image.load("macas/pontoss.png")
apple_special = pygame.image.load("macas/pontosRaro.png")
apple_gold = pygame.image.load("macas/pontosX2.png")
apple_haste = pygame.image.load("macas/PontosHaste.png")
apple_inverted = pygame.image.load("macas/PontosInvertido.png")
especial = False
chance = int()

#Buraco
buraco = pygame.image.load("fundo/buraco.png")

#Parede
parede = pygame.image.load("paredes/paredeee.png")
cantos = [(0,0), (0,560), (560,560), (560,0)]

#EFE
#efe_pos = ((280, 160))
#efe = pygame.image.load("menu/EFE.png")

#Pontos
pontos = 0

'''#textos configuração
fonte=pygame.font.SysFont("Arial",21)
arial = pygame.font.SysFont("Arial", 21)
fonteGO = pygame.font.SysFont("Arial", 78)
fonte_placar = pygame.font.SysFont("Arial", 44)
msg_play_formatado = fonte.render("Play",False,WHITE)
msg_placar_formatado = fonte.render("Placar",False,WHITE)
msg_sair_formatado = arial.render("Sair  ",False,WHITE)
aperte_iniciar = fonte.render('Aperte a tecla W ou a Seta para Cima para iniciar',False,GREEN2)
msg_menu = fonte.render("Main menu",False,WHITE)
msg_morte = fonteGO.render("Game-Over",False,WHITE)
msg_placar = fonte_placar.render("Placar Local: ",False,WHITE)
msg_creditos_formatado=fonte.render("Credits",False,WHITE)'''



#botões
botao_play = [pygame.image.load("menu/botao_padrao.png"), pygame.image.load("menu/mouse_em_cima.png"), pygame.image.load("menu/botao_clique.png")]
estado_play = 0
botao_placar = [pygame.image.load("menu/botao_padrao.png"), pygame.image.load("menu/mouse_em_cima.png"), pygame.image.load("menu/botao_clique.png")]
estado_placar = 0
botao_sair = [pygame.image.load("menu/botao_padrao.png"), pygame.image.load("menu/mouse_em_cima.png"), pygame.image.load("menu/botao_clique.png")]
estado_sair = 0
botao_menu = [pygame.image.load("menu/botao_padrao.png"), pygame.image.load("menu/mouse_em_cima.png"), pygame.image.load("menu/botao_clique.png")]
estado_menu = 0
botao_creditos = [pygame.image.load("menu/botao_padrao.png"), pygame.image.load("menu/mouse_em_cima.png"), pygame.image.load("menu/botao_clique.png")]
estado_creditos = 0

#escudos
escudo_2x = pygame.image.load("escudos/2x.png")
escudo_haste = pygame.image.load("escudos/haste.png")
escudo_invertido = pygame.image.load("escudos/invertido.png")
escudo_reviver = pygame.image.load("escudos/reviver.png")

#piscar escudos
piscar_double_point = False
piscar_haste = False
piscar_inverted = False


#Verificações
ultimo_aviso = 0
jogo_comecou = False
pausado = False
old_direction_guardado = False
allmapa = False
allwall = False
morreu = False
pode_clicar = True
menu_morte = False
pode_botoes_menu = True

#Sons
pygame.mixer.init()
click_caminho = pygame.mixer.Sound("sons/button-click.mp3")
canal_ian = pygame.mixer.Channel(5)
#Buraco
mapa = []
wall = []

ps = []
inuteis = []
nome = str()
senha = str()
p = int()
atual = []

y_creditos = 0
superficie = pygame.Surface((600, 4100), pygame.SRCALPHA)
xx = 0
yy = 0
scroll = 0
dados = []


with open("textos/nomes.txt", "r") as arquivo:
  linhas = arquivo.readlines()
  for i in linhas:
    nome, senha, p, inuteis = i.split(",") #Ian: Se der algum erro mais pra frente, saibam que a única mod. q fiz foi ter tirado uma variavel "p"     ^daqui
    dados.append((nome,senha,int(p)))
    dados.sort(key=lambda x: x[2], reverse=True)


def linhas_varredura(tela):

  #pygame.display.update()

  largura,  altura = tela.get_size()

  tela_por_cima = pygame.Surface((largura, altura), pygame.SRCALPHA)
  tela_por_cima.fill((231, 225, 169, 15))
  #tela_por_cima.fill((255,255,255,15))

  cor_linha = (0, 0, 0, 50)

  for y in range(0, altura, 4):
    pygame.draw.line(tela_por_cima, cor_linha, (0, y), (largura, y))

  screen.blit(tela_por_cima, (0, 0))

def reinicializar(msg_morte):
  global ultimo_aviso, double_point, inverted, inverted_active, haste, haste_active, double_point_active, apple_pos2, especial, cobra_save, pontos_save, apple_pos2_save, apple_pos_save, my_direction_save, jogo_comecou, old_direction_guardado, snake_pos, apple_pos, velocidade, qual, pode_comecar, my_direction, old_direction, morreu, pontos, menu_morte, pode_botoes_menu, jogo_comecou, pausado, aba_placar, pode_botoes_menu
  if morreu:
    ultimo_aviso = 0
    preto_transparente = pygame.Surface((600,600))
    preto_transparente.set_alpha(225)
    screen.blit(preto_transparente,(0,0))
    if old_direction_guardado == False:
      old_direction = my_direction
    old_direction_guardado = True
    my_direction = stop
    apple_pos = ((240, 160))
    snake_pos = [(240,200), (240,240), (240, 280)]
    pode_comecar = False
    canal_ian.stop()
    pode_botoes_menu = False
    screen.blit(msg_morte, msg_morte.get_rect(centerx=(600//2), top=(195)))
    atual[0] = (atual[0][0], atual[0][1], pontos)

    if not menu_morte:

      pode_botoes_menu = True
      jogo_comecou = False

      pontos = 0
      double_point_active = False
      double_point = False
      inverted = False
      inverted_active = False
      especial = False
      haste = False
      haste_active = False
      pausado = False
      aba_placar = False
      pode_botoes_menu = True
      old_direction_guardado = False
      velocidade = 120
      qual = 0
      pode_comecar = False
      my_direction = stop
      morreu = False
      old_direction = int()


def cronometro(tempo, momento):

  atual = time.time() - momento

  if atual >= tempo:
    return False

#Aumenta a quantidade de casas da Snake
def aumentar():
  global ultimo_aviso,inverted, momento_inverted, inverted_active, inverted_pos, momento_haste,haste, haste_pos, haste_active, momento, gold_pos, double_point, double_point_active, qual_save, qual, special_pos, apple_pos, apple_pos2, snake_pos, pontos, velocidade, especial, cobra_save, apple_pos2_save, apple_pos_save, pontos_save, my_direction_save, return_ativado

  p = pontos

  if snake_pos[0] == apple_pos:
    aleatorio = random.randint(0, 5)
    chance = 1
    haste_chance = 2

    comer = pygame.mixer.Sound("sons/comer.mp3")
    comer.play()


    if double_point_active:
      snake_pos.append(snake_pos[-1])
      snake_pos.append(snake_pos[-1])
      pontos += 2
    else:
      snake_pos.append(snake_pos[-1])
      pontos += 1

    if aleatorio == chance:
      especial = True
      haste = False
    elif aleatorio == haste_chance:
      haste = True
      especial = False
    else:
      haste = False
      especial = False

    if pontos == p + 1:
      velocidade -= 1
    
    
    while (ultimo_aviso + 1) * 20 <= pontos:
      aviso=pygame.mixer.Sound("sons/aviso.mp3")
      aviso.play()
      ultimo_aviso += 1
    

    if velocidade < 30:
      velocidade = 30
  
    while True:
      apple_pos = (random.randint(0, 14) * tam, random.randint(0, 14) * tam)
      if apple_pos in snake_pos or apple_pos in mapa or apple_pos in wall or apple_pos in cantos:
        continue
      else:
        break


    while True:
      #apple_pos2 = (random.randint(0, 14) * tam, random.randint(0, 14) * tam)
      if apple_pos2 in snake_pos or apple_pos2 in mapa or apple_pos2 in wall or apple_pos2 in cantos:
        continue
      else:
        break

    if apple_pos == apple_pos2:
      apple_pos = (random.randint(0, 14) * tam, random.randint(0, 14) * tam)
    if apple_pos2 == apple_pos:
      apple_pos2 = (random.randint(0, 14) * tam, random.randint(0, 14) * tam)
  if snake_pos[0] == special_pos:
    special_pos = ()
    return_ativado = True
    cobra_save = copy.deepcopy(snake_pos)
    pontos_save = copy.deepcopy(pontos)
    my_direction_save = copy.deepcopy(my_direction)
    qual_save = copy.deepcopy(qual)
    apple_pos_save = copy.deepcopy(apple_pos)
    apple_pos2_save = copy.deepcopy(apple_pos2)

  if snake_pos[0] == haste_pos:
    haste_pos = ()
    print("comeu haste")

    if not haste_active:
      velocidade -= 55
      
    haste_active = True
    momento_haste = time.time()

  if snake_pos[0] == apple_pos2:
    aleatorio_ = random.randint(0, 5)
    chance_ = 1
    chance_inverted = 2

    if aleatorio_ == chance_ and double_point_active == False:
      double_point = True
      inverted = False
    elif aleatorio_ == chance_inverted:
      inverted = True
      double_point = False
    else:
      inverted = False
      double_point = False
    comer = pygame.mixer.Sound("sons/comer(02).mp3")
    comer.play()
    if double_point_active:
      snake_pos.append(snake_pos[-1])
      snake_pos.append(snake_pos[-1])
      pontos += 2
    else:
      snake_pos.append(snake_pos[-1])
      pontos += 1

    if pontos == p + 1:
      velocidade -= 1

    if velocidade < 30:
      velocidade = 30
    if pontos%20==0:
      aviso=pygame.mixer.Sound("sons/aviso.mp3")
      aviso.play()

    while True:
      apple_pos2 = (random.randint(0, 14) * tam, random.randint(0, 14) * tam)
      if apple_pos2 in snake_pos or apple_pos2 in mapa or apple_pos2 in wall or apple_pos2 in cantos:
        continue
      else:
        break

    while True:
      #apple_pos = (random.randint(0, 14) * tam, random.randint(0, 14) * tam)
      if apple_pos in snake_pos or apple_pos in mapa or apple_pos in wall or apple_pos in cantos:
        continue
      else:
        break
    if apple_pos == apple_pos2:
      apple_pos = (random.randint(0, 14) * tam, random.randint(0, 14) * tam)
    if apple_pos2 == apple_pos:
      apple_pos2 = (random.randint(0, 14) * tam, random.randint(0, 14) * tam)
  if snake_pos[0] == gold_pos:
    gold_pos = ()
    ian = pygame.mixer.Sound("sons/ian.mp3")
    if canal_ian.get_busy:
      canal_ian.stop()

    canal_ian.play(ian)
    double_point_active = True
    momento = time.time()
  
  if snake_pos[0] == inverted_pos:
    print("comeu invertido")
    inverted_pos = ()
    inverted_active = True
    momento_inverted = time.time()


#Desenha o fundo quadriculado
def quadriculado(tela_login):
  screen.fill(WHITE)
  for y in range(0, 600,80):
    pygame.draw.line(tela_login, BLACK,(300,600),(300,0),3)
    for x in range(0,600,80):
      screen.blit(chao,(x,y))
    for x in range(40,600,80):
      screen.blit(chao,(x,y+40))
    


#Posicoes buracos
def buracos():
  global mapa, buraco, allmapa

  for y in range(0,600,560):
    for x in range(0,600,80):
      if not allmapa:
        mapa.append((x,y))
        if len(mapa) >= 32:
          allmapa = True
          break
      screen.blit(buraco,(x,y))

  for x in range(0,600,560):
    for y in range(0,600,80):
      if not allmapa:
        mapa.append((x,y))
        if len(mapa) >= 32:
          allmapa = True
          break
      screen.blit(buraco, (x,y))

def placar(msg_placar,fonte):
  global aba_placar, xx, yy, scroll, superficie, dados
  txts = []

  if aba_placar:
    superficie.fill((0,0,0,0))
    superficie.blit(msg_placar, (45,40))

    for i in range(len(dados)):
      if i == 100:
        break
      txt = fonte.render(f"{i + 1}: {dados[i][0]} - {dados[i][2]}",False,WHITE)
      txts.append(txt)

    for i in range(len(txts)):
      superficie.blit(txts[i], (45, 80 + (i + 1) * 40))
    screen.blit(superficie, (xx,yy))

#Posicoes paredes
def paredes():
  global wall, parede, allwall

  for y in range(0,600,560):
    for x in range(40,600,80):
      if not allwall:
        wall.append((x,y))
        if len(wall) == 32:
          allwall = True
          break
      screen.blit(parede,(x,y))

  for x in range(0,600,560):
    for y in range(40,600,80):
      if not allwall:
        wall.append((x,y))
        if len(wall) == 32:
          allwall = True
          break
      screen.blit(parede, (x,y))
  for i in cantos:
    screen.blit(parede, i)

#Verificação dos botões
def botoes(botao, event, estado):
  global estado_sair, estado_play, estado_placar, click, estado_creditos, estado_link

  mouse_pos = pygame.mouse.get_pos()

  if botao.collidepoint(mouse_pos):
    estado = 1
  elif not botao.collidepoint(mouse_pos):
    estado = 0
  if event.type == pygame.MOUSEBUTTONDOWN:
    mouse = event.pos
    if botao.collidepoint(mouse):  
      click_caminho.play()
      estado = 2
  if event.type == pygame.MOUSEBUTTONUP:
    mouse = event.pos
    if botao.collidepoint(mouse):

      return True, estado
  return False, estado

#Verifica se a cobra colidiu com si mesma
def colisao():
  global pause, qual, qual_save, pode_morrer, morreu,menu_morte,atual,dados,pontos,especial,return_ativado,snake_pos,my_direction,cobra_save,pontos_save,my_direction_save, apple_pos, apple_pos2, apple_pos2_save, apple_pos_save

  head = snake_pos[0]

  if (head in snake_pos[1:] or head in wall[0:]) and return_ativado == False:
    morte=pygame.mixer.Sound("sons/morte.mp3")
    morte.play()
    morreu = True
    menu_morte = True

    for i in range(len(dados)):
      if dados[i][0] == atual[0][0]:
        igual = dados[i][2]
        if dados[i][2] < pontos:
          del dados[i]
          break
        elif dados[i][2] > pontos or dados[i][2] == pontos:
          pontos = igual
          del dados[i]
          break


    dados.append((atual[0][0],atual[0][1],pontos))
    dados.sort(key=lambda x: x[2], reverse=True)

    with open("textos/nomes.txt", "w") as arquivo:
      for i in range(len(dados)):
        arquivo.write(f"{dados[i][0]},{dados[i][1]},{dados[i][2]},\n")

  elif (head in snake_pos[1:] or head in wall[0:]) and return_ativado == True:
    return_ativado = False
    pontos = pontos_save
    snake_pos = cobra_save
    my_direction = my_direction_save
    qual = qual_save
    apple_pos2 = apple_pos2_save
    apple_pos = apple_pos_save
    pause = True

def caixa_texto(txt, caixa, ativo, surface, funcao):
  fonte_menor = pygame.font.SysFont("Arial", 12)
  fonte_arial = pygame.font.SysFont("Arial", 14)
  color = GREEN if ativo else (169,169,169)
  pygame.draw.rect(surface, color, caixa, 2)
  txt = fonte_arial.render(txt, False, BLACK)
  funcao = fonte_menor.render(funcao, False, BLACK)
  surface.blit(txt, (caixa.x + 5, caixa.y + 12))
  surface.blit(funcao, (caixa.x, caixa.y - 13))

def posicao_escudos():
    global double_point_active, haste_active, inverted_active, escudo_reviver
    
    efeitos = [double_point_active, haste_active, inverted_active, escudo_reviver]
    pos_escudos = [(40,40), (60,40), (80,40), (100,40)]
    
    resultado = []
    pos_index = 0
    
    for efeito in efeitos:
        if efeito:
            resultado.append(pos_escudos[pos_index])
            pos_index += 1  
    
    return resultado



def escudos_draw():
    global piscar_double_point, piscar_haste, piscar_inverted
    global double_point_active, haste_active, inverted_active, return_ativado
    global escudo_2x, escudo_haste, escudo_invertido, escudo_reviver

    efeitos = [double_point_active, haste_active, inverted_active, return_ativado]
    sprites = [escudo_2x, escudo_haste, escudo_invertido, escudo_reviver]
    piscar_flags = [piscar_double_point, piscar_haste, piscar_inverted, False]  # o último sempre pode piscar
    posicoes = posicao_escudos()  
    tempo = pygame.time.get_ticks()
    piscar = (tempo // 200) % 2 == 0

    pos_index = 0
    for efeito, sprite, pode_piscar in zip(efeitos, sprites, piscar_flags):
        if efeito:
            if pode_piscar:  # só pisca se permitido pela flag
                if piscar:
                    screen.blit(sprite, posicoes[pos_index])
            else:
                screen.blit(sprite, posicoes[pos_index])  # sempre desenha se não pode piscar
            pos_index += 1




usuario = "Insira seu nome"
senha_txt = "Insira sua senha. Obs.: Segure CTRL para ver a senha"
entrar = 'ENTRAR'
txt1 = ''
txt2 = ''
txt22 = ''
log_in = "LOGIN"
sign_up = "REGISTER"
ativo1 = False
ativo2 = False
cima_botao = False
b = False


tela = True
def jogo():
  global piscar_double_point, piscar_haste, piscar_inverted, momento_inverted, inverted, inverted_active, apple_inverted, inverted_pos, haste, haste_active, haste_duration, apple_haste, haste_pos, double_point_active, double_point_duration, momento, gold_pos, apple_gold, pause, special_pos, especial, apple_pos2_save, return_ativado, apple_pos_save, cobra_save, pontos_save, my_direction_save, ativo4, ativo3, b, txt22, screen, aba_placar, aba_creditos, WHITE, BLACK, GREEN, GREEN2, RED, chao, up, right, left, down, stop, my_direction, old_direction, clock, fps, contador, cima, direita, esquerda, baixo, carinha, qual, pode_comecar, tam, inicial, snake_pos, cobra, velocidade, apple_pos, apple_pos2, apple, buraco, parede, cantos, pontos, otão_play, estado_play, botao_placar, estado_placar, botao_sair, estado_sair, botao_menu, estado_menu, botao_creditos, estado_creditos, jogo_comecou, pausado, old_direction_guardado, allmapa, allwall, morreu, pode_clicar, menu_morte, pode_botoes_menu, click_caminho, mapa, wall, ps, inuteis, nome, senha, p, atual, y_creditos, superficie, xx, yy, scroll, dados, usuario, senha_txt, entrar, txt1, txt2, log_in, ativo1, ativo2, cima_botao, tela

  # Inicializa o Pygame
  pygame.init()

  #fontes
  fonte=pygame.font.SysFont("Arial",21)
  arial = pygame.font.SysFont("Arial", 21)
  fonteGO = pygame.font.SysFont("Arial", 78)
  fonte_placar = pygame.font.SysFont("Arial", 44)
  msg_play_formatado = fonte.render("Play",False,WHITE)
  msg_placar_formatado = fonte.render("Placar",False,WHITE)
  msg_sair_formatado = arial.render("Sair",False,WHITE)
  aperte_iniciar = fonte.render('Aperte a tecla W ou a Seta para Cima para iniciar',False,GREEN2)
  msg_menu = fonte.render("Main menu",False,WHITE)
  msg_morte = fonteGO.render("Game-Over",False,WHITE)
  msg_placar = fonte_placar.render("Placar Local: ",False,WHITE)
  msg_creditos_formatado=fonte.render("Credits",False,WHITE)

  while tela:
    caixa1 = pygame.Rect(150,300, 300, 40)
    caixa2 = pygame.Rect(150,360, 300, 40)
    botao_entrar = pygame.Rect(150,420, 300, 40)
    botao_link= pygame.Rect(150,470,300,40)
    tela_login = pygame.Surface((600,600))
    tela_login.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()
    if botao_link.collidepoint(mouse_pos):
      pygame.draw.rect(tela_login, (128,128,128), botao_link)
    else:
      pygame.draw.rect(tela_login, (169,169,169), botao_link)
      
    if botao_entrar.collidepoint(mouse_pos):
      pygame.draw.rect(tela_login, (128,128,128), botao_entrar)
    else:
      pygame.draw.rect(tela_login, (169,169,169), botao_entrar)

    entre = fonte.render(entrar, False, WHITE)
    login = fonte_placar.render(log_in, False, BLACK)
    signup = fonte.render(sign_up, False, WHITE)
    tela_login.blit(login, (242,200))
    tela_login.blit(entre, (260, botao_entrar.y + 9))
    tela_login.blit(signup, (260, botao_link.y + 7))
    caixa_texto(txt1, caixa1, ativo1, tela_login, usuario)
    caixa_texto(txt22, caixa2, ativo2, tela_login, senha_txt)
    
    screen.blit(tela_login,(0,0))
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        shutdown_flask()
        os.system('curl -X POST http://127.0.0.1:5000/shutdown')
        os.system("exit")
        sys.exit()

      if event.type == pygame.MOUSEBUTTONUP:
        if botao_entrar.collidepoint(event.pos):
          try:
            resp = requests.post('http://127.0.0.1:5000/auth/login', data={
              'username': txt1,
              'password': txt2
            })
            if resp.ok and ('Incorrect username' not in resp.text and 'Incorrect password' not in resp.text) and txt1 != '' and txt2 != "":
              with open("textos/atual.txt", "w") as x:
                x.write(f"{txt1},{txt2},")
              tela = False
          except Exception as e:
            pass
        elif botao_link.collidepoint(event.pos):
          webbrowser.open_new_tab(url)
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN: 
          try:
            resp = requests.post('http://127.0.0.1:5000/auth/login', data={
              'username': txt1,
              'password': txt2
            })
            if resp.ok and ('Incorrect username' not in resp.text and 'Incorrect password' not in resp.text) and txt1 != '' and txt2 != "":
              with open("textos/atual.txt", "w") as x:
                x.write(f"{txt1},{txt2},")
              tela = False
          except Exception as e:
            pass
      if event.type == pygame.MOUSEBUTTONDOWN:
        if caixa1.collidepoint(event.pos):
          ativo1 = True
          ativo2 = False
          ativo3 = False
          ativo4 = False
          txt1 = ""
        elif caixa2.collidepoint(event.pos):
          ativo1 = False
          ativo2 = True
          ativo3 = False
          ativo4 = False
          txt2 = ""
          txt22 = ""
        else:
          ativo1 = False
          ativo2 = False
          ativo3 = False
          ativo4 = False

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
          if ativo1:
            ativo1 = False
            ativo2 = True
          elif ativo2:
            ativo2 = False
            ativo1 = True
          elif ativo3:
            ativo3 = False
            ativo4 = True
          elif ativo4:
            ativo4 = False
            ativo1 = True
            
        if ativo1:
          if event.key == pygame.K_BACKSPACE:
            txt1 = txt1[:-1]
          elif event.key == pygame.K_RETURN:
            ativo1 = False
          elif event.key == pygame.K_TAB:
            pass
          else:
            txt1 += event.unicode
            
            
        if ativo2:
          if event.key == pygame.K_BACKSPACE and not b:
             
              txt2 = txt2[:-1]
              x = len(txt2)
              txt22 = '*'*x
          elif event.key == pygame.K_RETURN:
              ativo2 = False
          elif event.key == pygame.K_TAB:
              pass
          elif event.key == pygame.K_LCTRL:
              txt22 = txt2
              b = True
          elif not b:
              
              txt2 += event.unicode
              x = len(txt2)
              
              
              txt22 = '*'*x
              
          elif event.key == pygame.K_LCTRL:
              txt22 = txt2
              b = True
              
      elif event.type == pygame.KEYUP:
          if event.key == pygame.K_LCTRL:
              x = len(txt2)
              txt22 = '*'*x
              b = False
          
    linhas_varredura(tela_login)
    pygame.display.update()

  with open("textos/atual.txt", "r") as archive:
    linha = archive.readline()
    nome, senha, inuteis = linha.split(",")
    atual.append((nome, senha))

  pygame.mixer.music.load("sons/elevator.mp3")
  pygame.mixer.music.play(-1)
  #Loop principal do jogo
  while True:
    if pause:
      pygame.mixer.music.pause()
      tempo=pygame.mixer.Sound("sons/VoltarNoTempo.mp3")
      tempo.play()
      time.sleep(0.60)
      pygame.mixer.music.unpause()
      pause = False
    #Atualiza o background
    quadriculado(tela_login)
    #Verificação de eventos
    for event in pygame.event.get():

      if event.type == pygame.MOUSEWHEEL:
        if aba_placar:
          scroll += event.y
          if scroll > 0:
            yy += scroll * 40
            scroll = 0
          elif scroll < 0:
            yy += scroll * 40
            scroll = 0
        if aba_creditos:
          scroll += event.y
          if scroll > 0:
            y_creditos += scroll * 40
            scroll = 0
          elif scroll < 0:
            y_creditos += scroll * 40
            scroll = 0


      if menu_morte:
        clicou_menu, estado_menu = botoes(pygame.Rect(200,360,botao_menu[estado_menu].get_width(), botao_menu[estado_menu].get_height()), event, estado_menu)
        
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            menu_morte = False

        if clicou_menu:
          menu_morte = False

      if (not aba_placar and not pausado and not jogo_comecou and not aba_creditos and not tela) or menu_morte:
        if (not aba_placar and not pausado and not jogo_comecou and not aba_creditos and not tela):
          clicou_sair, estado_sair = botoes(pygame.Rect(200,480,botao_sair[estado_sair].get_width(),botao_sair[estado_sair].get_height()), event, estado_sair)
          if clicou_sair:
            pygame.quit()

            shutdown_flask()
            os.system('curl -X POST http://127.0.0.1:5000/shutdown')
            os.system("exit")

            sys.exit()

        elif menu_morte:
          clicou_sair, estado_sair = botoes(pygame.Rect(200,400,botao_sair[estado_sair].get_width(),botao_sair[estado_sair].get_height()), event, estado_sair)
          if clicou_sair:
            pygame.quit()
            shutdown_flask()
            os.system('curl -X POST http://127.0.0.1:5000/shutdown')
            os.system("exit")
            sys.exit()

      #Chama a verificação dos botões
      if not aba_placar and not pausado and not jogo_comecou and not aba_creditos and not tela:
        clicou_placar, estado_placar = botoes(pygame.Rect(200,400,botao_placar[estado_placar].get_width(),botao_placar[estado_placar].get_height()), event, estado_placar)
        if clicou_placar:
          aba_placar = True

        clicou_play, estado_play = botoes(pygame.Rect(200,360,botao_play[estado_play].get_width(),botao_play[estado_play].get_height()), event, estado_play)
        if clicou_play:
          pode_comecar = True
          jogo_comecou = True
          velocidade = 120
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
              pode_comecar = True
              jogo_comecou = True
              velocidade = 120


        clicou_creditos, estado_creditos = botoes(pygame.Rect(200,440,botao_creditos[estado_creditos].get_width(),botao_creditos[estado_creditos].get_height()),event,estado_creditos)

        if clicou_creditos:
          aba_creditos=True


      if event.type == pygame.QUIT:
        pygame.quit()
        shutdown_flask()
        os.system('curl -X POST http://127.0.0.1:5000/shutdown')
        os.system("exit")
        sys.exit()

      #Verifica se o usuario apertou alguma tecla
      if event.type == pygame.KEYDOWN:
        if pode_comecar and pode_clicar:
          if (event.key == pygame.K_w
                or event.key == pygame.K_UP) and my_direction != down and pausado == False and not inverted_active:
            my_direction = up
            qual = 0
            pode_clicar = False
          if (event.key == pygame.K_d
                or event.key == pygame.K_RIGHT) and my_direction != left and my_direction != stop and not inverted_active:
            my_direction = right
            qual = 1
            pode_clicar = False
          if (event.key == pygame.K_a
                or event.key == pygame.K_LEFT) and my_direction != right and my_direction != stop and not inverted_active:
            my_direction = left
            qual = 2
            pode_clicar = False
          if (event.key == pygame.K_s
                or event.key == pygame.K_DOWN) and my_direction != up and my_direction != stop and not inverted_active:
            my_direction = down
            qual = 3
            pode_clicar = False
          
          if inverted_active == True:
            if (event.key == pygame.K_w
                or event.key == pygame.K_UP) and my_direction != up and pausado == False:
              my_direction = down
              qual = 3
            pode_clicar = False
            if (event.key == pygame.K_d
                or event.key == pygame.K_RIGHT) and my_direction != right and my_direction != stop:
              my_direction = left
              qual = 2
              pode_clicar = False
            if (event.key == pygame.K_a
                or event.key == pygame.K_LEFT) and my_direction != left and my_direction != stop:
              my_direction = right
              qual = 1
              pode_clicar = False
            if (event.key == pygame.K_s
                or event.key == pygame.K_DOWN) and my_direction != down and my_direction != stop:
              my_direction = up
              qual = 0
              pode_clicar = False






        if event.key == pygame.K_ESCAPE:
          if aba_placar:
            aba_placar = False
            y = 0
        if event.key == pygame.K_ESCAPE:
          if aba_creditos:
            aba_creditos=False

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_p and jogo_comecou and pausado == False:
          pausado = True

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE and jogo_comecou and pausado == True:
          pausado = False
          my_direction = old_direction


    #Movimentação
    head_x, head_y = snake_pos[0]
    head = snake_pos[0]

    if my_direction == up:
      head_y -= 40
    elif my_direction == right:
      head_x += 40
    elif my_direction == left:
      head_x -= 40
    elif my_direction == down:
      head_y += 40
    elif my_direction == stop:
      pass

    #Faz a cobra ir de um lado da tela para o outro
    if head[0] < 40:
      head_x = 520
    elif head[0] > 520:
      head_x = 40
    elif head[1] < 40:
      head_y = 520
    elif head[1] > 520:
      head_y = 40

    #Faz a movimentacao da cobra acontecer a cada loop
    old_snake = snake_pos.copy()

    for i in range(len(snake_pos)):
      if my_direction != stop:
        if i == 0:
          del snake_pos[0]
          snake_pos.insert(0, (head_x, head_y))
        elif i != 0:
          snake_pos[i] = old_snake[i-1]

    pode_clicar = True

    #Desenha os botoes se estiver no menu
    
    if not pode_comecar and pode_botoes_menu:
      screen.blit(botao_play[estado_play],(200,360))
      screen.blit(botao_placar[estado_placar],(200,400))
      screen.blit(botao_creditos[estado_creditos],(200, 440))
      screen.blit(botao_sair[estado_sair],(200, 480))

      if estado_creditos == 0 or estado_creditos == 1:
        screen.blit(msg_creditos_formatado,msg_creditos_formatado.get_rect(centerx=(600//2), top=(446)))

      elif estado_creditos == 2:
        screen.blit(msg_creditos_formatado,msg_creditos_formatado.get_rect(centerx=(600//2), top=(448)))

      if estado_sair == 0 or estado_sair == 1:
        screen.blit(msg_sair_formatado,msg_sair_formatado.get_rect(centerx=(600//2), top=(486)))
      elif estado_sair == 2:
        screen.blit(msg_sair_formatado,msg_sair_formatado.get_rect(centerx=(600//2), top=(488)))

      if estado_play == 0 or estado_play == 1:
        screen.blit(msg_play_formatado,msg_play_formatado.get_rect(centerx=(600//2),top=(366)))
      elif estado_play == 2:
        screen.blit(msg_play_formatado,msg_play_formatado.get_rect(centerx=(600//2),top=(368)))

      if estado_placar == 0 or estado_placar == 1:
        screen.blit(msg_placar_formatado,msg_placar_formatado.get_rect(centerx=(600//2),top=(406)))
      elif estado_placar == 2:
        screen.blit(msg_placar_formatado,msg_placar_formatado.get_rect(centerx=(600//2),top=(408)))

    #Desenha a "F" enquanto a cobra estiver parada
    #if my_direction == stop and pausado == False:
    #  screen.blit(efe,efe_pos)

    buracos()
    paredes()

    #Chama a funcao ja escrita antes
    #aumentar()
    colisao()

    #Desenha a cobra
    if not morreu:
      if my_direction != stop or pausado == True:
        for pos in snake_pos:
          if pos == snake_pos[0]:
            screen.blit(carinha[qual], pos)
          elif pos != snake_pos[0]:
            screen.blit(cobra, pos)
      else:
        for pos in snake_pos:
          screen.blit(cobra, pos)

    elif morreu:
      especial = False
      haste_active = False
      haste = False
      skane_pos = inicial
      my_direction = stop
      if my_direction != stop or pausado == True:
        for pos in snake_pos:
          if pos == snake_pos[0]:
            screen.blit(carinha[qual], pos)
          elif pos != snake_pos[0]:
            screen.blit(cobra, pos)
      else:
        for pos in snake_pos:
          screen.blit(cobra, pos)
    else:
      pass
    aumentar()

    piscar_double_point = double_point_active and (time.time() >= momento + double_point_duration - 1.15)
    piscar_haste        = haste_active and (time.time() >= momento_haste + haste_duration - 1.15)
    piscar_inverted     = inverted_active and (time.time() >= momento_inverted + inverted_duration - 1.15)


    if double_point_active and time.time() - momento >= double_point_duration:
      double_point_active = False
      print("acabou")

    if haste_active and time.time() - momento_haste >= haste_duration:
      haste_active = False
      velocidade += 55
      print("Haste Acabou")

    if inverted_active and time.time() - momento_inverted >= inverted_duration:
      inverted_active = False
      print("Acabou o invertido")

    #Desenha a maçã
    while True:
      if apple_pos2 in snake_pos or apple_pos2 in mapa or apple_pos2 in wall or apple_pos2 in cantos or apple_pos2 in apple_pos:
        apple_pos2 = (random.randint(0, 14) * tam, random.randint(0, 14) * tam)
        continue
      else:
        break
    while True:
      if apple_pos in snake_pos or apple_pos in mapa or apple_pos in wall or apple_pos in cantos or apple_pos in apple_pos2:
        apple_pos = (random.randint(0, 14) * tam, random.randint(0, 14) * tam)
        continue
      else:
        break

    if especial == False and haste == False:
      screen.blit(apple, apple_pos)
    elif especial == True:
      screen.blit(apple_special , apple_pos)
      special_pos = apple_pos
    elif haste == True:
      screen.blit(apple_haste , apple_pos)
      haste_pos = apple_pos

   # screen.blit(apple, apple_pos)
    #if my_direction != stop or pausado:
     # screen.blit(apple, apple_pos2)
    if my_direction != stop or pausado:
      if double_point == True:
        screen.blit(apple_gold, apple_pos2)
        gold_pos = apple_pos2
      elif inverted == True:
        screen.blit(apple_inverted, apple_pos2)
        inverted_pos = apple_pos2
      elif double_point == False and inverted == False:
        screen.blit(apple, apple_pos2)
    #Chama a função ja antes escrita


    if pode_comecar and my_direction == stop and pausado != True:
      screen.blit(aperte_iniciar,aperte_iniciar.get_rect(centerx=(600//2),top=(371)))

    if my_direction != stop:
      jogo_comecou = True

    if pausado:
      preto_transparente = pygame.Surface((600,600))
      preto_transparente.set_alpha(225)
      screen.blit(preto_transparente,(0,0))
      if old_direction_guardado == False:
        old_direction = my_direction
      old_direction_guardado = True
      my_direction = stop

    if not pausado:
      old_direction_guardado = False

    reinicializar(msg_morte)

    if menu_morte:
      screen.blit(botao_sair[estado_sair],(200, 400))

      if estado_sair == 0 or estado_sair == 1:
        screen.blit(msg_sair_formatado, msg_sair_formatado.get_rect(centerx=(600//2), top=(406)))
      elif estado_sair == 2:
        screen.blit(msg_sair_formatado,msg_placar_formatado.get_rect(centerx=(600//2),top=(408)))

    if menu_morte:
      screen.blit(botao_menu[estado_menu], (200, 360))

      if estado_menu == 0 or estado_menu == 1:
        #screen.blit(msg_menu,(242,366))
        screen.blit(msg_menu,msg_menu.get_rect(centerx=(600//2), top=(366)))
      elif estado_menu == 2:
        #screen.blit(msg_menu,(242,368))
        screen.blit(msg_menu,msg_menu.get_rect(centerx=(600//2), top=(368)))
    if aba_creditos:
      preto_transparente = pygame.Surface((600,3000))
  #adicionar creditos
      nome_jg=fonte_placar.render("Cobra do IFF",False,WHITE)
      fonte_menor = pygame.font.SysFont("Arial", 18)


      codigos=fonte.render('''Codigos em Python:''',False,WHITE)
      bd = fonte.render("Codigos em SQlite:",False,WHITE)
      graficos = fonte.render("Graficos:",False,WHITE)
      dub = fonte.render("Dublagem/Sons:", False, WHITE)
      musica = fonte.render("Musica:", False, WHITE)
      site = fonte.render(" Codigos pro site:", False, WHITE)
      
      kevin = fonte_menor.render(' "Local Forecast - Elevator" Kevin MacLeod', False, WHITE)
      creditos2=fonte_menor.render('Carlos Eduardo de Oliveira Barbosa',False,WHITE)
      creditos3=fonte_menor.render(' Ian Motta Ferreira',False,WHITE)
      creditos4=fonte_menor.render('Lucas Menezes Fasolo',False,WHITE)
      creditos5=fonte_menor.render('Ray Gomes Pereira',False,WHITE)
      creditos6=fonte_menor.render('João Victor Figueiredo Moura Gomes',False,WHITE)


      preto_transparente.set_alpha(225)
      preto_transparente.blit(nome_jg,(45,170))
      
      preto_transparente.blit(codigos,(45,240))
      preto_transparente.blit(creditos2,(45,280))
      preto_transparente.blit(creditos3,(45,320))
      preto_transparente.blit(creditos4,(45,360))
      preto_transparente.blit(creditos5,(45,400))
      preto_transparente.blit(creditos6,(45,440))

      preto_transparente.blit(bd,(45,500))
      preto_transparente.blit(creditos3,(45,540))
      preto_transparente.blit(creditos6,(45,580))

      preto_transparente.blit(graficos,(45,640))
      preto_transparente.blit(creditos2,(45,680))
      
      preto_transparente.blit(dub,(45,740))
      preto_transparente.blit(creditos3,(45,780))
      preto_transparente.blit(creditos4,(45,820))

      preto_transparente.blit(site,(45,880))
      preto_transparente.blit(creditos3,(45,920))
      preto_transparente.blit(creditos6,(45,960))

      preto_transparente.blit(musica,(45,1000))
      preto_transparente.blit(kevin,(45,1040))

      
      if y_creditos > 0:
        y_creditos = 0

      if y_creditos < -700:
        y_creditos = -700

      screen.blit(preto_transparente,(0,y_creditos))


    if aba_placar:
      preto_transparente = pygame.Surface((600,600))
      preto_transparente.set_alpha(225)
      screen.blit(preto_transparente,(0,0))

    if yy > 0:
      yy = 0

    #colisao()
    placar(msg_placar,fonte)

    msgponto=f"Pontos: {pontos}"
    msg_pontos=fonte.render(msgponto,False,BLACK)

    if my_direction != stop:
      screen.blit(msg_pontos,(447,50))
      escudos_draw()

    linhas_varredura(screen)
    #Atualiza a tela
    pygame.display.update()
    pygame.time.delay(velocidade)
    clock.tick(fps)
    contador+=fps

