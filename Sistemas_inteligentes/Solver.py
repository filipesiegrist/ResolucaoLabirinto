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
	
	def __init__(self):
		#posicao atual no labirinto
		self.__position = [0,0]
		#direcoes que foram percorridas
		self.__path = []
		#todas as coordenadas dos nodos percorridos
		self.__nodes = []
		#adiciona a posicao inicial
		self.__nodes.append([0,0])
	
	#Funcao que efetua o movimento e atualiza as variaveis:
	#	path
	#	position
	#	nodes
	#Recebe Numero de 0-3 seguindo o padrao acima
	def registraMovimento(self,numdir):
		referencia = ['c','d','b','e']
		
		#adiciona o numero em path
		self.__path.append(numdir)
		
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
			
		
		#adiciona a nova coordenada na lista de nodos
		self.__nodes.append(self.__position)
	
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
		print "----------Mapa do Labirinto-----------"
		print "Posicao atual: " , self.__position
		print "Caminho percorrido: " , self.__path
		print "Nodos percorridos: " , self.__nodes
		print "-------------Fim do Mapa---------------"

	#define qual a proxima posicao que deve ir
	#recebe string com as posicoes possiveis no estilo "[c, d, b, e]"
	#retorna numero de 0-3 com a acao
	def proxDirecao(self,posicoes):
		acoes = ["0","cima","0","0","dir","0","0","baixo","0","0","esq"]
		#escolhe acao nova enquanto der caminho
		acao = randint(0,3)
		while posicoes[acao*3 +1] != '1':
			acao = randint(0,3)
			#print "Iria para " , acoes[acao] 
		print "Movendo para " , acoes[acao*3+1]
		return acao

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
			
			print "Comportamento Move Iniciado"
			
			msgrecebida = self._receive(True)
			
			#vetor dizendo onde pode mover 0 é parede e 1 é caminho
			posicoes = msgrecebida.getContent()
			
			print "mensagem recebida pelo move: " , posicoes
			
			#Recebe qual a proxima acao a ser feita das as posicoes
			acao = MazeMap.proxDirecao(posicoes)
			
			#-----------<escolha da acao a ser feita>-------------
			
			#escolhe acao nova enquanto der caminho
			# acao = randint(0,3)*3 +1
			# while posicoes[acao] != '1':
				# acao = randint(0,3)*+1
				# #print "Iria para " , acoes[acao] 
			
			# print "Movendo para " , acoes[acao]
			#-------------</escolhadeacaoaserfeita>-------------
			
			
			#Envia uma mensagem de movimento para o labirinto
			msgmove = spade.ACLMessage.ACLMessage()
			msgmove.setPerformative("subscribe")
			msgmove.addReceiver(spade.AID.aid("tabuleiro@127.0.0.1",["xmpp://tabuleiro@127.0.0.1"]))
			msgmove.setContent(acoes[acao])            
			self.myAgent.send(msgmove)
			print "enfaggot"
			#Nao precisa receber a resposta pq sabemos que sera automaticamente sucesso
			
			#normaliza os numeros das direcoes para encaixarem de 0-3
			movimento = acao
			#atualiza o mapa
			MazeMap.registraMovimento(movimento)
			MazeMap.imprime()
			#print "Estou na coordenada " , MazeMap.getPosition()
			
			#Remove esse comportamento
			self.myAgent.removeBehaviour(self.myAgent.Move())
		
	#Daniel. 
	#Recebe "inform" com 'true' ou 'false' dizendo se chegou no objetivo
	#Se é true: Faz proposta de solucao
	#Se é false: Envia mensagem pedindo sucessores
	class VerifyPosition(spade.Behaviour.Behaviour):
		def _process(self):
			print "verifica"
	
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
			print "Mensagem enviada de CRIAR"
			
			#recebe mensagem de criar para prosseguir
			msgrecebida = self._receive(True);
			
			#se a mensagem for valida:
			if len(msgrecebida.getSender().getName()) > 0:
				print "mensagem de 'criar com sucesso' recebida: " , msgrecebida.getContent()
				
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
				print "mensagem dos sucessores enviada"
			
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


		#--------------Comportamento VerifyPosition------------------------------#

		#adiciona um template de mensagem para receber posições de movimento
		#templatePos = spade.Behaviour.ACLTemplate()
		#templatePos.setPerformative("inform")
		#templatePos.setContent("criar")
		#tPos = spade.Behaviour.MessageTemplate(templatePos)
		
		#adiciona comportamento de move
		#self.addBehaviour(self.Move(),tPos)

#testando a classe

ip = '127.0.0.1'
teste = Solver("teste@"+ip, "secret") 
teste.start()

time.sleep(10)

teste.stop()
