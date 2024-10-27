from Token import *
import Lexer
import sys


class Parser:
    class Parser:
        def __init__(self, tokens):
            """Initialize the parser with a list of tokens provided by the lexer."""
            self.tokens = tokens
            self.position = 0
            self.results = []

        def parse(self):
            """Main parsing method. Iterates over tokens and builds the parse tree or structured results."""
            while self.position < len(self.tokens):
                construct = self.parse_statement()
                if construct:
                    self.results.append(construct)


        def parse_statement(self):
            """Parses a single statement based on tokens."""
            token = self.current_token()
            if token.kind == TokenType.IF:
                return self.parse_if_statement()
            elif token.kind == TokenType.REPEAT:
                return self.parse_while_statement()
            # Add additional cases for other statement types as needed

        def parse_if_statement(self):
            """Parses an if-statement structure, assuming tokens are in 'IF <condition> THEN <body> END' format."""
            self.advance()  # jumps over IF
            condition = self.parse_expression()
            self.advance()
            self.advance()
            body = self.parse_block()
            return {'type': 'IF', 'condition': condition, 'body': body}

        def parse_expression(self):
            """Parses an expression, such as a comparison or arithmetic operation."""
            left = self.current_token()
            operator = self.next_token()
            right = self.next_token()
            return {'left': left, 'operator': operator, 'right': right}

        def parse_block(self):
            """Parses a block of statements (e.g., statements inside an if-statement or loop)."""
            block = []
            while self.current_token().kind != TokenType.ENDREPEAT and self.current_token().kind != TokenType.ENDIF:
                block.append(self.parse_statement())
                # this will get stuck in a continious loop, need to advance either here or in parse_statement
            self.advance()
            return block

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

        def error(self,message):
            sys.exit("Error: " + message)



