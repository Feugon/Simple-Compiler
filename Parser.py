from Token import *
import sys

# TODO: handle endif token, change the assignment parsing so it includes the name of the variable

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
            return self.parse_while_statement()
        elif token.kind == TokenType.SET:
            return self.parse_assignment()
        elif token.kind == TokenType.ENDIF:
            return token.kind
        elif token.kind == TokenType.ENDREPEAT:
            return token.kind
        elif token.kind == TokenType.PRINT:
            return self.parse_print()
        else:
            self.advance()
            return token.kind
        # Add additional cases for other statement types as needed

    def parse_if_statement(self):
        """Parses an if-statement structure, assuming tokens are in 'IF <condition> DO <body> END' format."""
        self.advance()  # jumps over IF
        condition = self.parse_condition()
        self.advance() # jumps over last token in condition
        self.advance() # jumps over DO
        self.skip_newlines()
        body = self.parse_block()
        return {'type': 'IF', 'condition': condition, 'body': body}

    def parse_condition(self):
        """Parses an expression, such as a comparison or arithmetic operation."""
        if self.current_token().kind == TokenType.IDENT:
            left = self.current_token().text
            self.advance()
        else:
            left = self.parse_expression()

        operator = self.current_token()
        self.advance()

        if self.current_token().kind == TokenType.IDENT:
            right = self.current_token().text
            self.advance()
        else:
            right = self.parse_expression()
        if operator.kind.value < 206:
            self.error("Incorrect operator")
        return {'left': left, 'operator': operator.text, 'right': right}

    def parse_block(self):
        """Parses a block of statements (e.g., statements inside an if-statement or loop)."""
        block = []
        while self.current_token().kind != TokenType.ENDREPEAT and self.current_token().kind != TokenType.ENDIF:
            block.append(self.parse_statement())
        self.advance()
        return block


    def parse_assignment(self):
        var_name = self.next_token()
        value = None
        if self.match(self.next_token(), TokenType.EQ, True):
            operator = self.current_token()
        if self.match(self.next_token(), TokenType.STRING):
            value = self.current_token().text
        elif self.match(self.current_token(), TokenType.NUMBER) or self.match(self.current_token(), TokenType.LP):
            value = self.parse_expression()
        if not value:
            self.error("No value found in assignment.")
        self.advance()
        self.declaredVars.add(var_name.text)
        return {'type': 'SET', 'operator': operator.text, 'value': value}

    def parse_expression(self):
        """Parses an expression with addition and subtraction, consisting of terms."""
        left = self.parse_term()

        # Parse additional terms with "+" or "-"
        while self.current_token().kind in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token().text  # Use operator text instead of the token object
            self.advance()  # Move past the operator
            right = self.parse_term()
            left = {'operator': operator, 'left': left, 'right': right}

        return left

    def parse_term(self):
        """Parses a term with multiplication and division, consisting of factors."""
        left = self.parse_factor()

        # Parse additional factors with "*" or "/"
        while self.current_token().kind in (TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.current_token().text  # Use operator text instead of the token object
            self.advance()  # Move past the operator
            right = self.parse_factor()
            left = {'operator': operator, 'left': left, 'right': right}

        return left

    def parse_factor(self):
        """Parses a factor, which can be a number or a parenthesized expression."""
        token = self.current_token()

        if token.kind == TokenType.NUMBER:
            self.advance()  # Move past the number
            return int(token.text)  # Return the number as an integer

        elif token.kind == TokenType.LP:
            self.advance()  # Move past "("
            expression = self.parse_expression()
            if self.current_token().kind != TokenType.RP:
                self.error("Expected ')'")
            self.advance()  # Move past ")"
            return expression
        else:
            self.error("Expected a number or '(' in factor instead of " + str(token.kind))


    def parse_print(self):
        """Parses a print statement, assuming the syntax 'PRINT <expression>'."""
        self.advance() # jump over PRINT
        token = self.current_token()
        if self.match(self.current_token(),TokenType.STRING):
            # Handle direct string printing
            self.advance()
            return {'type': 'PRINT', 'value': token.text}
        elif self.match(self.current_token(), TokenType.IDENT) and self.current_token().text in self.declaredVars:
            self.advance()
            return {'type': 'PRINT', 'identifier': token.text}
        elif self.match(self.current_token(), TokenType.IDENT) and self.current_token().text not in self.declaredVars:
            self.error("Trying to access an undeclared variable.")
        else:
            expression = self.parse_expression()
            return {'type': 'PRINT', 'expression': expression}

    def current_token(self):
        """Returns the current token without advancing the position."""
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
        if token.kind == type:
            return True
        elif strict:
            self.error("Expected " + type + " but recieved " + token.kind)

    def error(self,message):
        sys.exit("Error: " + message)



