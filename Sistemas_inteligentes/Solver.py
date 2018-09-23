#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Solucao.py
#  
#  Copyright 2018 Filipe-UFSC <filipe-ufsc@filipeufsc-Aspire-5740>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import spade
import time
from random import randint

#Classe que guarda o mapa do labirinto
class Mapa:
	#position
	#vetor com coordenadas [0] - x
	#                      [1] - y
	
	#path
	#vetor com o caminho percorrido
	# Posição:
	# 0	c
	# 1	d
	# 2	b
	# 3	e
	
	#nodes
	#Lista dos nodos percorridos, ex:
	# [0,0] , [1,0] , [1,1]
	
	#prevposition
	#Posicao anterior, no mesmo formato de position
	
	#prevpath
	#Acao anterior, segue o mesmo padrao de path
	
	
	#Contadores para debugging:
	
	#num_lefthandrule
	#Numero de movimentos usando a regra da mao esquerda
	
	#num_random
	#Numero de movimentos aleatorios no mapa
	
	def __init__(self):
		#posicao atual no labirinto
		self.__position = [0,0]
		#adiciona a posicao anterior do labirinto
		self.__prevposition = [0,0]
		#direcoes que foram percorridas
		self.__path = []
		#direcao anterior à atual, 0 como referencia. Significa que o agente estava virado para cima
		self.__prevpath = 0
		#todas as coordenadas dos nodos percorridos
		self.__nodes = []
		#adiciona a posicao inicial
		self.__nodes.append([0,0])
		
		
		#Inicia os contadores como zero
		self.__num_lefthandrule = 0
		self.__num_random = 0
	
	#Funcao que efetua o movimento e atualiza as variaveis:
	#	path
	#	position
	#	nodes
	#Recebe Numero de 0-3 seguindo o padrao acima
	def registraMovimento(self,numdir):
		referencia = ['c','d','b','e']
		
		#adiciona a ultima acao em prevpath se path no esta vazia
		if self.__path:
			self.__prevpath = self.__path[-1]
		
		#adiciona o numero em path
		self.__path.append(numdir)
		
		#adiciona a posicao atual em prevposition
		self.__prevposition = self.__position[:]
		
		
		#atualiza as coordenadas:
		if referencia[numdir] == 'c':
			#y++
			self.__position[1] += 1
		elif referencia[numdir] == 'd':
			#x++
			self.__position[0] += 1
		elif referencia[numdir] == 'b':
			#y--
			self.__position[1] -= 1
		elif referencia[numdir] == 'e':
			#x--
			self.__position[0] -= 1
			
		coordenada = self.__position[:]
		#adiciona a nova coordenada na lista de nodos se ela nao consta
		if not self.coordenadaExistente(coordenada):
			self.__nodes.append(coordenada)
	
	#retorna a posicao
	def getPosition(self):
		return self.__position
		
	#retorna as direcoes percorridas
	def getPath(self):
		return self.__path
	
	#retorna a lista de nodos percorridos
	def getNodeList(self):
		return self.__nodes
		
	def imprime(self):
		acao = ["cima","dir","baixo","esq"]
		print "----------Mapa do Labirinto-----------"
		print "Posicao atual: " , self.__position
		print "Posicao anterior: " , self.__prevposition
		print "Caminho percorrido: " , self.__path
		print "Acao Atual: " , acao[self.__path[-1]]
		print "Acao Anterior: " , acao[self.__prevpath]
		print "Nodos percorridos: " , self.__nodes
		print "-------------Fim do Mapa---------------"

	#define qual a proxima posicao que deve ir
	#recebe string com as posicoes possiveis no estilo "[c, d, b, e]"
	#retorna numero de 0-3 com a acao
	def proxDirecao(self,posicoes):
		acoes = ["0","cima","0","0","dir","0","0","baixo","0","0","esq"]
		
		#----------------------------JEITO ALTERNATIVO----------------------------
		#Escolhe as direcoes de acordo com uma prioridade: 
		#Ordem decrescente: c-d-b-e , ou 0,1,2,3
		
		#Da prioridade para o menor numero
		# for i in range(4):
			# if posicoes[i*3 +1] == '1':
				# acao = i
				# break
		#----------------------------JEITO ALTERNATIVO----------------------------
		
		#-----------------------------Jeito++----------------------------
		
		# if self.numeroPassagens(posicoes) > 1:
			# #Escolhe o caminho na prioridade, mas tem que ser diferente do ultimo
			# for i in range(4):
				# if posicoes[i*3 +1] == '1':
					# if (i != self.__prevpath - 2 and i != self.__prevpath + 2):
						# acao = i
						# break
		# else:
			# for i in range(4):
				# if posicoes[i*3 +1] == '1':
					# acao = i
					# break
		
		#-----------------------------Jeito++-----------------------------
		
		#-------------------------------------------------Regra da mao esquerda--------------------------------------------------
		#tenta sempre seguir essas posicoes relativas na ordem:
		#-esquerda (3)
		#-cima (0)
		#-direita (1)
		#-baixo (2)
		
		
		#vetor contendo essas prioridades para usar no for. Direcoes relativas
		direcaopreferida = [3,0,1,2]
		
		
		#print "------------------------DEBUG------------------------"
		
		#Se path estiver vazia a acao e cima. Se nao tiver pega path[-1]
		
		direcaopreferidanome = ["esquerda","cima","direita","baixo"]
		
		for i in range(4):
			#Pega a direcao absoluta pega, que depende da ultima acao do agente
			direcao = self.dirAbsoluta(direcaopreferida[i])
			#verifica se e possivel executar essa acao
			#print "proxDirecao: tentando ir à dir preferida: " , direcaopreferidanome[i]
			#print "proxDirecao: tentando ir à dir absoluta" , direcaopreferidanome[self.dirAbsoluta(i)]
			if posicoes[direcao*3 +1] == '1':
				acao = direcao
				#print "proxDirecao: conseguiu"
				break
			#else:
				#print "proxDirecao: nao disponivel"
		
		#-------------------------------------------------Regra da mao esquerda-------------------------------------------------
		
		#Agora verifica se ja passou por essa coordenada. Se ja passou, escolhe outra aleatoriamente
		if (self.coordenadaExistente(self.coordenadaMovimento(acao))):
			#incrementa o contador de movimentos aleatorios
			self.__num_random += 1
			
			print "\nproxDirecao: Ja foi para esse lugar. Escolhe um lugar aleatorio agora."
			#----------------------------JEITO ALEATÓRIO----------------------------
			#escolhe acao nova enquanto der caminho
			acao = randint(0,3)
			while posicoes[acao*3 +1] != '1':
				acao = randint(0,3)
				#print "Iria para " , acoes[acao]
				
			print "proxDirecao: Ira para a coordenada: ", self.coordenadaMovimento(acao)
			#----------------------------JEITO ALEATÓRIO----------------------------
			print "\n"
		else:
			#incrementa o contador de movimentos usando a regra da mao esquerda
			self.__num_lefthandrule += 1
		
		return acao

	#verifica se o seguinte nodo já esta na lista de nodos
	def coordenadaExistente(self,coord):
		for nodo in self.__nodes:
			if nodo == coord:
				return True
		return False

	#pega o vetor e diz o numero de passagens que existem
	def numeroPassagens(self,posicoes):
		contador = 0
		#percorre as direcoes e conta os 1's
		for i in range(4):
			if posicoes[i*3 +1] == '1':
				contador += 1
		return contador
	
	
	#Essa função pega o sentido de movimento do agente e determina para qual sentido ele deve ir.
	#Ex: Se o agente executou uma subida (0) e quer ir à esquerda (3) a direcao absoluta é esquerda (3)
	#	Já se o agente executou uma descida (2) e quer ir à esquerda (3) a direcao absoluta será a direita (2)
	#recebe a posição direcao (0-3) e devolve a posição direcao (0-3)
	def dirAbsoluta(self, dirRelativa):
		#matriz de posicoes.
		#matrizposicoes[x][y], onde:
		#x: direcao que o agente tomou, (0-3)
		#y: direcao relativa que ele quer sair
		#o valor da matriz é a direcao absoluta
		matrizposicoes = [ 
							[0,1,2,3],
							[1,2,3,0],
							[2,3,0,1],
							[3,0,1,2]
						 ]
						 
		# a posicao X é self.__prevpath se __path esta vazia ou entao pega __path[-1]
		#retorna a direcao atraves da matriz
		if not self.__path:
			X = 0
		else:
			X = self.__path[-1]
		
		return matrizposicoes[X][dirRelativa]
	
	#retorna as coordenadas hipoteticas de um determinado movimento
	#movimento no padrao 0-3
	#retorna vetor [x,y]
	def coordenadaMovimento(self,mov):
		#cima
		coordenadas = self.__position[:]
		if mov == 0:
			coordenadas[1] += 1
		#direita
		elif mov == 1:
			coordenadas[0] += 1
		#baixo
		elif mov == 2:
			coordenadas[1] -= 1
		#esquerda
		elif mov == 3:
			coordenadas[0] -= 1
		return coordenadas
	
	#Mostra os movimentos utilizados
	def imprimeStatusFinal(self):
		print "--------------STATUS FINAL--------------"
		print "Numero de movimentos usando a regra da mao esquerda: " , self.__num_lefthandrule
		print "Numero de movimentos aleatorios: " , self.__num_random
		print "--------------STATUS FINAL--------------"
	
class Solver(spade.Agent.Agent):
	#Classe global, que é o mapa do labirinto
	global MazeMap
	MazeMap = Mapa()
	
	
	#Filipe
	#Recebe inform com posicoes dispniveis
	#Recebe vetor com c/d/b/e
	#Escolhe posicao aleatoria
	#Envia mensagem pra efetuar movimento
	class Move(spade.Behaviour.Behaviour):
		def _process(self):
			#para ser ativado vai receber uma mensagem com as posicoes disponiveis

			#ordem das acoes
			acoes = ["cima","dir","baixo","esq"]
			
			print "Move: Comportamento Move Iniciado"
			
			msgrecebida = self._receive(True)
			
			#vetor dizendo onde pode mover 0 é parede e 1 é caminho
			posicoes = msgrecebida.getContent()
			
			print "Move: mensagem recebida: " , posicoes
			
			#Recebe qual a proxima acao a ser feita das as posicoes
			acao = MazeMap.proxDirecao(posicoes)
			
			#Envia uma mensagem de movimento para o labirinto
			msgmove = spade.ACLMessage.ACLMessage()
			msgmove.setPerformative("subscribe")
			msgmove.addReceiver(spade.AID.aid("tabuleiro@127.0.0.1",["xmpp://tabuleiro@127.0.0.1"]))
			msgmove.setContent(acoes[acao])            
			self.myAgent.send(msgmove)
			#Nao precisa receber a resposta pq sabemos que sera automaticamente sucesso
			#atualiza o mapa
			MazeMap.registraMovimento(acao)
			MazeMap.imprime()
			
			#Cria o template para o teste de objetivo
			templateTst = spade.Behaviour.ACLTemplate()
			templateTst.setPerformative("inform")
			templateTst.setSender(spade.AID.aid("tabuleiro@127.0.0.1",["xmpp://tabuleiro@127.0.0.1"]))
			tTst = spade.Behaviour.MessageTemplate(templateTst)
			
			#Cria o comportamento do teste de objetivo
			print "Move: VerifyPosition criado"
			self.myAgent.addBehaviour(self.myAgent.VerifyPosition(),tTst)
			
			#Envia mensagem de teste de objetivo
			msgteste = spade.ACLMessage.ACLMessage()
			msgteste.setPerformative("request")
			msgteste.addReceiver(spade.AID.aid("tabuleiro@127.0.0.1",["xmpp://tabuleiro@127.0.0.1"]))
			msgteste.setContent("obj")            
			self.myAgent.send(msgteste)
			print "Move: pedido de teste de objetivo enviado"
			
			#Remove esse comportamento
			self.myAgent.removeBehaviour(self.myAgent.Move())
		
	#Daniel. 
	#Recebe "inform" com 'true' ou 'false' dizendo se chegou no objetivo
	#Se é true: Faz proposta de solucao
	#Se é false: Envia mensagem pedindo sucessores
	class VerifyPosition(spade.Behaviour.Behaviour):
		def _process(self):
			print "VerifyPosition: Comportamento criado"
			
			#mensagem, pode conter true ou false
			msgrecebida = self._receive(True)
			
			valorTeste = msgrecebida.getContent()
			
			#Se chegou ao objetivo envia string com todo o caminho para o labirinto e chama o comportamento Propose
			if valorTeste == "true":
				print "VerifyPosition: É o objetivo"
				MazeMap.imprimeStatusFinal()
				#self.myAgent.removeBehaviour(self.myAgent.VerifyPosition())
			#senão pede os sucessores e chama o comportamento Move novamente
			else:
				print "VerifyPosition: Não é objetivo"
				#time.sleep(3)
				#a = raw_input("Prosseguir? ")
				#Cria template de mensagem para o comportamento Move
				
				#adiciona um template de mensagem para receber posições de movimento
				templatePos = spade.Behaviour.ACLTemplate()
				templatePos.setPerformative("inform")
				templatePos.setSender(spade.AID.aid("tabuleiro@127.0.0.1",["xmpp://tabuleiro@127.0.0.1"]))
				tPos = spade.Behaviour.MessageTemplate(templatePos)
				
				#adiciona comportamento de move
				print "VerifyPosition: Chamou comportamento Move"
				self.myAgent.addBehaviour(self.myAgent.Move(),tPos)
				
				#Envia mensagem pedindo as posicoes disponiveis
				msgsucessores = spade.ACLMessage.ACLMessage()
				msgsucessores.setPerformative("request")
				msgsucessores.addReceiver(spade.AID.aid("tabuleiro@127.0.0.1",["xmpp://tabuleiro@127.0.0.1"]))
				msgsucessores.setContent('sucessores')          
				self.myAgent.send(msgsucessores)
				print "VerifyPosition: mensagem dos sucessores enviada"
				
		#Remove esse comportamento
			self.myAgent.removeBehaviour(self.myAgent.VerifyPosition())
	
	#Filipe
	#Manda mensagem de criar e recebe essa mesma mensagem
	#
	class StartAction(spade.Behaviour.OneShotBehaviour):
		#Adiciona comportamento do move
		def _process(self):
			
			msgcria = spade.ACLMessage.ACLMessage()
			msgcria.setPerformative("request")
			msgcria.addReceiver(spade.AID.aid("tabuleiro@127.0.0.1",["xmpp://tabuleiro@127.0.0.1"]))
			msgcria.setContent('criar')            
			self.myAgent.send(msgcria)
			print "StartAction: Mensagem enviada de CRIAR"
			
			#recebe mensagem de criar para prosseguir
			msgrecebida = self._receive(True);
			
			#se a mensagem for valida:
			if len(msgrecebida.getSender().getName()) > 0:
				print "StartAction: mensagem de 'criar com sucesso' recebida: " , msgrecebida.getContent()
				
				#Cria template do Move
				
				#adiciona um template de mensagem para receber posições de movimento
				templatePos = spade.Behaviour.ACLTemplate()
				templatePos.setPerformative("inform")
				templatePos.setSender(spade.AID.aid("tabuleiro@127.0.0.1",["xmpp://tabuleiro@127.0.0.1"]))
				tPos = spade.Behaviour.MessageTemplate(templatePos)
				
				#adiciona comportamento de move
				self.myAgent.addBehaviour(self.myAgent.Move(),tPos)
				
				
				#Envia mensagem pedindo as posicoes disponiveis
				msgsucessores = spade.ACLMessage.ACLMessage()
				msgsucessores.setPerformative("request")
				msgsucessores.addReceiver(spade.AID.aid("tabuleiro@127.0.0.1",["xmpp://tabuleiro@127.0.0.1"]))
				msgsucessores.setContent('sucessores')          
				self.myAgent.send(msgsucessores)
				print "StartAction: mensagem dos sucessores enviada"
			
	class Propose(spade.Behaviour.Behaviour):
		global a
		
	#Essa função tem que adicionar todos os comportamentos que a gente fez. Se eles recebem mensagem eles já criam o template
	def _setup(self):
		
		#--------------Comportamento StartAction------------------------------#
		
		# O comportamento StartAction vai receber uma mensagem de confirmacao da criacao
		templateCria = spade.Behaviour.ACLTemplate()
		templateCria.setPerformative("inform")
		templateCria.setContent("criar")
		templateCria.setSender(spade.AID.aid("tabuleiro@127.0.0.1",["xmpp://tabuleiro@127.0.0.1"]))
		tCria = spade.Behaviour.MessageTemplate(templateCria)
		
		#adiciona o comportamento de começar o labirinto com um template de mensagem pra receber criacao
		self.addBehaviour(self.StartAction(),tCria)

#testando a classe

ip = '127.0.0.1'
teste = Solver("teste@"+ip, "secret") 
teste.start()

time.sleep(300)

teste.stop()
