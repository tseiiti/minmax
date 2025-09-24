import professor
from min_max import MinMax, Tabuleiro
# import time

class Jogo:
  def __init__(self, linha: int = 7, coluna: int = 7, oponente: str = 'humano', level: int = 2, level_professor: int = 4):
    self.tabuleiro = Tabuleiro(linha = linha, coluna = coluna)
    self.min_max = MinMax(self.tabuleiro, 'O', 'X')
    self.oponente = oponente
    self.level = level
    self.level_professor = level_professor
    self.rodada = 0
    self.encerrar = False

  def jogada(self, linha: int, coluna: int, simbolo: str):
    self.tabuleiro.matrix[linha][coluna] = simbolo
    if simbolo == self.min_max.simbolo_maquina:
      self.tabuleiro.msg[2] = f'Máquina ({self.min_max.simbolo_maquina}) jogou em {coluna + 1} ({linha + 1})'
    else:
      self.tabuleiro.msg[3] = f'Oponente ({self.min_max.simbolo_oponente}) jogou em {coluna + 1} ({linha + 1})'
    self.jogada_avaliar()
    
  def jogada_humano(self):
    linha = -1
    coluna = 0
    while(True):
      txt = input('Informe a coluna ou zero para encerrar: ')
      if txt in '1234567890':
        if txt == '0': 
          self.tabuleiro.msg[9] = 'Desistiu'
          self.encerrar = True
        coluna = int(txt) - 1
        linha = self.tabuleiro.livre(coluna)
      if linha >= 0 or coluna < 0: break
      else: print('Coluna inválida. Tente outra.')
    self.jogada(linha, coluna, self.min_max.simbolo_oponente)

  def jogada_maquina(self):
    _, coluna = self.min_max.mmax(self.tabuleiro, self.level, self.min_max.simbolo_maquina)
    linha = self.tabuleiro.livre(coluna)
    self.jogada(linha, coluna, self.min_max.simbolo_maquina)
    
  def jogada_oponente(self) -> bool:
    coluna = professor.minimax(self.tabuleiro.matrix, self.level_professor)
    linha = self.tabuleiro.livre(coluna)
    self.jogada(linha, coluna, self.min_max.simbolo_oponente)
    
  def jogada_avaliar(self) -> bool:
    self.tabuleiro.msg[0] = f'Rodada: {self.rodada}'
    placar = self.min_max.avaliacao(self.tabuleiro)
    self.tabuleiro.msg[1] = f'Placar: {placar} | {professor.funcaoAvaliacao(self.tabuleiro.matrix)}'
    if placar > 5000:
      self.tabuleiro.msg[9] = 'Máquina ganhou'
      self.encerrar= True
    elif placar < -5000:
      self.tabuleiro.msg[9] = 'Oponente ganhou'
      self.encerrar= True
    elif self.tabuleiro.restantes() == 0:
      self.tabuleiro.msg[9] = 'Empate'
      self.encerrar= True
    # time.sleep(1)
    
  def jogar(self):
    self.tabuleiro.imprimir()
    if self.oponente == 'professor':
      self.jogada(6, 3, self.min_max.simbolo_oponente)
      self.jogada_maquina()

    while True:
      self.rodada += 1
      if self.oponente == 'professor':
        self.jogada_oponente()
      else:
        self.jogada_humano()
      self.jogada_maquina()
      
      self.tabuleiro.imprimir()
      if self.encerrar: break

# jogo = None
# def new(l: int = 2, o: str = 'humano'):
#   jogo = Jogo(level = l, oponente = o)

if __name__ == "__main__":
  # tabuleiro = Tabuleiro(linha = 9, coluna = 9)
  # jogo = Jogo(tabuleiro = tabuleiro)
  # jogo = Jogo(oponente = 'professor', level_professor = 5)
  jogo = Jogo()
  jogo.jogar()
