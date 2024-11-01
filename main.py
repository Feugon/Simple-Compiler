from Lexer import *
from Parser import *

source = "SET x = 10 + 6 * 20 - (10+5) \nPRINT x + 10\nIF x == 10 DO \nPRINT x\nENDIF"
lexer = Lexer(source)

tokenList = []

token = lexer.getToken()
while token.kind != TokenType.EOF:
    tokenList.append(token)
    token = lexer.getToken()

print("\n" + source)
parser = Parser(tokenList)
parser.parse()


for statement in parser.get_results():
    print(statement)