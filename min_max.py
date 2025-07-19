from tabuleiro import Tabuleiro

class MinMax:
  def __init__(self, tabuleiro: Tabuleiro, simbolo_maquina: str = 'X', simbolo_oponente: str = 'O'):
    self.tabuleiro = tabuleiro
    self.simbolo_maquina = simbolo_maquina
    self.simbolo_oponente = simbolo_oponente

  def pontuar(self, validacao: str, simbolo: str) -> int:
    s4 = simbolo * 4
    s3 = simbolo * 3
    s2 = simbolo * 2
    s2_ = s2 + ' ' + simbolo
    s_2 = simbolo + ' ' + s2
    s1_1 = simbolo + ' ' + simbolo
    pontos = 0
    pontos += validacao.count(s4) * 10000
    pontos += validacao.count(s3 + ' ') * 75
    pontos += validacao.count(' ' + s3) * 75
    pontos += validacao.count(s2_) * 60
    pontos += validacao.count(s2_ + ' ') * 10
    pontos += validacao.count(' ' + s2_) * 10
    pontos += validacao.count(s_2) * 60
    pontos += validacao.count(s_2 + ' ') * 10
    pontos += validacao.count(' ' + s_2) * 10
    pontos += validacao.count(s1_1 + ' ') * 30
    pontos += validacao.count(' ' + s1_1) * 30
    pontos += validacao.count(s2 + '  ') * 30
    pontos += validacao.count('  ' + s2) * 30
    pontos += validacao.count(' ' + s2 + ' ') * 30
    return pontos
  
  def avaliacao(self, tabuleiro: Tabuleiro) -> int:
    validacao = tabuleiro.validacao()
    maquina = self.pontuar(validacao, self.simbolo_maquina)
    oponente = self.pontuar(validacao, self.simbolo_oponente)
    return maquina - oponente
  
  def resultado(self):
    pontos = self.avaliacao(self.tabuleiro)
    msg = ''
    if pontos > 5000:
      msg = 'Máquina ganhou'
    elif pontos < -5000:
      msg = 'Oponente ganhou'
    elif self.tabuleiro.restantes() == 0:
      msg = 'Empate'
    return pontos, msg
    
  def mmax(self, tabuleiro: Tabuleiro, level: int, simbolo: str) -> int:
    if not tabuleiro: return 20000, 0
    if level == 0: return self.avaliacao(tabuleiro), 0
    pontos = []
    for t in tabuleiro.sucessores(simbolo):
      ponto, _ = self.mmin(t, level - 1, self.outro(simbolo))
      pontos.append(ponto)
    return max(pontos), pontos.index(max(pontos))

  def mmin(self, tabuleiro: Tabuleiro, level: int, simbolo: str) -> int:
    if not tabuleiro: return -20000, 0
    if level == 0: return self.avaliacao(tabuleiro), 0
    pontos = []
    for t in tabuleiro.sucessores(simbolo):
      ponto, _ = self.mmax(t, level - 1, self.outro(simbolo))
      pontos.append(ponto)
    return min(pontos), pontos.index(min(pontos))
    
  def outro(self, simbolo: str) -> str:
    if simbolo == self.simbolo_maquina: return self.simbolo_oponente
    else: return self.simbolo_maquina
