from Lexer import *
from Parser import *
from Emitter import *

# reads the input file
with open('input.txt', 'r') as file:
    source = file.read()

# clears the output file, so if there is an error the previous compiled code won't show
with open('output.txt', 'w') as file:
    file.write("")


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
    print(0,statement)


emitter = Emitter(parser.get_results())
emitter.emit_tree()


# writes the output file
with open('output.txt', 'w') as file:
    file.write("")
    file.write(emitter.return_code())



"""
List of things that should be implemented/fixed:
------------------------------------------------
code quality:
nested for-loops (everything breaks in them) 
There is a bug with ENDFUNCTION token (should not be in the parse tree, but is)

features:
-functions
"""