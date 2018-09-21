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

class Solver(spade.Agent.Agent):
	#vetor com coordenadas [0] - x
	#                      [1] - y
	global position
	position = []
	#vetor com o caminho percorrido
	# Posição:
	# 0	c
	# 1	d
	# 2	b
	# 3	e
	global path 
	path = []
	
	#Filipe
	#Recebe inform com posicoes dispniveis
	#Recebe vetor com c/d/b/e
	#Escolhe posicao aleatoria
	#Envia mensagem pra efetuar movimento
	class Move(spade.Behaviour.Behaviour):
		def _process(self):
			#para ser ativado vai receber uma mensagem com as posicoes disponiveis
			
			
			
			print "movendo"
			#envia request com posicoes disponiveis
			msg = spade.ACLMessage.ACLMessage()
			msg.setPerformative("request")
			msg.addReceiver(spade.AID.aid("tabuleiro@127.0.0.1",["xmpp://tabuleiro@127.0.0.1"]))
			msg.setSender('solver')
			#acao e a posicao aleatoria
			acoes = ['c','b','e','d']
			acao = acoes[randint(0,3)]
			msg.setContent(acao)         
			self.myAgent.send(msg)
		
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
			if len(msg.getSender().getName()) > 0:
				print "mensagem de 'criar com sucesso' recebida"
				#envia mensagem pedindo as posicoes
				msgsucessores = spade.ACLMessage.ACLMessage()
				msgsucessores.setPerformative("request")
				msgsucessores.addReceiver(spade.AID.aid("tabuleiro@127.0.0.1",["xmpp://tabuleiro@127.0.0.1"]))
				msgcria.setContent('sucessores')
			
	class Propose(spade.Behaviour.Behaviour):
		global a
		
	#Essa função tem que adicionar todos os comportamentos que a gente fez. Se eles recebem mensagem eles já criam o template
	def _setup(self):
		
		#--------------Comportamento StartAction------------------------------#
		
		# O comportamento StartAction vai receber uma mensagem de confirmacao da criacao
		templateCria = spade.Behaviour.ACLTemplate()
		templateCria.setPerformative("inform")
		templateCria.setContent("criar")
		tCria = spade.Behaviour.MessageTemplate(templateCria)
		
		#adiciona o comportamento de começar o labirinto com um template de mensagem pra receber criacao
		self.addBehaviour(self.StartAction(),tCria)


		#--------------Comportamento VerifyPosition------------------------------#

		#adiciona um template de mensagem para receber posições de movimento
		templatePos = spade.Behaviour.ACLTemplate()
		templatePos.setPerformative("inform")
		templatePos.setSender(spade.AID.aid("tabuleiro@127.0.0.1",["xmpp://tabuleiro@127.0.0.1"]))
        templatePos.setContent("criar")
		tPos = spade.Behaviour.MessageTemplate(templatePos)
		
		#adiciona comportamento de move
		self.addBehaviour(self.Move(),tPos)

#testando a classe

ip = '127.0.0.1'
teste = Solver("teste@"+ip, "secret") 
teste.start()

time.sleep(10)

teste.stop()
