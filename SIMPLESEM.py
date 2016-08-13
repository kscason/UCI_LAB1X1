#!/usr/bin/python

"""
SIMPLESEM
Interpreter for SIMPLESEM Language
UCI CSE 141
9 August 2016
Kaitlyn Cason
"""

from sys import argv
import re

"""Rules to create tokens needed for lexical analysis
	in accordance with SIMPLESEM grammar."""

keywords = {'set', 'write', 'read', 'halt', 'jump', 'jumpt'}
token_pattern = r"""
			(?P<number>([0]|[1-9][0-9]*)) 		
			|(?P<comma>[,])
			|(?P<factop>(\(|\)|[D]\[|\]))			
			|(?P<multop>(\*|\/|\%))
			|(?P<addop>(\+|\-))
			|(?P<cmpop>([!=<>][=]|[<>]))
			|(?P<space>\s+)
			|(?P<letters>[a-zA-Z]+) 			
			"""

"""SIMPLESEM opens the given file and sends each statement 
	to be processed. One SIMPLESEM statement per line in 
	accordance to input format."""
class SIMPLESEM:
	def __init__(self, filename):
		with open(filename) as f:
			self.process(f.read())

	def process(self, statement):
		lex = LEXANALYZER()
		lex.lexer(statement)

"""TokenizerException to catch any accidental mistakes and errors."""
class TokenizerException(Exception): pass

"""LEXANALYZER performs the lexical analysis. Takes a file string
	and splits into keywords, symbols, and expressions. These tokens
	will eventually be sent to a PARSER to identify non-terminals"""
class LEXANALYZER(object):
	def __init__(self):
		pass

	def lexer(self, to_parse):
		#Create token regex by given token_pattern
		token_re = re.compile(token_pattern, re.VERBOSE)

		#Identify & tokenize keywords, symbols, and expressions
		token_list = []
		for tok in self.tokenize(to_parse, token_re):
			#if the token is not a space
			if tok[0] != 'space':
				token_list.append(tok)
			if tok[0] == 'eos':
				print "NEW STATEMENT"
		parser = PARSER(token_list)
		parser.parse()

	def tokenize(self, text, rules):
		#Create a scanner for token rules
		scan = rules.scanner(text)

		#Attempt to scan through text statement and group matches into tokens
		try:
			while True:
				m = scan.match()#rules.match(text, pos)
				if not m: 
					break
				tokname = m.lastgroup
				tokvalue = m.group(tokname)
				if tokname == 'letters' and tokvalue in keywords:
					tokname = tokvalue
				yield tokname, tokvalue
		except EOFError:
			pass #ignore an EOF error
		except SyntaxError:
			raise TokenizerException('SyntaxError: Tokenizer stopped!')

"""ParserException to catch any accidental mistakes and errors."""
class ParserException(Exception): pass

"""PARSER applies looping and recursion to correctly parse SIMPLESEM
	grammar rules. Takes a SIMPLESEM program and identifies all non-
	terminals as we parse through the grammar. Non-terminals are printed
	to standard output line by line sequentially as they are entered."""
class PARSER(object):
	def __init__(self, toklist):
		self.toklist = toklist

	def eatToken(self):
		#"Eat" the current token by removing it from the list.
		del self.toklist[0]

	def getNextToken(self):	
		#Returns the token type of the next token to be processed.
		return self.toklist[0][0]

	def parse(self):
		print "Program"
		
		#<Statement>	
		self.parseS()

		#{<Statement>}	:: Keep processing statements until no more tokens	
		while len(self.toklist) is not 0:
			self.parseS()

	def parseS(self):
		print "Statement"
		#<Set> | <Jump> | <Jumpt> | halt
		nextok_type = self.getNextToken()
		if nextok_type == 'halt':				#halt
			self.eatToken()
		elif nextok_type == 'set':				#<Set>
			self.parseSt()
		elif nextok_type == 'jump':				#<Jump>
			self.parseJ()
		elif nextok_type == 'jumpt':			#<Jumpt>
			self.parseJt()
		else:									#Simple syntax error checking
			raise ParserException('SyntaxError: Statement not correctly formatted!')

	def parseSt(self):
		print "Set"

		self.eatToken()							#set

		#(write|<Expr>)
		if self.getNextToken() == 'write':		#write
			self.eatToken()
		else:									#<Expr>
			self.parseE()

		self.eatToken()							# ,

		#(read |<Expr>)
		if self.getNextToken() == 'read':		#read
			self.eatToken()
		else:									#<Expr>
			self.parseE()

	def parseJ(self):
		print "Jump"
		#jump <Expr>
		self.eatToken()							#jump
		self.parseE()							#<Expr>

	def parseJt(self):
		print "Jumpt"
		#jumpt <Expr>, <Expr> (!= | == | > | < | >= |<=) <Expr>
		self.eatToken()							#jumpt
		self.parseE()							#<Expr>

		self.eatToken()							# ,

		self.parseE()							#<Expr>
		self.eatToken()							#(!= | == | > | < | >= |<=)
		self.parseE()							#<Expr>

	def parseE(self):
		print "Expr"
		
		self.parseT()							#<Term>

		#{(+|-)<Term>}
		while self.getNextToken() == 'addop':	#(+|-)	
			self.eatToken()						
			self.parseT()						#<Term>

	def parseT(self):
		print "Term"

		self.parseF()							#<Factor>

		#{(*|/|%)<Factor>}
		while self.getNextToken() == 'multop':	#(*|/|%)
			self.eatToken()						
			self.parseF()						#<Factor>

	def parseF(self):
		print "Factor"
		#<Number> | D[ <Expr> ] | ( <Expr> )
		nextok_type = self.getNextToken()
		if nextok_type == 'factop':				#D[ or (
			self.eatToken()
			self.parseE()						#<Expr>
			self.eatToken()						#] or )
		else:									#<Number>
			self.parseN()

	def parseN(self):
		print "Number"
		#0 | (1..9){0..9}
		self.eatToken()

		
def main():
	try: 
		FILE = argv[1]
	except:
		parser.error("Error: Missing filename.")
	try:
		generator = SIMPLESEM(FILE)
	except IOError as e:
		errno, strerror = e.args
		parser.error("I/O error({0}): {1}".
					format(errno,strerror))

if __name__ == "__main__":
	main()