from Lexer import *

source = "IF 123"
lexer = Lexer(source)

token = lexer.getToken()
while token.kind != TokenType.EOF:
    print(token.kind)
    token = lexer.getToken()