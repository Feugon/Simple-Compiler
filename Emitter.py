from Token import *
import sys



class Emitter:

    def __init__(self, parseTree):
        self.parseTree = parseTree
        self.code = ""
        self.symbolsTable = {}

        # this represents libraries and int main etc. that we need to run a c++ program
        self.outlineTop = "#include <iostream>\n#include <string>\n \nint main()\n{\n"
        self.outlineBot = "\n\treturn 0;\n}"

    def emit_tree(self):
        """ Iter through every statement in parse tree and emit the necessary code"""
        for statement in self.parseTree:
            if statement["type"] == "SET":
                compiledCode = self.emit_SET(statement)
                self.emit(compiledCode)
            elif statement["type"] == "PRINT":
                pass # handle print statement...
            elif statement["type"] == "IF":
                pass # handle IF statement...
            else:
                self.error("Unsupported Statement Type")


    def emit_SET(self,statement):
        """Emits SET statement"""
        value = self.emit_value(statement["value"])
        var_name = statement["variable"]
        var_type = ""

        if value[0].isdigit():
            # easier to use float for all numerical vars than identifying them
            var_type = "float"
        elif value[0] == "\"":
            var_type = "std::string"

        self.symbolsTable[var_name] = var_type
        return f"{var_type} {var_name} = {value};"

    def emit_PRINT(self):
        """Emits PRINT statement"""
        pass

    def emit_IF(self):
        """Emits IF statement"""
        pass

    def emit_value(self, value):
        if isinstance(value,str):
            if value.isdigit():
                return value
            else:
                return f'\"{value}\"'  # puts quotes around the strings
        elif isinstance(value,dict):
            operator = value["operator"]
            left = self.emit_value(value["left"])
            right = self.emit_value(value["right"])
            return f"{left} {operator} {right}"


    def emit(self, statement):
        """ Appends a statement to the code"""
        self.code += "\t" + statement + "\n"

    def return_code(self):
        """ Returns the C++ code as a string"""
        return self.outlineTop + self.code + self.outlineBot

    def error(self, message):
        """Exits the code and sends an error message."""
        sys.exit("Emitter Error: " + message)
