from Lexer import *
from Parser import *
from Emitter import *

source = "PRINT 10\nPRINT \"Hi\"\nSET x = 10\nPRINT x "
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


emitter = Emitter(parser.get_results())
emitter.emit_tree()
print(emitter.return_code())


"""
List of things that should be implemented/fixed:
------------------------------------------------
parentheses handling in emitter
assignment to existing variables
currently no way to tell if we are printing a variable or a string with var name

"""