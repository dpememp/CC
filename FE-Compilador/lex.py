#!/usr/bin/python3

import sys

class Token():
	def __init__(self,ttype,attribute,line,col):
		self.name      = ttype
		# cnst  = constante
		# ident = identificador
		# relop = operador relacional
		# rword = palavra reservada
		# pont  = pontuação
		# op    = operador
		self.attribute = attribute
		self.line      = line
		self.col       = col
	def print_token(self):
		print(self.name,self.attribute,self.line,self.col)

class STDiagram():
	def __init__(self,afd):
		fd         = open(afd,"r")
		lines      = fd.readlines()
		self.tt    = [] # transition table
		self.final = {} # final states


		for l in lines:
			aux = {}
			l   = l.strip("\n")
			l   = l.split(",")
			i   = 1

			for j in range(39,46):
				aux[chr(j)] = int(l[i])
				i += 1
			for j in range(48,58):
				aux[chr(j)] = int(l[i])
				i += 1
			for j in range(59,63):
				aux[chr(j)] = int(l[i])
				i += 1
			for j in range(91,94):
				aux[chr(j)] = int(l[i])
				i += 1
			for j in range(97,123):
				aux[chr(j)] = int(l[i])
				i += 1
			self.tt.append(aux)
			if l[i] != "0":
				self.final[str(len(self.tt) - 1)] = l[i]
#				aux['class'] = l[i]
#				self.final.append(len(self.tt) - 1)

		print(self.final)

	def is_final(self,state):
		if str(state) in self.final.keys():
			return True
		return False

class SBTable():
	def __init__(self):
		self.st    = [] # simbol table
	
	def add_element(self,value):
		for i in range(0,len(self.st)):
			if self.st[i] == value:
				return i
		self.st.append(value)
		return (len(self.st) - 1)

class Tokenizer():
	def __init__(self,file_name):
		self.source_code      = file_name
		self.buffer           = []
		self.transition_table = STDiagram("./Tables/t_afd.csv")
		self.symbol_table     = SBTable()

	def run(self):
		tokens      = []
		fd          = open(self.source_code,"r")
		self.buffer = fd.read()

		start = None
		end   = None
		state = 0
		line  = 1
		col   = 0

		for i in range(len(self.buffer) - 1):
		# Setar "ponteiros"
			head = self.buffer[i]
			prox = self.buffer[i+1]
#			print(head,"and",prox)
# ----------------------------------------------------------------------------------------------------------------------------------------------------
			if start == None and head != " " and head != "\t" and head != "\n":
				start = i
			if head == " " or head == "\t":
				col += 1
				if start != None:
					if self.transition_table.is_final(state):
						end = i
						col_start = col + 1 - (end - start)
						if self.transition_table.final[str(state)] == "idt":
							index = self.symbol_table.add_element(self.buffer[start:end + 1].replace(" ","").replace("\n","").replace("\t",""))
							tk = Token(self.transition_table.final[str(state)],index,line,col_start)
						else:
							tk = Token(self.transition_table.final[str(state)],self.buffer[start:end + 1].replace(" ","").replace("\n","").replace("\t",""),line,_start)
						tokens.append(tk)
						tk.print_token()

#						print("1",self.buffer[start:end + 1].replace(" ","").replace("\n","").replace("\t",""))
						state  = 0
						start  = None
						end    = None 
					else:
						print("1 Error at",line,col)
						break
				else:
					continue
			elif head == '\n':
				if start != None:
					if self.transition_table.is_final(state):
						end = i
						col_start = col + 1 - (end - start)
						if self.transition_table.final[str(state)] == "idt":
							index = self.symbol_table.add_element(self.buffer[start:end + 1].replace(" ","").replace("\n","").replace("\t",""))
							tk = Token(self.transition_table.final[str(state)],index,line,col_start)
						else:
							tk = Token(self.transition_table.final[str(state)],self.buffer[start:end + 1].replace(" ","").replace("\n","").replace("\t",""),line,col_start)
						tokens.append(tk)
						tk.print_token()
#						print("2",self.buffer[start:end + 1].replace(" ","").replace("\n","").replace("\t",""))
						state  = 0
						start  = None
						end    = None
					else:
						print("2 Error at",line,col)
						break
				else:
					line += 1
					col   = 0
					continue
				
# ----------------------------------------------------------------------------------------------------------------------------------------------------
		# Usar diagrama para determinar estados
#			print(state,end=" -> ")
			state     = self.transition_table.tt[state][head]
#			print(state)
			if self.transition_table.is_final(state):
				end = i
			if prox == " " or prox == "\t" or prox == "\n":
				new_state = -1
			else:
				new_state = self.transition_table.tt[state][prox]
#			print(prox,"+",state,"=",new_state)

			# Reconheceu o mais longo
			if new_state == -1:
				if end != None: # state hit final at some point
					col_start = col + 1 - (end - start)
					if self.transition_table.final[str(state)] == "idt":
						index = self.symbol_table.add_element(self.buffer[start:end + 1].replace(" ","").replace("\n","").replace("\t",""))
						tk = Token(self.transition_table.final[str(state)],index,line,col_start)
						tk.print_token()
					else:
						tk = Token(self.transition_table.final[str(state)],self.buffer[start:end + 1].replace(" ","").replace("\n","").replace("\t",""),line,col_start)
					tokens.append(tk)
					tk.print_token()
##					print("3",self.buffer[start:end + 1].replace(" ","").replace("\n","").replace("\t",""))
					state  = 0
					start  = None
					end    = None
#					lexema = Token("",self.buffer[start:head + 1],line,col)
				else :
					print("3 Error at",line,col)
					
			col += 1
		return tokens
