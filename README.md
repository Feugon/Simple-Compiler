# Simple Compiler


## Overview
This compiler is a custom compiler project that translates code written in a simple, user-defined programming language into C++ code. This project demonstrates the fundamentals of compiler design, including lexical analysis, syntax parsing, and code generation, aimed at simplifying the learning process for basic compiler principles.

## Features
- **Lexical Analysis**: Tokenizes source code to identify keywords, variables, operators, and literals.
- **Syntax Parsing**: Parses tokens using a grammar defined for the language and generates a parse tree or abstract syntax tree (AST).
- **Code Generation**: Converts parsed structures into C++ code that can be compiled to create an executable program.
- **Error Handling**: Provides basic syntax and semantic error handling for more accessible debugging.

## Project Structure
- `lexer.py`: Handles lexical analysis and tokenization of source code.
- `parser.py`: Parses tokens using the specified grammar to validate structure and semantics.
- `emitter.py`: Converts parsed code into C++ syntax.
- `input.txt`: Input text file that gets compiled into C++ code.
- `output.txt`: Output code compiled to C++.
- `README.md`: Project documentation.

## Steps to Assemble the Compiler

1. **Define Language Grammar**:
   - Created a grammar that outlines the syntax and structure of the custom language, defining rules for statements, expressions, variable declarations, control structures, etc.
   - Grammar Example: `program ::= statement | statement program`

2. **Develop the Lexer**:
   - Implemented a lexer that tokenizes each line of code by identifying keywords, literals, and operators.
   - Largely utilized the work of Austin Henley from his "Teeny Tiny" compiler series

3. **Build the Parser**:
   - Created a basic parser to check that the sequence of tokens follows the defined grammar.
   - Organized the code into a structured format that makes it easier to generate C++ code.

4. **Implement Code Generation**:
   - Designed a code generation phase to transform the parse tree into equivalent C++ code, focusing on statements like variable assignments, basic control flows, and print statements.
   - Emission Examples:
     - Variable Declaration: `SET x = 10` becomes `float x = 10;` in C++.
     - Conditional Statements: `IF x == 10 DO` is translated to `if (x==10) {`.

5. **Integrate Error Handling**:
   - Added basic error detection for syntax and semantic issues, with error messages that reference the source line and type of error for easier debugging.

## Language Grammar
The language grammar for this project was defined as follows:
---

### Grammar

This defines the syntax for the custom language used in this project, written in Backus-Naur Form (BNF).

#### Program Structure

```bnf
<program>        ::= {<statement>}
```

#### Statements

```bnf
<statement>      ::= <assignment> nl
                 | <if-statement> nl
                 | <expression> nl
                 | PRINT (<factor> | <str>) nl
                 | <repeat> nl
                 | <function> nl
```

#### Assignment

```bnf
<assignment>     ::= <identifier> <var_name> "=" <expression> nl
<var_name>       ::= <str>
<identifier>     ::= "num" | "str"
<num>            ::= <digit>+
<digit>          ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<nl>             ::= "\n"
```

#### If-Statement

```bnf
<if-statement>   ::= "IF" <condition> "DO" nl <statement>* "ENDIF" nl
<condition>      ::= <term> (("==" | "!=" | ">" | ">=" | "<" | "<=") <term>)
                 | <expression> (("==" | "!=" | ">" | ">=" | "<" | "<=") <expression>)
                 | <factor> (("==" | "!=" | ">" | ">=" | "<" | "<=") <factor>)
```

#### Expressions

```bnf
<expression>     ::= <term> (("+" | "-") <term>)*
<term>           ::= <factor> (("*" | "/") <factor>)*
<factor>         ::= <number> | "(" <expression> ")"
```

#### Strings

```bnf
<str>            ::= "\"" <character>* "\""
<character>      ::= <letter> | <digit> | <punctuation> | <whitespace>
```

#### Repeat Loop

```bnf
<repeat>         ::= "REPEAT" <body> "TIMES" <num> "VAR" <str>
<body>           ::= <statement> | <statement> <body>
```

#### Functions

```bnf
<function>       ::= "FUNCTION" <function_name> <body> "ENDFUNCTION"
<function_name>  ::= '"' <name> '"'
<body>           ::= <statement> | <statement> <body>
```

#### Characters and Tokens

```bnf
<letter>         ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
<punctuation>    ::= "!" | "@" | "#" | "$" | "%" | "^" | "&" | "*" | "(" | ")" | "," | "." | ":" | ";" | "<" | "=" | ">" | "?"
<whitespace>     ::= " " | "\t" | "\n"
```



## Challenges and Lessons Learned
1. **Lexical Ambiguities**: Adjusted the lexer to handle ambiguous cases.
2. **Error Messaging**: Added line-by-line error reporting, which improved debugging.
3. **Overall Structure of a Compiler**: Learned a lot about how a compiler operates.


## Acknoweledgments 
This project was attempted largely in part because I saw a brief article by Austin Henley about creating his own minute compiler. The article was so interesting that I decided to tackle this project head on and try to implement my own design. Here is the link to the article: https://austinhenley.com/blog/teenytinycompiler1.html. I employed the help of ChatGPT for writing the README and debugging some code.


