from Token import *
import sys

#TODO: add new line handling || assignment doesn't allow for expressions

class Parser:
    def __init__(self, tokens):
        """Initialize the parser with a list of tokens provided by the lexer."""
        self.tokens = tokens
        self.position = 0
        self.results = []

    def parse(self):
        """Main parsing method. Iterates over tokens and builds the parse tree or structured results."""
        while self.position < len(self.tokens):
            self.skip_newlines()
            construct = self.parse_statement()
            if construct:
                self.results.append(construct)

    def skip_newlines(self):
        """Advances the position to skip any newline tokens."""
        while self.current_token().kind == TokenType.NEWLINE:
            self.advance()


    def parse_statement(self):
        """Parses a single statement based on tokens."""
        token = self.current_token()
        if token.kind == TokenType.IF:
            return self.parse_if_statement()
        elif token.kind == TokenType.REPEAT:
            return self.parse_while_statement()
        elif token.kind == TokenType.SET:
            return self.parse_assignment()
        else:
            self.advance()
            return token.kind
        # Add additional cases for other statement types as needed

    def parse_if_statement(self):
        """Parses an if-statement structure, assuming tokens are in 'IF <condition> DO <body> END' format."""
        self.advance()  # jumps over IF
        condition = self.parse_expression()
        self.advance() # jumps over last token in condition
        self.advance() # jumps over DO
        self.skip_newlines()
        body = self.parse_block()
        return {'type': 'IF', 'condition': condition, 'body': body}

    def parse_expression(self):
        """Parses an expression, such as a comparison or arithmetic operation."""
        left = self.current_token()
        operator = self.next_token()
        right = self.next_token()
        return {'left': left.text, 'operator': operator.text, 'right': right.text}

    def parse_block(self):
        """Parses a block of statements (e.g., statements inside an if-statement or loop)."""
        block = []
        while self.current_token().kind != TokenType.ENDREPEAT and self.current_token().kind != TokenType.ENDIF:
            self.skip_newlines() # THIS CAUSES THE FUCKUP
            block.append(self.parse_statement())
        self.advance()
        return block


    def parse_assignment(self):
        var_name = self.next_token()
        value = None
        if self.match(self.next_token(), TokenType.EQ, True):
            operator = self.current_token()
        if self.match(self.next_token(), TokenType.STRING) or self.match(self.current_token(), TokenType.NUMBER):
            value = self.current_token()
        if not value:
            self.error("No value found in assignment.")
        self.advance()
        return {'type': 'SET', 'operator': operator, 'value': value}


    def current_token(self):
        """Returns the current token without advancing the position."""
        return self.tokens[self.position]

    def next_token(self):
        """Advances to the next token and returns it."""
        self.position += 1
        if self.position >= len(self.tokens):
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



