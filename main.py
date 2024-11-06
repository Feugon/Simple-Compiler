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
    print(statement)


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
add some way to interact with the variable in the for loops (so if we define var as i for the looping portion we should
be able to use i the same way we use a regular variable, and then we should delete it)

features:
-functions

"""