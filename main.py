from Lexer import *
from Parser import *

source = "SET x = 10 \n SET y = 20 \n SET z = x + y"
lexer = Lexer(source)

tokenList = []

token = lexer.getToken()
while token.kind != TokenType.EOF:
    tokenList.append(token)
    token = lexer.getToken()

print("\n" + source)
parser = Parser(tokenList)
parser.parse()
print(parser.get_results())
