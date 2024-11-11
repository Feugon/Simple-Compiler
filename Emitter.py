from Token import *
import sys



class Emitter:

    def __init__(self, parseTree):
        self.parseTree = parseTree
        self.code = ""
        self.symbolsTable = {}
        self.indents = 1
        # this represents libraries  that we need to run a c++ program
        self.outlineTop = "#include <iostream>\n#include <string>\n"
        self.outlineBot = "\n\treturn 0;\n}"

    def emit_statement(self,statement):
        """Emits statement based on their types"""
        if statement["type"] == "SET":
            compiledCode = self.emit_SET(statement)
            return compiledCode
        elif statement["type"] == "PRINT":
            compiledCode = self.emit_PRINT(statement)
            return compiledCode
        elif statement["type"] == "IF":
            compiledCode = self.emit_IF(statement)
            return compiledCode
        elif statement["type"] == "VAR CHANGE":
            compiledCode = self.emit_var_change(statement)
            return compiledCode
        elif statement["type"] == "REPEAT":
            compiledCode = self.emit_repeat(statement)
            return compiledCode
        elif statement["type"] == "FUNCTION":
            compiledCode = self.emit_function(statement)
            self.outlineTop += compiledCode
            return ""
        elif statement["type"] == "CALL":
            compiledCode = self.emit_call(statement)
            return compiledCode
        else:
            self.error("Unsupported Statement Type")

    def emit_tree(self):
        """Emits the entire parse tree"""
        for statement in self.parseTree:
            compiledCode = self.emit_statement(statement)
            self.emit(compiledCode)

    def emit_SET(self,statement):
        """Emits SET statement"""
        value = self.emit_value(statement["value"])
        var_name = statement["variable"]
        var_type = ""

        if value[0].isdigit() or value[0] == "(":
            # easier to use float for all numerical vars than identifying them
            var_type = "float"
        elif value[0] == "\"":
            var_type = "std::string"

        self.symbolsTable[var_name] = var_type
        return f"{var_type} {var_name} = {value};"

    def emit_PRINT(self, statement):
        """Emits PRINT statement"""
        value = None
        if "value" in statement:
            value = self.emit_value(statement["value"])
        elif "identifier/expression" in statement:
            value = self.emit_value(statement["identifier/expression"])

        if not value:
            self.error("Expected a value to print")

        return f"std::cout << {value} << std::endl;"


    def emit_IF(self,statement):
        """Emits IF statement"""

        condition = self.emit_value(statement["condition"])
        output = f"if ({condition}) {{"

        self.indents += 1
        for line in statement["body"]:
            if isinstance(line, TokenType):  # this checks for ENDIF token (a tad hacky)
                break
            output += "\n" + ("\t" * self.indents) + self.emit_statement(line)

        output += "\n" + "\t" * (self.indents - 1) + "}"
        self.indents -= 1

        return output

    def emit_repeat(self,statement):

        times = statement["times"]
        var_name = statement["var"]
        self.symbolsTable[var_name] = "float"
        output = f"for (int {var_name} = 0; {var_name} < {times}; {var_name}++) {{"
        #output += self.emit_body(statement)
        self.indents += 1
        for line in statement["body"]:
            if isinstance(line, TokenType):  # this checks for ENDIF token (a tad hacky)
                break
            output += "\n" + ("\t" * self.indents) + self.emit_statement(line)


        self.indents -= 1

        del self.symbolsTable[var_name]

        return output + "\n" + ("\t" * self.indents) + "}"

    def emit_function(self,statement):
        func_name = statement["name"]
        output = f"void {func_name}(){{"
        output += self.emit_body(statement)
        return output + "\n" + ("\t" * self.indents) + "}"

    def emit_call(self,statement):
        func_name = statement["function"]
        return f"{func_name}();"


    def emit_body(self,statement):
        output = ""
        self.indents += 1
        for line in statement["body"]:
            if isinstance(line, TokenType):  # this checks for end tokens (a tad hacky)
                break
            output += "\n" + ("\t" * self.indents) + self.emit_statement(line)
        self.indents -= 1
        return output


    def emit_var_change(self,statement):
        """Emits variable change / reassignment"""
        var = statement["variable"]

        if var not in self.symbolsTable:
            self.error("Trying to change an undeclared variable")

        varIsString = self.symbolsTable[var] == "std::string"
        operator = statement["operator"]

        if "value" in statement:
            value = self.emit_value(statement["value"])

            if varIsString and value[0] != "\"":
                self.error("String variable can not do operation with non-string values")
            return f"{var} {operator} {value};"
        elif operator == "++" or operator == "--":
            if varIsString:
                self.error("Using increment/decrement operator on a string")
            return f"{var}{operator};"
        else:
            self.error("Expected a value when changing variable value")


    def emit_value(self, value):
        """Emits the value element: expressions,nums,strings and such """
        if isinstance(value,str):
            return value

        elif isinstance(value,dict):
            operator = value["operator"]
            # recursively obtain the value of expressions nested in other expressions
            left = self.emit_value(value["left"])
            right = self.emit_value(value["right"])

            """
            This is an error check for when we are trying to do an expression on non numericals, haven't figured out what do
            when we are summing a num with another expression
            if not left.isdigit() or not right.isdigit():
                if (self.symbolsTable[left] and self.symbolsTable[left] != "float") or (self.symbolsTable[right] and self.symbolsTable[right] != "float"):
                    self.error("Need two numerical values for an expression")
            """

            return f"({left} {operator} {right})"


    def emit(self, code):
        """ Appends a statement to the code"""
        self.code += ("\t" * self.indents) + code + "\n"

    def return_code(self):
        """ Returns the C++ code as a string"""
        return self.outlineTop + "\nint main()\n{\n" + self.code + self.outlineBot

    def error(self, message):
        """Exits the code and sends an error message."""
        sys.exit("Emitter Error: " + message)
