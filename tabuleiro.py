class Tabuleiro:
  def __init__(self, matrix: list = None, linha: int = 7, coluna: int = 7):
    if matrix == None: 
      matrix = [[' ' for _ in range(coluna)] for _ in range(linha)]
    self.matrix = matrix
    self.linha  = len(matrix)
    self.coluna = len(matrix[0])
    self.msg = [ '' for _ in range(4) ]
  
  def livre(self, coluna: int, linha: int = None) -> int:
    if coluna < 0 or coluna >= self.coluna: return -1
    if linha == None: linha = self.linha - 1
    if linha < 0: return -1
    if self.matrix[linha][coluna] == ' ': return linha
    return self.livre(coluna, linha - 1)
  
  def validacao(self) -> str:
    validacao = ''
    validacao += self._horizontal()
    validacao += self._vertical()
    validacao += self._diagonal('principal')
    validacao += self._diagonal('secundaria')
    return validacao
  
  def sucessores(self, simbolo: str) -> list:
    aux = []
    for coluna in range(self.coluna):
      linha = self.livre(coluna)
      if linha >= 0:
        matrix = [e[:] for e in self.matrix]
        matrix[linha][coluna] = simbolo
        aux.append(Tabuleiro(matrix))
      else:
        aux.append(None)
    return aux

  def imprimir(self):
    lin = '   ' + '-' * (self.coluna * 4 + 1) + '\n'
    t = '\n'
    for i in range(self.linha):
      t += lin
      t += f'{i + 1:2} '
      for j in range(self.coluna): t += f'| {self.matrix[i][j] } '
      t += '|'
      if i < 4 and self.msg[i] != '': t += '   - ' + self.msg[i]
      t += '\n'
    t += lin
    t += '   '
    for j in range(self.coluna): t += f'  {j + 1} '
    t += ' \n'
    print(t)

  def restantes(self) -> int:
    rest = 0
    for i in range(self.linha):
      for j in range(self.coluna):
        if self.matrix[i][j] == ' ': rest += 1
    return rest

  # privates

  def _horizontal(self) -> str:
    t = ''
    for l in range(self.linha):
      for c in range(self.coluna): t += self.matrix[l][c]
      t += '\n'
    return t
  
  def _vertical(self) -> str:
    t = ''
    for c in range(self.coluna):
      for l in range(self.linha): t += self.matrix[l][c]
      t += '\n'
    return t
  
  def _diagonal(self, type: str = 'principal') -> str:
    t = ''
    h = max(self.linha, self.coluna)
    h += min(self.linha, self.coluna) - 1
    for i in range(h):
      j = self.linha - i - 1
      k = j * - 1
      if k < 0: k = 0
      l = i + 1
      if l > self.coluna: l = self.coluna
      for y in range(k, l):
        if type == 'principal': x = j + y
        elif type == 'secundaria': x = i - y
        t += self.matrix[x][y]
      t += '\n'
    return t
