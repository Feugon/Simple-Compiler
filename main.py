from Lexer import *
from Parser import *

source = "IF BOOP == 123 DO \n 123 \n ENDIF"
lexer = Lexer(source)

tokenList = []

token = lexer.getToken()
while token.kind != TokenType.EOF:
    tokenList.append(token)
    print(token.kind)
    token = lexer.getToken()


print("\n")
parser = Parser(tokenList)
parser.parse()
print(parser.get_results())
