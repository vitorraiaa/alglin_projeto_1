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

GRAVIDADE = 700

class Projetil:
    def __init__(self, x, y):
        self.posicao = [x, y]
        self.raio = 10
        self.cor = VERMELHO
        self.velocidade = [0, 0]
        self.movendo = False
    
    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.posicao[0]), int(self.posicao[1])), self.raio)
    
    def atualizar(self, dt):
        if self.movendo:
            self.velocidade[1] += GRAVIDADE * dt
            self.posicao[0] += self.velocidade[0] * dt
            self.posicao[1] += self.velocidade[1] * dt

            # Verificar colisão com o chão
            if self.posicao[1] + self.raio >= ALTURA:
                self.movendo = False
            
            # Verificar se ultrapassou os limites da tela
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
        self.cor = AZUL
    
    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)

class Alvo:
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = VERDE
    
    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)

def reiniciar_jogo(projetil, canhao):
    projetil.posicao = [canhao.x, canhao.y]
    projetil.velocidade = [0, 0]
    projetil.movendo = False

def main():
    relogio = pygame.time.Clock()
    rodando = True
    
    canhao = Cano(100, ALTURA - 100)
    projetil = Projetil(canhao.x, canhao.y)
    
    obstaculos = [
        Obstaculo(400, ALTURA - 150, 50, 150),
        Obstaculo(600, ALTURA - 200, 50, 200)
    ]
    
    alvo = Alvo(750, ALTURA - 50, 50, 50)
    
    while rodando:
        dt = relogio.tick(60) / 1000.0
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and not projetil.movendo:
                pos_mouse = pygame.mouse.get_pos()
                canhao.ajustar_angulo(pos_mouse)
                
                
                distancia_horizontal = max(100, pos_mouse[0] - canhao.x)  +100
                potencia = min(100000, distancia_horizontal)  +100
                
                projetil.velocidade[0] = potencia * math.cos(canhao.angulo)
                projetil.velocidade[1] = -potencia * math.sin(canhao.angulo)
                projetil.movendo = True
        
        projetil.atualizar(dt)
        
       
        if not projetil.movendo:
            reiniciar_jogo(projetil, canhao)
        
        tela.fill(PRETO)
        canhao.desenhar(tela)
        projetil.desenhar(tela)
        alvo.desenhar(tela)
        
        for obstaculo in obstaculos:
            obstaculo.desenhar(tela)
            if projetil.movendo and obstaculo.rect.colliderect(pygame.Rect(projetil.posicao[0] - projetil.raio, projetil.posicao[1] - projetil.raio, projetil.raio*2, projetil.raio*2)):
                reiniciar_jogo(projetil, canhao)
        
        if projetil.movendo and alvo.rect.colliderect(pygame.Rect(projetil.posicao[0] - projetil.raio, projetil.posicao[1] - projetil.raio, projetil.raio*2, projetil.raio*2)):
            print("Acertou o alvo!")
            rodando = False
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
