import professor
from min_max import MinMax, Tabuleiro
# import time

class Jogo:
  def __init__(self, tabuleiro: Tabuleiro = None, level: int = 2, simbolo_maquina: str = 'X', simbolo_oponente: str = 'O'):
    if tabuleiro == None: tabuleiro = Tabuleiro()
    self.tabuleiro = tabuleiro
    self.min_max = MinMax(self.tabuleiro, simbolo_maquina, simbolo_oponente)
    self.level = level
    self.rodada = 0

  def jogada(self, linha: int, coluna: int, simbolo: str):
    self.tabuleiro.matrix[linha][coluna] = simbolo
    if simbolo == self.min_max.simbolo_maquina:
      self.tabuleiro.msg[2] = f'Máquina ({self.min_max.simbolo_maquina}) jogou em {coluna + 1} ({linha + 1})'
    else:
      self.tabuleiro.msg[3] = f'Oponente ({self.min_max.simbolo_oponente}) jogou em {coluna + 1} ({linha + 1})'
    
  def jogada_humano(self):
    while(True):
      coluna = input('Informe a coluna ou zero para encerrar: ')
      if coluna in '1234567890':
        coluna = int(coluna) - 1
        linha = self.tabuleiro.livre(coluna)
      if linha >= 0: break
      else: print('Coluna inválida. Tente outra.')
    self.jogada(linha, coluna, self.min_max.simbolo_oponente)

  def jogada_maquina(self):
    _, coluna = self.min_max.mmax(self.tabuleiro, self.level, self.min_max.simbolo_maquina)
    linha = self.tabuleiro.livre(coluna)
    self.jogada(linha, coluna, self.min_max.simbolo_maquina)
    
  def jogada_oponente(self) -> bool:
    coluna = professor.minimax(jogo.tabuleiro.matrix, 4)
    linha = self.tabuleiro.livre(coluna)
    self.jogada(linha, coluna, self.min_max.simbolo_oponente)
    
  def jogada_avaliar(self) -> bool:
    self.tabuleiro.msg[0] = f'Rodada: {self.rodada}'
    pontos, msg = self.min_max.resultado()
    self.tabuleiro.msg[1] = f'Placar: {pontos} | {professor.funcaoAvaliacao(self.tabuleiro.matrix)}'
    self.tabuleiro.imprimir()
    # time.sleep(1)
    if msg != '':
      print(msg)
      return True
    return False
    
  def main(self):
    # self.jogada(6, 3, self.min_max.simbolo_oponente)
    # self.jogada_maquina()
    self.jogada_avaliar()

    while True:
      self.rodada += 1
      self.jogada_oponente()
      # self.jogada_humano()
      self.jogada_maquina()
      if self.jogada_avaliar(): break

if __name__ == "__main__":
  jogo = Jogo(simbolo_maquina = 'O', simbolo_oponente = 'X')
  jogo.main()
