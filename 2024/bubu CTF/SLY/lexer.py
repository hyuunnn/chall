from sly import Lexer


class BuBuLexer(Lexer):
    tokens = {
        NAME,
        NUMBER,
        FLOAT,
        PLUS,
        MINUS,
        TIMES,
        DIVIDE,
        ASSIGN,
        LPAREN,
        RPAREN,
        PRINT,
        STRING,
        TRUE,
        FALSE,
        NOT,
        EQ,
        NE,
        LT,
        GT,
        LE,
        GE,
    }
    ignore = " \t"

    # Tokens
    PRINT = r"print"
    TRUE = r"True"
    FALSE = r"False"
    NOT = r"not"

    NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"
    FLOAT = r"\d+\.\d+"
    NUMBER = r"\d+"

    EQ = r"=="
    NE = r"!="
    LE = r"<="
    GE = r">="
    LT = r"<"
    GT = r">"

    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"
    ASSIGN = r"="
    LPAREN = r"\("
    RPAREN = r"\)"
    STRING = r"\"[^\"]*\"|\'[^\']*\'"

    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    def STRING(self, t):
        t.value = t.value.strip('"').strip("'")
        return t

    def TRUE(self, t):
        t.value = True
        return t

    def FALSE(self, t):
        t.value = False
        return t

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
