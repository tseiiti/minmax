# import numpy as np
from copy import deepcopy
import math

def funcaoAvaliacao(mat):
  pontuacaoComput =  max( avaliacaoHorizontal(mat, 'X'),
                        avaliacaoVertical(mat, 'X'),
                        avaliacaoDiagonalPrincipal(mat, 'X'),
                        avaliacaoDiagonalSecundaria(mat, 'X') )
  pontuacaoHumano =  max( avaliacaoHorizontal(mat, 'O'),
                        avaliacaoVertical(mat, 'O'),
                        avaliacaoDiagonalPrincipal(mat, 'O'),
                        avaliacaoDiagonalSecundaria(mat, 'O') )
  if pontuacaoHumano == 4: retorno = -1000
  elif pontuacaoComput == 4: retorno = 1000
  elif pontuacaoHumano >= 2.5: retorno = -500
  elif pontuacaoComput >= 2.5: retorno = 500
  else: retorno = 200*(pontuacaoComput - pontuacaoHumano)
  # print(f'Pontuação Humano={pontuacaoHumano}, Pontuação Computador={pontuacaoComput}, Retorno={retorno}')
  return retorno

# ajuste na função de avaliação (07/05/2025)
def pontuar(matString, jogador):
  if (jogador*4) in matString: return 4
  elif jogador+' '+(jogador*2) in matString or (jogador*2)+' '+jogador in matString: return 3
  elif ' '+(jogador*3) in matString or (jogador*3)+' ' in matString: return 3
  elif ' '+(jogador*2) in matString or (jogador*2)+' ' in matString: return 2
  elif jogador+' '+jogador in matString or jogador+'  '+jogador in matString: return 1.5  # acréscimo
  else: return 0

# # ajuste na função de avaliação (28/03/2023)
# def pontuar(matString, jogador):
#   if (jogador*4) in matString: return 4
#   elif ' '+(jogador*3) in matString or (jogador*3)+' ' in matString: return 3
#   elif jogador+'  '+(jogador*2) in matString or (jogador*2)+'  '+jogador in matString or\
#        jogador+' '+jogador+' ' in matString or ' '+jogador+' '+jogador in matString  or\
#        ' '+(jogador*2)+' ' in matString or jogador+'  '+jogador in matString: return 2.5  # acréscimo
#   else: return 0

# # ajuste na função de avaliação (11/04/2022)
# def pontuar(matString, jogador):
#   if (jogador*4) in matString: return 4
#   elif ' '+(jogador*3) in matString or (jogador*3)+' ' in matString: return 3
#   elif jogador+' '+(jogador*2) in matString or (jogador*2)+' '+jogador in matString: return 2.5  # acréscimo
#   elif ' '+(jogador*2) in matString or (jogador*2)+' ' in matString: return 2
#   elif jogador+' '+jogador in matString or jogador+'  '+jogador in matString: return 1.5  # acréscimo
#   else: return 0

def avaliacaoHorizontal(mat, jogador):
  matString = ''
  for l in range(len(mat)):
    for c in range(len(mat[0])):
      matString += mat[l][c]
    matString += '\n'
  #print('String:', matString, sep='\n')
  return pontuar(matString, jogador)

def avaliacaoVertical(mat, jogador):
  matString = ''
  for c in range(len(mat[0])):
    for l in range(len(mat)):
      matString += mat[l][c]
    matString += '\n'
  #print('String:', matString, sep='\n')
  return pontuar(matString, jogador)

def avaliacaoDiagonalPrincipal(mat, jogador):
  matString = ''
  for x in range(len(mat)-1, 0, -1):
    l = x; c = 0
    while l<len(mat) and c<len(mat[0]):
      matString += mat[l][c]
      l+=1; c+=1
    matString += '\n'

  for x in range(len(mat[0])):
    l = 0; c = x
    while l<len(mat) and c<len(mat[0]):
      matString += mat[l][c]
      l+=1; c+=1
    matString += '\n'
  #print('String:', matString, sep='\n')
  return pontuar(matString, jogador)

def avaliacaoDiagonalSecundaria(mat, jogador):
  matString = ''
  for x in range(len(mat)-1, 0, -1):
    l = x; c = len(mat[0])-1
    while l<len(mat) and c>=0:
      matString += mat[l][c]
      l+=1; c-=1
    matString += '\n'

  for x in range(len(mat[0])-1, -1, -1):
    l = 0; c = x
    while l<len(mat) and c>=0:
      matString += mat[l][c]
      l+=1; c-=1
    matString += '\n'
  #print('String:', matString, sep='\n')
  return pontuar(matString, jogador)

'''
 Funções úteis
'''
def primeiraLinhaLivre(coluna, mat):
  return livre(len(mat)-1, coluna, mat)

def livre(linha, coluna, mat):
  if linha<0: return -1
  if mat[linha][coluna] == ' ': return linha
  return livre(linha-1, coluna, mat)

def outro(jogador):
  if jogador == 'X': return 'O'
  else: return 'X'

def gereSucessores(inicio, vez):
  suc = []
  for i in range(len(inicio[0])):
    linha = primeiraLinhaLivre(i, inicio)
    if linha >= 0:
      novaMat = deepcopy(inicio)
      novaMat[linha][i] = vez
      suc.append(novaMat)
    else:
      suc.append(None)
  return suc

def imprimirMatriz(mat):
  print('😡 = Computador     😎 = Humano\n')
  for i in range(len(mat)):
    print(f'{i:2} ', end=' ')
    for j in range(len(mat[0])):
      if mat[i][j] == 'O': print('😎 ', end='')
      elif mat[i][j] == 'X': print('😡 ', end='')
      else: print('   ', end='')
    print()
  print('   ', end='')
  for j in range(len(mat[0])):
    print(f'{j:2} ', end='')
  print()

'''
 Algoritmo Minimax
'''
def minimax (inicio, nivelDeDificuldade):
  _ , coluna = maxNo(inicio, 'X', nivelDeDificuldade)  # O computador quer maximizar seus pontos
  return coluna

def maxNo(inicio, vez, dificuldade):
  if dificuldade == 0:
    return funcaoAvaliacao(inicio), 0
  else:
    sucessores = gereSucessores(inicio, vez)
    pontos = []
    for i in range(len(sucessores)):
      if sucessores[i] == None: pontos.append(-math.inf) # jogada impossível
      else:
        ponto, indice = minNo( sucessores[i], outro(vez), dificuldade-1)
        pontos.append(ponto)
    return max(pontos), pontos.index(max(pontos)) #np.argmax(pontos)

def minNo(inicio, vez, dificuldade):
  if dificuldade == 0:
    return funcaoAvaliacao(inicio), 0
  else:
    sucessores = gereSucessores(inicio, vez)
    pontos = []
    for i in range(len(sucessores)):
      if sucessores[i] == None: pontos.append(math.inf) # jogada impossível
      else:
        ponto, indice = maxNo( sucessores[i], outro(vez), dificuldade-1)
        pontos.append(ponto)
    return min(pontos), pontos.index(min(pontos)) #np.argmin(pontos)

def quantasJogadasRestam(mat):
  cont=0
  for i in range(7):
    for j in range(7):
      if mat[i][j] == ' ': cont+=1
  return cont

'''
 Jogo Connect4
'''
def main():
  mat = [[' ',' ',' ',' ',' ',' ',' '],
         [' ',' ',' ',' ',' ',' ',' '],
         [' ',' ',' ',' ',' ',' ',' '],
         [' ',' ',' ',' ',' ',' ',' '],
         [' ',' ',' ',' ',' ',' ',' '],
         [' ',' ',' ',' ',' ',' ',' '],
         [' ',' ',' ','X',' ',' ',' ']]

  imprimirMatriz(mat)
  while(True):
    #Jogada do humano
    jogadasRestantes = quantasJogadasRestam(mat)
    print('Restam', jogadasRestantes, 'jogadas no máximo.')
    if jogadasRestantes == 0:
      print('Empate!!')
      break
    while(True):
      colunaString = input('Entre com a coluna em que deseja jogar: ')
      coluna = int(colunaString)
      linha = primeiraLinhaLivre(coluna, mat)
      if linha >= 0: break
      else: print('Essa coluna está lotada. Tente outra.')
    mat[linha][coluna] = 'O'
    placar = funcaoAvaliacao(mat)
    imprimirMatriz(mat)
    if placar > 0: print('Vantagem do COMPUTADOR')
    else: print('Vantagem do HUMANO')
    if placar <= -1000:
      print('Parabéns, você ganhou!!')
      break
    # Jogada do computador
    coluna = minimax(mat, 2)  # grau de dificuldade 2
    linha = primeiraLinhaLivre(coluna, mat)
    if linha == -1:
      print('Empate!!!!')
      break
    print('\nMinha jogada: COLUNA =', coluna, ', LINHA =', linha)
    mat[linha][coluna] = 'X'
    imprimirMatriz(mat)
    placar = funcaoAvaliacao(mat)
    if placar > 0: print('Vantagem do COMPUTADOR')
    else: print('Vantagem do HUMANO')
    if placar >= 1000:
      print('Patinho! Eu ganhei!!!!')
      break

# main()
