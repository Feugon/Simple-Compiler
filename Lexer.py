
class Lexer:
    def __init__(self, source):
        self.source = source
        self.cur_char = " "

        # we do this to avoid bounds checking here
        self.position = -1
        self.nextToken()

    def nextToken(self):
        self.position += 1
        if self.position >= len(self.source):
            self.cur_char = "error"
        else:
            self.cur_char = self.source[self.position]
            print(self.cur_char)



x = Lexer("hi")