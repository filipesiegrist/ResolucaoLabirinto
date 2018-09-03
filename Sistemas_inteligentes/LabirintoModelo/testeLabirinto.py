#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 13:29:12 2018

@author: filipe-ufsc
"""
import spade
from LabirintoModelo import Labirinto

LabTeste = Labirinto()

while True:    
    LabTeste.imprime()
    posicao = raw_input("Insira a posicao que vc quer andar (c-cima,b-baixo,e-esquerda,d-direita,s-sair): ")
    if posicao == "d":
        LabTeste.right()
    elif posicao == "w":
        LabTeste.up()
    elif posicao == "s":
        LabTeste.down()
    elif posicao == "a":
        LabTeste.left()
    else:
        break
    if LabTeste.testeSaida():
        LabTeste.imprime()
        print("VOCE GANHOU!!!")
        break
