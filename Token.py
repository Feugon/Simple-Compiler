import enum

class Token:
	def __init__(self,text, kind):
		self.text = text
		self.kind = kind

	@staticmethod
	def checkIfKeyword(tokenText):
		for kind in TokenType:
			if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
				return kind
		return None

class TokenType(enum.Enum):
	EOF = -1
	NEWLINE = 0
	NUMBER = 1
	IDENT = 2
	STRING = 3
	# Keywords.
	SET = 101
	GOTO = 102
	PRINT = 103
	INPUT = 104
	LET = 105
	IF = 106
	DO = 107
	ENDIF = 108
	WHILE = 109
	REPEAT = 110
	ENDREPEAT = 111
	# Operators.
	EQ = 201
	PLUS = 202
	MINUS = 203
	MULTIPLY = 204
	DIVIDE = 205
	EQEQ = 206
	NOTEQ = 207
	LT = 208
	LTEQ = 209
	GT = 210
	GTEQ = 211
	LP = 212       # left parentheses
	RP = 213	   # right parentheses
	INC = 214	   # ++
	DEC = 215	   # --
	PLUSEQ = 216
	MINUSEQ = 217
