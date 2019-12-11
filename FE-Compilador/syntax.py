#!/usr/bin/python3

from lex import Token

# gram       = nterm -> [derivations]
grammar = {
"I"   : [[("rwd","programa"),("nterm","B")]],
"B"   : [[("rwd","inicio"),("nterm","D"),("nterm","C"),("rwd","fim")]],
"D"   : [[("nterm","T"),("idt","idt"),("pnt",";")],[]],
"T"   : [[("rwd","int")],[("rwd","char")],[("rwd","real")]],
"C"   : [[("rwd","se"),("nterm","CO"),("rwd","entao"),("nterm","B"),("nterm","C")],[("rwd","enquanto"),("nterm","CO"),("nterm","B"),("nterm","C")],[("nterm","E"),("nterm","C")],[]],
"CO"  : [[("pnt","("),("nterm","X"),("nterm","R"),("nterm","X"),("pnt",")")]],
"E"   : [[("nterm","A"),("pnt",";")]],
"A"   : [[("idt","idt"),("opt","="),("nterm","M")]],
"M"   : [[("pnt","("),("nterm","M11"),("pnt",")")],[("nterm","X")]],
"M11" : [[("nterm","M21"),("nterm","M12")]],
"M12" : [[("opt","+"),("nterm","M21"),("nterm","M12")],[("opt","-"),("nterm","M21"),("nterm","M12")],[]],
"M21" : [[("nterm","M"),("nterm","M22")]],
"M22" : [[("opt","*"),("nterm","M"),("nterm","M22")],[("opt","/"),("nterm","M"),("nterm","M22")],[]],
"X"   : [[("idt","idt")],[("cst","cst")]],
"R"   : [[("rlp","==")],[("rlp","<>")],[("rlp","<=")],[("rlp",">=")],[("rlp","<")],[("rlp",">")]]
}

term = {
"programa" : " ", 
"inicio"   : " ",
"fim"      : " ",
"idt"      : " ",
"int"      : " ",
"char"     : " ",
"real"     : " ",
"se"       : " ",
"entao"    : " ",
"enquanto" : " ",
"="        : " ",
"cst"      : " ",
"+"        : " ",
"-"        : " ",
"*"        : " ",
"/"        : " ",
"=="       : " ",
"<>"       : " ",
">="       : " ",
"<="       : " ",
">"        : " ",
"<"        : " ",
"("        : " ",
")"        : " ",
";"        : " ",
"$"        : " ",
}

def print_table_line(nterm) :
	print("|",nterm,"|",end="")
	for k in term.keys():
#		print(term[k],"[",k,"]|",end="")
		print(term[k] + "|",end="")
		term[k] = " "
	print()

def print_grammar():
	for nterm in grammar.keys():
		print(nterm,end=" -> ")
		for derv in grammar[nterm]:
			for alfa in derv :
				print(alfa[1],end=" ")
			print("",end=" | ")
		print()

def first(nterm):
	if nterm not in grammar.keys():
		return [nterm]
	else:
		res = []
		for derv in grammar[nterm]:
			if   not derv:
				res.append(None)
			for alfa in derv:
				if alfa[0] != "nterm":
					res.append(alfa[1])
					break
				else:
					aux = first(alfa[1])
					if None in aux:
						res += aux
					else:
						res += aux
						break
		return list(set(res))

def follow(nterm):
	res = []
	if    nterm not in grammar.keys():
		return res
	elif nterm == "I":
		res.append("$")
	for gkeys in grammar.keys():
		for derv in grammar[gkeys]:
			for j in range(0,len(derv)):
				if derv[j][1] == nterm:
					if j == len(derv) - 1:
						if gkeys != nterm:
							for k in follow(gkeys):
								if k not in res:
									res.append(k)
					else:
						for k in first(derv[j + 1][1]):
							if k not in res:
								res.append(k)#
						if None in res or j == len(derv):
							for k in follow(gkeys):
								if k not in res:
									res.append(k)
	try:
		res.remove(None)
	except:
		pass
	return res

def create_table():
	producao = 1

	for nterm in grammar.keys():
		for derv in grammar[nterm]:
			if derv:
				for xxx in first(derv[0][1]):
#					print(xxx)
					term[xxx] = str(producao)
			else:
				for xxx in follow(nterm):
#					print(xxx)
					term[xxx] = str(producao)
			producao += 1
		print_table_line(nterm)

class ListTokens():
	def __init__(self,tokens):
		self.current = 0
		self.tk_list = tokens

	def name(self):
		return self.tk_list[self.current].name

	def attribute(self):
		if   self.tk_list[self.current].name == "idt":
			return "idt"
		elif self.tk_list[self.current].name == "cst":
			return "cst"

		return self.tk_list[self.current].attribute

	def next(self):
		if self.current < len(self.tk_list) - 1:
			self.current += 1
		print(self.tk_list[self.current - 1].attribute,"->",self.tk_list[self.current].attribute)

class ACPredictible():

	def run(self,tokens):
		print("\nSyntax Analyzer :\n")
		self.token = ListTokens(tokens)
		create_table()
		


#def derivation():
#	for der in gram[nterm]:
#		for gsimbol in der:
#			
