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
	#Envia request com posicoes disoniveis
	#Recebe vetor com c/d/b/e
	#Escolhe posicao aleatoria
	class Move(spade.Behaviour.Behaviour):
		def _process(self):
			#envia request com posicoes disponiveis
			msg = spade.ACLMessage.ACLMessage()
			msg.setPerformative("request")
			msg.addReceiver(spade.AID.aid("tabuleiro@127.0.0.1",["xmpp://tabuleiro@127.0.0.1"]))
		
	#Daniel. 
	#Envia request para o labirinto (ver como ele interpreta)
	#Recebe "inform" com 'true' ou 'false'
	class VerifyPosition(spade.Behaviour.Behaviour):
		def _process(self):
			print "verifica"
		
	class Start(spade.Behaviour.OneShotBehaviour):
		def _process(self):
			template = spade.Behaviour.ACLTemplate()
			template.setPerformative("inform")
			t = spade.Behaviour.MessageTemplate(template)
			self.myAgent.addBehaviour(teste.resposta(),t) 
			msg = spade.ACLMessage.ACLMessage()
			msg.setPerformative("request")
			#msg.addReceiver(spade.AID.aid("tabuleiro@127.0.0.1"))
			msg.addReceiver(spade.AID.aid("tabuleiro@127.0.0.1",["xmpp://tabuleiro@127.0.0.1"]))
			msg.setContent('criar')            
			self.myAgent.send(msg)
			print "Mensagem enviada de CRIAR"
			
	class Propose(spade.Behaviour.Behaviour):
		global a
		
	#Essa função tem que adicionar todos os comportamentos que a gente fez. Se eles recebem mensagem eles já criam o template
	def _setup(self):
		self.enderecohost = "tabuleiro@127.0.0.1"
		
		#adiciona o comportamento de começar o labirinto
		self.addBehaviour(self.Start())
		
		#adiciona um template de mensagem para receber posições de movimento
		templatePos = spade.Behaviour.ACLTemplate()
		templatePos.setSender(spade.AID.aid(self.enderecohost,["xmpp://" , self.enderecohost]))
		tPos = spade.Behaviour.MessageTemplate(templatePos)
		
		#adiciona comportamento de move
		self.addBehaviour(self.Move(),tPos)

#testando a classe

ip = '127.0.0.1'
teste = Solver("teste@"+ip, "secret") 
teste.start()

time.sleep(10)

teste.stop()
