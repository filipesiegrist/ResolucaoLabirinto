#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  MazeHost.py
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
from LabirintoModelo import Labirinto

#Agente que fornece os serviços do labirinto
class MazeHost(spade.Agent.Agent):
	
	#Comportamento #1: Informa se a posição atual é válida ou não
	#Comportamento #2: Informa se a ação (up,down,left ou right) foi aceita ou recusada
	class MazeBhv(spade.Behaviour.Behaviour):
		
		def onStart(self):
			#Labirinto global
			self.Maze = Labirinto()
			self.Maze.imprime();
		
		def _process(self):
			msg = self._receive(True,5)
			if msg:
				conteudo = msg.getContent()
				performativa = msg.getPerformative()
				#mensagem de resposta
				novamsg = spade.ACLMessage.ACLMessage()
				#só aceita performativas de requisição
				if performativa == "request":
					
					#Teste de objetivo
					if conteudo == "test":
						if Maze.testeSaida() == False:
							novamsg.setPerformative("refuse")
						else:
							novamsg.setPerformative("agree")
						novamsg.setContent("test")
						self.myAgent.send(novamsg)
						
					#Teste de subida
					elif conteudo == "up":
						if Maze.up() == False:
							novamsg.setPerformative("refuse")
						else:
							novamsg.setPerformative("agree")
						novamsg.setContent("up")
						self.myAgent.send(novamsg)
						
					#Teste de descida
					elif conteudo == "down":
						if Maze.down() == False:
							novamsg.setPerformative("refuse")
						else:
							novamsg.setPerformative("agree")
						novamsg.setContent("down")
						self.myAgent.send(novamsg)
						
					#Teste de esquerda
					elif conteudo == "left":
						if Maze.left() == False:
							novamsg.setPerformative("refuse")
						else:
							novamsg.setPerformative("agree")
						novamsg.setContent("left")
						self.myAgent.send(novamsg)
						
					#Teste de direita
					elif conteudo == "right":
						if Maze.right() == False:
							novamsg.setPerformative("refuse")
						else:
							novamsg.setPerformative("agree")
						novamsg.setContent("right")
						self.myAgent.send(novamsg)
						
					else:
						print "Invalid message."
						
				else:
					print "Wrong performative received."
					
			else:
				print "MazeHost awaiting command."
				
	def _setup(self):
		template = spade.Behaviour.ACLTemplate()
		template.setSender(spade.AID.aid("a@127.0.0.1",["xmpp://a@127.0.0.1"]))
		t = spade.Behaviour.MessageTemplate(template)
		self.addBehaviour(self.MazeBhv(),t)
		
print "Comecou"
Agent = MazeHost("maze@127.0.0.1","secret")
Agent.start()
time.sleep(30)
Agent.stop()

