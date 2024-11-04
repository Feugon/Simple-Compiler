from Lexer import *
from Parser import *
from Emitter import *

source = "SET x = 12\nSET y = 10\nIF x == y DO\nSET z = \"123\"\nPRINT z\nENDIF "
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
code quality:
parentheses handling in emitter
currently no way to tell if we are printing a variable or a string with var name
in parse_var_change: we should handle having a string there, i.e. not allow numerical vars become strings (or do some weird casting <bad>?)
documentation/comments

features:
-for loops
-functions
-use external files to input and output code

"""