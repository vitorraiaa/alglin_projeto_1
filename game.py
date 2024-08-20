import math
import pygame

pygame.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Angry Birds no Espaço")

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)

GRAVIDADE = 700
G = 4

class Vetor:
    @staticmethod
    def modulo(vetor):
        return math.sqrt(vetor[0]**2 + vetor[1]**2)
    
    @staticmethod
    def normalizar(vetor):
        modulo = Vetor.modulo(vetor)
        if modulo == 0:
            return [0, 0]
        return [vetor[0] / modulo, vetor[1] / modulo]
    
    @staticmethod
    def escalar(vetor, escalar):
        return [vetor[0] * escalar, vetor[1] * escalar]
    
    @staticmethod
    def somar(vetor1, vetor2):
        return [vetor1[0] + vetor2[0], vetor1[1] + vetor2[1]]

class Projetil:
    def __init__(self, x, y, sprite):
        self.posicao = [x, y]
        self.raio = 20
        self.velocidade = [0, 0]
        self.movendo = False

        self.imagem = pygame.image.load("img/download-removebg-preview (1).png")
        self.imagem = pygame.transform.scale(self.imagem, (self.raio * 2, self.raio * 2))
    
    def desenhar(self, tela):
        posicao_imagem = (int(self.posicao[0] - self.raio), int(self.posicao[1] - self.raio))
        tela.blit(self.imagem, posicao_imagem)
    
    def atualizar(self, dt):
        if self.movendo:
            self.posicao = Vetor.somar(self.posicao, Vetor.escalar(self.velocidade, dt))
            gravidade_vetor = [0, GRAVIDADE * dt]
            self.velocidade = Vetor.somar(self.velocidade, gravidade_vetor)
    
            if self.posicao[1] + self.raio >= ALTURA:
                self.movendo = False

            if (self.posicao[0] < 0 or self.posicao[0] > LARGURA or
                self.posicao[1] < 0 or self.posicao[1] > ALTURA):
                self.movendo = False

class Cano:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
    
    def desenhar(self, tela):
        ponta = (
            self.x + 50 * math.cos(self.angulo),
            self.y - 50 * math.sin(self.angulo)
        )
        pygame.draw.line(tela, BRANCO, (self.x, self.y), ponta, 5)
    
    def ajustar_angulo(self, pos_mouse):
        dx = pos_mouse[0] - self.x
        dy = self.y - pos_mouse[1]
        self.angulo = math.atan2(dy, dx)

class Obstaculo:
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.imagem = pygame.image.load("img/Blue_birds_2.webp")
        self.imagem = pygame.transform.scale(self.imagem, (largura, altura))

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect.topleft)

class Alvo:
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.imagem = pygame.image.load("img/download-removebg-preview.png")
        self.imagem = pygame.transform.scale(self.imagem, (largura, altura))

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect.topleft)

class Planeta:
    def __init__(self, x, y, massa, raio):
        self.x = x
        self.y = y
        self.massa = massa
        self.raio = raio
        self.imagem = pygame.image.load("img/png-clipart-earth-saturn-the-ringed-planet-earth-purple-desktop-wallpaper-removebg-preview.png")
        self.imagem = pygame.transform.scale(self.imagem, (self.raio * 2, self.raio * 2))
    
    def desenhar(self, tela):
        posicao_imagem = (int(self.x - self.raio), int(self.y - self.raio))
        tela.blit(self.imagem, posicao_imagem)
    
    def aplicar_gravidade(self, projetil, dt):
        direcao = [self.x - projetil.posicao[0], self.y - projetil.posicao[1]]
        distancia = Vetor.modulo(direcao)
        
        if distancia > 0:
            direcao_normalizada = Vetor.normalizar(direcao)
            forca = G * self.massa / (distancia**2)
            aceleracao = Vetor.escalar(direcao_normalizada, forca * dt)
            projetil.velocidade = Vetor.somar(projetil.velocidade, aceleracao)

    def verificar_colisao(self, projetil):
        distancia = Vetor.modulo([self.x - projetil.posicao[0], self.y - projetil.posicao[1]])
        return distancia <= self.raio + projetil.raio

def reiniciar_jogo(projetil, canhao):
    projetil.posicao = [canhao.x, canhao.y]
    projetil.velocidade = [0, 0]
    projetil.movendo = False

def tela_inicio():
    fundo = pygame.image.load("img/transferir.jpg")
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
    
    projetil_sprite = pygame.image.load("img/download-removebg-preview (1).png")
    projetil_sprite = pygame.transform.scale(projetil_sprite, (50, 50))
    
    fonte = pygame.font.Font(None, 74)
    texto_iniciar = fonte.render("Iniciar", True, PRETO)
    rect_iniciar = texto_iniciar.get_rect(center=(LARGURA // 2, ALTURA // 2))

    rodando = True
    angulo_projetil = 0
    raio_circulo = 100
    velocidade_angular = 0.0005
    
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_iniciar.collidepoint(evento.pos):
                    return True

        angulo_projetil += velocidade_angular
        x_projetil = LARGURA // 2 + raio_circulo * math.cos(angulo_projetil)
        y_projetil = ALTURA // 2 + raio_circulo * math.sin(angulo_projetil)

        tela.blit(fundo, (0, 0))
        tela.blit(projetil_sprite, (x_projetil - projetil_sprite.get_width() // 2, y_projetil - projetil_sprite.get_height() // 2))
        
        pulsar = 1.05 + 0.05 * math.sin(pygame.time.get_ticks() / 200)
        texto_pulsante = pygame.transform.scale(texto_iniciar, (int(rect_iniciar.width * pulsar), int(rect_iniciar.height * pulsar)))
        rect_pulsante = texto_pulsante.get_rect(center=(LARGURA // 2, ALTURA // 2))
        tela.blit(texto_pulsante, rect_pulsante)

        pygame.display.flip()

def main():
    if not tela_inicio():
        return

    relogio = pygame.time.Clock()
    rodando = True
    
    fundo = pygame.image.load("img/Space-Free-PNG-Image.png")
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
    
    sprite_projetil = pygame.image.load('angry_birds.png').convert_alpha()
    
    canhao = Cano(100, ALTURA - 100)
    projetil = Projetil(canhao.x, canhao.y, sprite_projetil)
    
    obstaculos = [
        Obstaculo(400, ALTURA - 300, 50, 150),
        Obstaculo(550, ALTURA - 350, 50, 200)
    ]
    
    alvo = Alvo(750, 30, 50, 50)
    
    planeta = Planeta(500, 100, massa=5e6, raio=50)
    
    while rodando:
        dt = relogio.tick(60) / 1000.0
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and not projetil.movendo:
                pos_mouse = pygame.mouse.get_pos()
                canhao.ajustar_angulo(pos_mouse)

                direcao = [math.cos(canhao.angulo), -math.sin(canhao.angulo)]
                direcao_normalizada = Vetor.normalizar(direcao)
                distancia_horizontal = max(100, pos_mouse[0] - canhao.x) + 200
                potencia = min(1000, distancia_horizontal) + 200
                projetil.velocidade = Vetor.escalar(direcao_normalizada, potencia)
                projetil.movendo = True

        if projetil.movendo:
            planeta.aplicar_gravidade(projetil, dt)
        
        projetil.atualizar(dt)
        
        if not projetil.movendo:
            reiniciar_jogo(projetil, canhao)
        
        tela.blit(fundo, (0, 0))  # Desenha o fundo antes de todos os outros elementos
        canhao.desenhar(tela)
        projetil.desenhar(tela)
        alvo.desenhar(tela)
        
        planeta.desenhar(tela)
        
        for obstaculo in obstaculos:
            obstaculo.desenhar(tela)
            if projetil.movendo and obstaculo.rect.colliderect(pygame.Rect(projetil.posicao[0] - projetil.raio, projetil.posicao[1] - projetil.raio, projetil.raio*2, projetil.raio*2)):
                reiniciar_jogo(projetil, canhao)
        
        if projetil.movendo and planeta.verificar_colisao(projetil):
            reiniciar_jogo(projetil, canhao)
        
        if projetil.movendo and alvo.rect.colliderect(pygame.Rect(projetil.posicao[0] - projetil.raio, projetil.posicao[1] - projetil.raio, projetil.raio*2, projetil.raio*2)):
            rodando = False
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
