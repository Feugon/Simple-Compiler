from Lexer import *
from Parser import *

source = "IF BOOP == 123 DO \n \n SET x = (123 + 4) \n PRINT x \n ENDIF \n \n "
lexer = Lexer(source)

tokenList = []

token = lexer.getToken()
while token.kind != TokenType.EOF:
    tokenList.append(token)
    print(token.kind)
    token = lexer.getToken()

print("")
parser = Parser(tokenList)
parser.parse()
print(parser.get_results())
