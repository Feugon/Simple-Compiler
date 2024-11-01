from Token import *
import sys



class Emitter:

    def __init__(self, parseTree):
        self.parseTree = parseTree
        self.code = ""
        self.symbolsTable = {}

        # this represents libraries and int main etc. that we need to run a c++ program
        self.outlineTop = ""
        self.outlineBot = ""

    def emit_tree(self):
        """ Iter through every statement in parse tree and emit the necessary code"""
        for statement in self.parseTree:
            if statement["type"] == "SET":
                pass # handle set statement...
            elif statement["type"] == "PRINT":
                pass # handle print statement...
            elif statement["type"] == "IF":
                pass # handle IF statement...
            else:
                self.error("Unsupported Statement Type")


    def emit_SET(self):
        """Emits SET statement"""
        pass

    def emit_PRINT(self):
        """Emits PRINT statement"""
        pass

    def emit_IF(self):
        """Emits IF statement"""
        pass

    def emit(self, statement):
        """ Appends a statement to the code"""
        self.code += statement

    def return_code(self):
        """ Returns the C++ code as a string"""
        return self.outlineTop + self.code + self.outlineBot

    def error(self, message):
        """Exits the code and sends an error message."""
        sys.exit("Emitter Error: " + message)
