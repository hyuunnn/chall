from sly import Parser
from lexer import BuBuLexer


class BuBuParser(Parser):
    tokens = BuBuLexer.tokens

    precedence = (
        ("nonassoc", EQ, NE, LT, GT, LE, GE),
        ("left", PLUS, MINUS),
        ("left", TIMES, DIVIDE),
        ("right", NOT),
        ("right", UMINUS),
    )

    def __init__(self):
        self.env = {}

    @_("PRINT expr")
    def statement(self, p):
        print(p.expr)

    @_("NAME ASSIGN expr")
    def statement(self, p):
        self.env[p.NAME] = p.expr
        return p.expr

    @_("expr")
    def statement(self, p):
        return p.expr

    @_(
        "expr EQ expr",
        "expr NE expr",
        "expr LT expr",
        "expr GT expr",
        "expr LE expr",
        "expr GE expr",
        "expr PLUS expr",
        "expr MINUS expr",
        "expr TIMES expr",
        "expr DIVIDE expr",
    )
    def expr(self, p):
        return self.calc(p[1], p.expr0, p.expr1)

    @_("MINUS expr %prec UMINUS")
    def expr(self, p):
        return -p.expr

    @_("PLUS expr")
    def expr(self, p):
        return p.expr

    @_("NOT expr")
    def expr(self, p):
        return not p.expr

    @_("LPAREN expr RPAREN")
    def expr(self, p):
        return p.expr

    @_("FLOAT")
    def expr(self, p):
        return p.FLOAT

    @_("NUMBER")
    def expr(self, p):
        return p.NUMBER

    @_("STRING")
    def expr(self, p):
        return p.STRING

    @_("TRUE")
    @_("FALSE")
    def expr(self, p):
        return p[0]

    @_("NAME")
    def expr(self, p):
        try:
            return self.env[p.NAME]
        except LookupError:
            print(f"Undefined name {p.NAME!r}")
            return 0

    def calc(self, op, expr0, expr1):
        try:
            if self.is_str(expr0, expr1):
                if op == "+":
                    return str(expr0) + str(expr1)
                elif op == "*":
                    return (
                        expr0 * int(expr1)
                        if isinstance(expr0, str)
                        else int(expr0) * expr1
                    )
            return eval(f"{expr0} {op} {expr1}")
        except Exception:
            return "Invalid input"

    def is_str(self, expr0, expr1):
        return any(isinstance(expr, str) for expr in (expr0, expr1))


if __name__ == "__main__":
    lexer = BuBuLexer()
    parser = BuBuParser()

    while True:
        try:
            text = input(">> ")
            result = parser.parse(lexer.tokenize(text))
            if result is not None:
                print(result)
        except EOFError:
            break
