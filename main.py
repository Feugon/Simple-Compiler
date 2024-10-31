from Lexer import *
from Parser import *

source = "IF 24 * 7 == 123 + 5 DO \n \n SET x = (123 + 4) \n PRINT 234 * 5 \n ENDIF \n \n "
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
