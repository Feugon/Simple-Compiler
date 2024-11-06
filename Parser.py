from Token import *
import sys

class Parser:
    def __init__(self, tokens):
        """Initialize the parser with a list of tokens provided by the lexer."""
        self.tokens = tokens
        self.tokenLen = len(tokens)
        self.position = 0
        self.results = []
        self.declaredVars = set()

    def parse(self):
        """Main parsing method. Iterates over tokens and builds the parse tree or structured results."""
        while self.position < self.tokenLen:
            construct = self.parse_statement()
            if construct:
                self.results.append(construct)

    def skip_newlines(self):
        """Advances the position to skip any newline tokens."""
        # not sure if out of bounds check is necessary here
        while self.position < self.tokenLen and self.current_token().kind == TokenType.NEWLINE:
            self.advance()


    def parse_statement(self):
        """Parses a single statement based on tokens."""
        self.skip_newlines()
        if self.position >= self.tokenLen:
            return
        token = self.current_token()
        if token.kind == TokenType.IF:
            return self.parse_if_statement()
        elif token.kind == TokenType.REPEAT:
            return self.parse_repeat()
        elif token.kind == TokenType.SET:
            return self.parse_assignment()
        elif token.kind == TokenType.ENDIF:
            return token.kind
        elif token.kind == TokenType.VAR:
            return token.kind
        elif token.kind == TokenType.PRINT:
            return self.parse_print()
        elif token.kind == TokenType.IDENT:
            return self.parse_var_change()
        else:
            self.advance()
            return token.kind
        # Add additional cases for other statement types as needed

    def parse_if_statement(self):
        """Parses an if-statement structure, assuming tokens are in "IF <condition> DO <body> END" format."""
        self.advance()  # jumps over IF
        condition = self.parse_condition()
        self.advance() # jumps over last token in condition
        self.advance() # jumps over DO
        self.skip_newlines()
        body = self.parse_block()
        return {"type": "IF", "condition": condition, "body": body}

    def parse_condition(self):
        """Parses an expression, such as a comparison or arithmetic operation."""
        if self.current_token().kind == TokenType.IDENT:
            left = self.current_token().text
            self.advance()
        else:
            left = self.parse_expression()

        operator = self.current_token()
        self.advance()

        if self.current_token().kind == TokenType.IDENT or self.current_token().kind == TokenType.STRING:
            right = f'"{self.current_token().text}"'
            self.advance()
        else:
            right = self.parse_expression()
        if operator.kind.value < 206 and operator.kind.value > 211 :
            self.error("Incorrect operator")
        return {"left": left, "operator": operator.text, "right": right}

    def parse_block(self):
        """Parses a block of statements (e.g., statements inside an if-statement or loop)."""
        block = []
        while self.current_token().kind != TokenType.TIMES and self.current_token().kind != TokenType.ENDIF:
            block.append(self.parse_statement())
        self.advance()
        return block

    def parse_var_change(self):
        """Parse a variable change, such as increment/decrement or setting equal to another value."""
        var = self.current_token()

        if var.text not in self.declaredVars:
            self.error("Using an undeclared variable")


        value = None
        expectedTokens = [TokenType.EQ,TokenType.PLUSEQ, TokenType.MINUSEQ, TokenType.INC,TokenType.DEC]
        if self.match(self.next_token(), expectedTokens, True):
            operator = self.current_token()

        if self.match(operator, [TokenType.INC,TokenType.DEC]):
            self.advance()
            return {"type": "VAR CHANGE", "variable": var.text, "operator": operator.text}

        self.advance()
        tokenOfValue = self.current_token()

        if self.match(tokenOfValue, TokenType.STRING):
            value = f'"{tokenOfValue.text}"'
        elif self.match(tokenOfValue, TokenType.NUMBER) or self.match(tokenOfValue, TokenType.LP):
            value = self.parse_expression()
        elif self.match(tokenOfValue, TokenType.IDENT) and tokenOfValue.text in self.declaredVars:
            value = self.parse_expression()
        if not value:
            self.error("No value found in assignment.")
        self.advance()
        self.declaredVars.add(var.text)
        return {"type": "VAR CHANGE", "variable": var.text, "operator": operator.text, "value": value}


    def parse_assignment(self):
        """ Parses an assignment statement """
        var = self.next_token()
        value = None
        if self.match(self.next_token(), TokenType.EQ, True):
            operator = self.current_token()

        self.advance()
        tokenOfValue = self.current_token()
        if self.match(tokenOfValue, TokenType.STRING):
            value = f'"{tokenOfValue.text}"'
        elif self.match(tokenOfValue, TokenType.NUMBER) or self.match(tokenOfValue, TokenType.LP):
            value = self.parse_expression()
        elif self.match(tokenOfValue, TokenType.IDENT) and tokenOfValue.text in self.declaredVars:
            value = self.parse_expression()
        if not value:
            self.error("No value found in assignment.")
        self.advance()
        self.declaredVars.add(var.text)
        return {"type": "SET", "variable": var.text, "operator": operator.text, "value": value}

    def parse_repeat(self):
        self.advance() # jump over repeat
        self.skip_newlines()

        body = self.parse_block()
        times = self.parse_expression()
        self.advance() # jump over var

        var_name = self.current_token().text
        self.advance()

        if not isinstance(var_name,str):
            self.error("VAR should be a string name for the variable")

        return {"type": "REPEAT", "body": body, "times":times, "var":var_name}

    def parse_expression(self):
        """Parses an expression with addition and subtraction, consisting of terms."""
        left = self.parse_term()

        # Parse additional terms with "+" or "-"
        while self.position < self.tokenLen and self.current_token().kind in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token().text  # Use operator text instead of the token object
            self.advance()  # Move past the operator
            right = self.parse_term()
            left = {"operator": operator, "left": left, "right": right}

        return left

    def parse_term(self):
        """Parses a term with multiplication and division, consisting of factors."""
        left = self.parse_factor()

        # Parse additional factors with "*" or "/"
        while self.position < self.tokenLen and self.current_token().kind in (TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.current_token().text  # Use operator text instead of the token object
            self.advance()  # Move past the operator
            right = self.parse_factor()
            left = {"operator": operator, "left": left, "right": right}

        return left

    def parse_factor(self):
        """Parses a factor, which can be a number or a parenthesized expression."""
        token = self.current_token()

        if token.kind == TokenType.NUMBER or (token.kind == TokenType.IDENT and token.text in self.declaredVars):
            self.advance()
            return token.text
        elif token.kind == TokenType.LP:
            self.advance()  # Move past "("
            expression = self.parse_expression()
            if self.position >= self.tokenLen or self.current_token().kind != TokenType.RP:
                self.error("Expected \")\"")
            self.advance()  # Move past ")"
            return expression
        else:
            self.error("Expected a number or \"(\" in factor instead of " + str(token.kind))


    def parse_print(self):
        """Parses a print statement, assuming the syntax "PRINT <expression>"."""
        self.advance() # jump over PRINT
        token = self.current_token()
        if self.match(self.current_token(),TokenType.STRING):
            # Handle direct string printing
            self.advance()
            return {"type": "PRINT", "value": f'"{token.text}"'}
        elif self.match(self.current_token(), TokenType.IDENT) and self.current_token().text in self.declaredVars:
            expression = self.parse_expression()
            return {"type": "PRINT", "identifier/expression": expression}
        elif self.match(self.current_token(), TokenType.IDENT) and self.current_token().text not in self.declaredVars:
            self.error("Trying to access an undeclared variable.")
        else:
            expression = self.parse_expression()
            return {"type": "PRINT", "value": expression}

    def current_token(self):
        """Returns the current token without advancing the position."""
        if self.position >= self.tokenLen:
            self.error("Trying to get out of bounds token")
        return self.tokens[self.position]
#
    def next_token(self):
        """Advances to the next token and returns it."""
        self.position += 1
        if self.position >= self.tokenLen:
            self.error("Expected additional tokens")

        return self.tokens[self.position]

    def advance(self):
        """Moves to the next token without returning it, useful for skipping over keywords."""
        self.position += 1

    def get_results(self):
        """Retrieves the parsed results in a structured format."""
        return self.results

    def match(self,token, type, strict = False):
        """ Checks if a token is a certain kind, if strict match it sends an error if the token doesn"t match."""
        if isinstance(type,list):
            if token.kind in type:
                return True
            if strict:
                self.error("Expected " + str(type) + " but received " + str(token.kind))
        if token.kind == type:
            return True
        elif strict:
            self.error("Expected " + str(type) + " but received " + str(token.kind))

    def error(self,message):
        """Exits the code and sends an error message."""
        sys.exit("Parser Error: " + message)



