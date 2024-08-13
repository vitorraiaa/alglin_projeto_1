import pygame
import math

pygame.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Angry Birds no Espaço")

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

def modulo_vetor(vetor):
    return math.sqrt(vetor[0] ** 2 + vetor[1] ** 2)

def normalizar_vetor(vetor):
    modulo = modulo_vetor(vetor)
    if modulo == 0:
        return (0, 0)
    return (vetor[0] / modulo, vetor[1] / modulo)

def multiplicar_vetor(vetor, escalar):
    return (vetor[0] * escalar, vetor[1] * escalar)

def somar_vetores(vetor1, vetor2):
    return (vetor1[0] + vetor2[0], vetor1[1] + vetor2[1])

class Projetil:
    def __init__(self, x, y):
        self.posicao = (x, y)
        self.raio = 10
        self.cor = VERMELHO
        self.velocidade = (0, 0)
        self.movendo = False
    
    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.posicao[0]), int(self.posicao[1])), self.raio)
    
    def atualizar(self, dt, corpos_gravitacionais):
        if self.movendo:
            forca_total = (0, 0)
            for corpo in corpos_gravitacionais:
                forca = corpo.atracao(self)
                forca_total = somar_vetores(forca_total, forca)
            aceleracao = forca_total
            self.velocidade = somar_vetores(self.velocidade, multiplicar_vetor(aceleracao, dt))
            self.posicao = somar_vetores(self.posicao, multiplicar_vetor(self.velocidade, dt))

class CorpoGravitacional:
    def __init__(self, x, y, massa):
        self.posicao = (x, y)
        self.massa = massa
        self.raio = int(math.sqrt(massa))
        self.cor = BRANCO
    
    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.posicao[0]), int(self.posicao[1])), self.raio)
    
    def atracao(self, projetil):
        G = 100
        direcao = (self.posicao[0] - projetil.posicao[0], self.posicao[1] - projetil.posicao[1])
        distancia = modulo_vetor(direcao)
        if distancia == 0:
            distancia = 0.1
        direcao_normalizada = normalizar_vetor(direcao)
        modulo_forca = G * self.massa / (distancia ** 2)
        forca = multiplicar_vetor(direcao_normalizada, modulo_forca)
        return forca

def main():
    relogio = pygame.time.Clock()
    rodando = True
    projetil = Projetil(100, ALTURA // 2)
    corpos_gravitacionais = [CorpoGravitacional(LARGURA // 2, ALTURA // 2, 5000)]
    posicao_inicial = None
    
    while rodando:
        dt = relogio.tick(60) / 1000.0
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if not projetil.movendo:
                    posicao_inicial = pygame.mouse.get_pos()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if not projetil.movendo and posicao_inicial:
                    posicao_final = pygame.mouse.get_pos()
                    vetor_lancamento = (posicao_final[0] - posicao_inicial[0], posicao_final[1] - posicao_inicial[1])
                    vetor_lancamento_normalizado = normalizar_vetor(vetor_lancamento)
                    modulo_lancamento = modulo_vetor(vetor_lancamento) * 0.1
                    projetil.velocidade = multiplicar_vetor(vetor_lancamento_normalizado, modulo_lancamento)
                    projetil.movendo = True
        
        projetil.atualizar(dt, corpos_gravitacionais)
        
        tela.fill(PRETO)
        projetil.desenhar(tela)
        for corpo in corpos_gravitacionais:
            corpo.desenhar(tela)
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
