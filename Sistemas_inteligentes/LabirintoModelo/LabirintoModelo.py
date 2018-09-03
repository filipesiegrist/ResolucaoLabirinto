#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 12:59:28 2018

@author: filipe-ufsc
"""
from __future__ import print_function
from random import randint


class Labirinto:
    #matriz 10x10 com labirinto
    #x e y correntes
    #construtor
    def __init__(self):
        #essa linha cria uma matriz de zeros 10x10
        self.__matriz = [[0 for x in range(10)] for y in range(10)]
        #gera numeros aleatorios na matriz
        for i in range(10):
            for j in range(10):
                #se for 1 e parede, se for 0 e caminho
                self.__matriz[i][j] = randint(0,1)
        #gera uma posicao aleatoria para comecar, mas tem que ser 0
        self.__currentX = randint(1,8)
        self.__currentY = randint(1,8)
        while self.__matriz[self.__currentX][self.__currentY] == 1:
            self.__currentX = randint(1,8)
            self.__currentY = randint(1,8)
            
    #Retorna se a celula tem zero ou um
    def __getNumero(self):
        return self.__matriz[self.__currentX][self.__currentY]
    
    #faz o teste se a posicao e uma posicao de saida do labirinto
    def testeSaida(self):
        if self.__getNumero() == 1: return False
        elif self.__currentX == 0 or self.__currentX == 9: return True
        elif self.__currentY == 0 or self.__currentY == 9: return True
        else: return False
        
    #funcao auxiliar para mostrar o labirinto
    def imprime(self):
        
        for j in range (10):
            for i in range(10):
                if i == self.__currentX and j == self.__currentY:
                    print ('X'," ",end='')
                else:
                    print(self.__matriz[i][j]," ",end='')
            print("\n")
    
    #funcao auxiliar para posicao corrente
    def localizacao(self):
        print("\nCurrent Position: X=",self.__currentX," Y=",self.__currentY)
    
# =============================================================================
#     TENTA MOVER PARA CIMA
#     RETORNA:
#         0 SE BATEU EM PAREDE
#         1 SE MOVEU COM SUCESSO
#         2 SE SAIU DO LABIRINTO
# =============================================================================
    def up(self):
        self.__currentY -= 1
        #se chegou em uma parede volta a posicao e retorna zero
        if self.__getNumero() == 1:
            self.__currentY += 1
            return False
        #se nao saiu do labirinto retorna um
        else: return True
        
# =============================================================================
#     TENTA MOVER PARA BAIXO
#     RETORNA:
#         0 SE BATEU EM PAREDE
#         1 SE MOVEU COM SUCESSO
#         2 SE SAIU DO LABIRINTO
# =============================================================================
    def down(self):
        self.__currentY += 1
        #se chegou em uma parede volta a posicao e retorna zero
        if self.__getNumero() == 1:
            self.__currentY -= 1
            return False
        #se nao saiu do labirinto retorna um
        else: return 1
        
# =============================================================================
#     TENTA MOVER PARA A ESQUERDA
#     RETORNA:
#         0 SE BATEU EM PAREDE
#         1 SE MOVEU COM SUCESSO
#         2 SE SAIU DO LABIRINTO
# =============================================================================
    def left(self):
        self.__currentX -= 1
        #se chegou em uma parede volta a posicao e retorna zero
        if self.__getNumero() == 1:
            self.__currentX += 1
            return False
        #se tem caminho a andar verifica se saiu do labirinto e retorna dois
        else: return True
        
# =============================================================================
#     TENTA MOVER PARA A DIREITA
#     RETORNA:
#         0 SE BATEU EM PAREDE
#         1 SE MOVEU COM SUCESSO
#         2 SE SAIU DO LABIRINTO
#
# =============================================================================
    def right(self):
        self.__currentX += 1
        #se chegou em uma parede volta a posicao e retorna zero
        if self.__getNumero() == 1:
            self.__currentX -= 1
            return False
        #se tem caminho a andar verifica se saiu do labirinto e retorna dois
        else: return True
    
