from colorama import *
import sys

class Wrong(Exception):
	pass

class ParenError(Wrong):
	pass
	
class TokenError(Wrong):
	pass
	
class WhyAreYouHere:
	def __init__(self):
		raise Exception("What? How? Why? Just why? Why are you here?")

print(Style.BRIGHT+"Welcome to the "+Fore.BLUE+"E INTERPERATOR!!"+Style.RESET_ALL)

variables={"pi":3.14159,"e":2.71828,"errorRaiser":"poop"}
def lexer(text):
	tok = ""
	OP = {"+":"ADD","-":"SUBTRACT","*":"MULTIPLY","/":"DIVIDE","^":"POWER"}
	types = ['STR','NUMBER','BOOL']
	iS = False
	iN = False
	sP = False
	wFVN = False
	jTOW = False
	string = ""
	tmp = ""
	digits = "0123456789."
	tokens = []
	tokens.append("SOF")
	for char in text:
		tok += char
		if tok == "'" or tok == '"':
			if iS:
				if sP == True and tok == "'":
					iS = False
					tokens.append(f"STR: {string}")
					string = ""
					sP = False
				elif sP == False and tok == '"':
					iS = False
					tokens.append(f"STR: {string}")
					string = ""
				else:
					string+=tok
			else:
				if tok == "'":
					sP = True
				else:
					sP = False
				iS = True
			tok = ""
		elif tok in OP:
			tokens.append(OP[tok])
			tok = ""
		elif tok == " ":
			if iS:
				string+=tok
			elif iN:
				iN = False
				tokens.append(f"NUMBER: {tmp}")
				tmp = ""
			elif jTOW:
				jTOW = False
			elif wFVN and jTOW == False:
				tokens.append(f"NAME: {tmp}")
				tmp = ""
				wFVN = False
			tok = ""
		elif tok == "log(":
			tokens.append("LOG")
			tok = ""
		elif tok == ")":
			tokens.append("CLOSE")
			tok = ""
		elif tok[-1:] == "#":
			tokens.append(f'REFERENCE: {tok[:-1]}')
			tok = ""
		elif tok in digits:
			tmp = str(tmp)
			tok = str(tok)
			if iN:
				tmp += tok
			else:
				iN = True
				tmp += tok	
			tok = ""
		elif tok.upper() in types or tok.upper() == "NUM":
			if tok.upper() == "NUM":
				tokens.append("VAR TYPE NUMBER")
			else:
				tokens.append("VAR TYPE "+tok.upper())
			wFVN = True
			jTOW = True
			tok = ""
		elif tok == "=":
			tokens.append("EQUALS")
			tok = ""
		else:
			if iS:
				string += tok
				tok = ""
			elif iN:
				iN = False
				tokens.append(f"NUMBER: {tmp}")
				tmp = ""
			elif wFVN:
				tmp += tok
				tok = ""
			
	if iN:
		iN = False
		tokens.append(f"NUMBER: {tmp}")
		tmp = ""
	tokens.append("EOF")
	if tokens == ['SOF','EOF']:
		raise TokenError("No tokens to be found in list.")
	#print(tokens)
	return tokens

def parser(toks):
	i = 0
	ty = ['STR','BOOL','NUMBER']
	pFNV = False
	pFSV = False
	pFBV = False
	operators = ["ADD","SUBTRACT","MULTIPLY","DIVIDE","POWER"]
	try:
		while i < len(toks):
			if toks[i] != "EOF":
				if f"{toks[i]} {toks[i+1][:3]}" == "LOG STR":
					if toks[i+2] == "CLOSE":
						print(toks[i+1][5:])
					else:
						raise ParenError(f"No closing statement at log statement '{toks[i+1][5:]}'")
				elif f'{toks[i]} {toks[i+1]}' == "LOG CLOSE":
					raise WhyAreYouHere()
				elif f'{toks[i]} {toks[i+1][:9]}' == "LOG REFERENCE":
					if toks[i+2] == "CLOSE":
						rN = toks[i+1][11:]
						print(rN)
						vV = str(variables[rN])
						print(vV)
						print(str(variables[toks[i+1][11:]]))
					else:
						raise ParenError(f"No closing statement at log statement '{toks[i+1][5:]}'")
				elif toks[i] == "REFERENCE: errorRaiser":
					raise WhyAreYouHere()
				elif toks[i][:8] == "VAR TYPE":
					a = toks[i][9:]
					if a in ty:
						if a == "NUMBER":
							pFNV = True
						elif a == "BOOL":
							pFBV = True
						elif a == "STR":
							pFSV = True
					else:
						raise TypeError("Not valid variable type.")
					if toks[i+1]:
						name = toks[i+1][5:]
						if toks[i+2] and toks[i+3]:
							if pFNV:
								value = float(toks[i+3][8:])
								pFNV = False
							elif pFSV:
								value = toks[i+3][5:]
								pFSV = False
							elif pFBV:
								value = bool(toks[i+3][6:])
								pFBV = False
						variables[name] = value
					else:
						raise SyntaxError("Declared type, but not name.")
				elif toks[i+1] in operators:
					if toks[i][11:] in variables:
						a = variables[toks[i][11:]]
					else:
						a = float(toks[i][8:])
					if toks[i+2][11:] in variables:
						b = variables[toks[i+2][11:]]
					else:
						b = float(toks[i+2][8:])
					if toks[i+1] == "ADD":
						print(a+b)
					elif toks[i+1] == "SUBTRACT":
						print(a-b)
					elif toks[i+1] == "MULTIPLY":
						print(a*b)
					elif toks[i+1] == "DIVIDE":
						print(a/b)
					elif toks[i+1] == "POWER":
						e = a
						f = b
						print(pow(e,f))
				else:
					pass
			i+=1
	except Exception as e:
		print(e)
	
def run():
	if sys.argv[1]:
		b = open(sys.argv[1],'r').read()
		e = lexer(b)
		f = parser(e)
	else:
		while True:
			b = input(">>> ")
			b = str(b)
			e = lexer(b)
			f = parser(e)


run()
