from project_code.tokens import Token
from project_code.lexer import Lexer


class TestLexer:
    def test_get_next_token(self):
        text = " "
        lexer = Lexer(text)
        token = lexer.get_next_token()

        assert token.type_ == Token.EOF
        assert token.value is None

    def test_get_next_token_with_int(self):
        text = "5334"
        lexer = Lexer(text)
        token = lexer.get_next_token()

        assert token.type_ == Token.INT
        assert token.value == 5334

        token = lexer.get_next_token()

        assert token.type_ == Token.EOF
        assert token.value is None

    def test_get_next_token_with_float(self):
        text = "53.3454"
        lexer = Lexer(text)
        token = lexer.get_next_token()

        assert token.type_ == Token.FLOAT
        assert token.value == 53.3454

        token = lexer.get_next_token()

        assert token.type_ == Token.EOF
        assert token.value is None

    def test_get_next_token_with_id(self):
        text = "baz"
        lexer = Lexer(text)
        token = lexer.get_next_token()

        assert token.type_ == Token.IDENTIFIER
        assert token.value == "baz"

        token = lexer.get_next_token()

        assert token.type_ == Token.EOF
        assert token.value is None

    def test_get_next_token_with_arithmetic_operator(self):
        text = "+-*/%//"
        lexer = Lexer(text)
        token = lexer.get_next_token()

        assert token.type_ == Token.PLUS
        assert token.value == "+"

        token = lexer.get_next_token()

        assert token.type_ == Token.MINUS
        assert token.value == "-"

        token = lexer.get_next_token()

        assert token.type_ == Token.MULTIPLICATION
        assert token.value == "*"

        token = lexer.get_next_token()

        assert token.type_ == Token.FLOAT_DIVISION
        assert token.value == "/"

        token = lexer.get_next_token()

        assert token.type_ == Token.MODULO
        assert token.value == "%"

        token = lexer.get_next_token()

        assert token.type_ == Token.INT_DIVISION
        assert token.value == "//"

        token = lexer.get_next_token()

        assert token.type_ == Token.EOF
        assert token.value is None

    def test_get_next_token_with_parenthesis(self):
        text = "()"
        lexer = Lexer(text)
        token = lexer.get_next_token()

        assert token.type_ == Token.LEFT_PARENTHESIS
        assert token.value == "("

        token = lexer.get_next_token()

        assert token.type_ == Token.RIGHT_PARENTHESIS
        assert token.value == ")"

        token = lexer.get_next_token()

        assert token.type_ == Token.EOF
        assert token.value is None

    def test_get_next_token_with_equals(self):
        text = "=="
        lexer = Lexer(text)
        token = lexer.get_next_token()

        assert token.type_ == Token.EQUALS
        assert token.value == "=="

        token = lexer.get_next_token()

        assert token.type_ == Token.EOF
        assert token.value is None

    def test_get_next_token_with_assignment_operators(self):
        text = "+= -= *= /= %= //= ="
        lexer = Lexer(text)
        token = lexer.get_next_token()

        assert token.type_ == Token.PLUS_ASSIGN
        assert token.value == "+="

        token = lexer.get_next_token()

        assert token.type_ == Token.MINUS_ASSIGN
        assert token.value == "-="

        token = lexer.get_next_token()

        assert token.type_ == Token.MULTIPLICATION_ASSIGN
        assert token.value == "*="

        token = lexer.get_next_token()

        assert token.type_ == Token.FLOAT_DIVISION_ASSIGN
        assert token.value == "/="

        token = lexer.get_next_token()

        assert token.type_ == Token.MODULO_ASSIGN
        assert token.value == "%="

        token = lexer.get_next_token()

        assert token.type_ == Token.INT_DIVISION_ASSIGN
        assert token.value == "//="

        token = lexer.get_next_token()

        assert token.type_ == Token.ASSIGN
        assert token.value == "="

        token = lexer.get_next_token()

        assert token.type_ == Token.EOF
        assert token.value is None

    def test_get_next_token_with_semi_colon(self):
        text = ";"
        lexer = Lexer(text)
        token = lexer.get_next_token()

        assert token.type_ == Token.SEMI_COLON
        assert token.value == ";"

        token = lexer.get_next_token()

        assert token.type_ == Token.EOF
        assert token.value is None

    def test_int_division(self):
        text = "10 // 3"
        lexer = Lexer(text)
        token = lexer.get_next_token()

        assert token.type_ == Token.INT
        assert token.value == 10

        token = lexer.get_next_token()

        assert token.type_ == Token.INT_DIVISION
        assert token.value == "//"

        token = lexer.get_next_token()

        assert token.type_ == Token.INT
        assert token.value == 3

        token = lexer.get_next_token()

        assert token.type_ == Token.EOF
        assert token.value is None

    def test_get_next_token_with_expression(self):
        text = "10 * (8 + 4) / 2"
        lexer = Lexer(text)
        token = lexer.get_next_token()

        assert token.type_ == Token.INT
        assert token.value == 10

        token = lexer.get_next_token()

        assert token.type_ == Token.MULTIPLICATION
        assert token.value == "*"

        token = lexer.get_next_token()

        assert token.type_ == Token.LEFT_PARENTHESIS
        assert token.value == "("

        token = lexer.get_next_token()

        assert token.type_ == Token.INT
        assert token.value == 8

        token = lexer.get_next_token()

        assert token.type_ == Token.PLUS
        assert token.value == "+"

        token = lexer.get_next_token()

        assert token.type_ == Token.INT
        assert token.value == 4

        token = lexer.get_next_token()

        assert token.type_ == Token.RIGHT_PARENTHESIS
        assert token.value == ")"

        token = lexer.get_next_token()

        assert token.type_ == Token.FLOAT_DIVISION
        assert token.value == "/"

        token = lexer.get_next_token()

        assert token.type_ == Token.INT
        assert token.value == 2

        token = lexer.get_next_token()

        assert token.type_ == Token.EOF
        assert token.value is None

    def test_get_next_token_with_assignment(self):
        text = """
        a = 10;
        a = a + 20;
        """
        lexer = Lexer(text)
        token = lexer.get_next_token()

        assert token.type_ == Token.IDENTIFIER
        assert token.value == "a"

        token = lexer.get_next_token()

        assert token.type_ == Token.ASSIGN
        assert token.value == "="

        token = lexer.get_next_token()

        assert token.type_ == Token.INT
        assert token.value == 10

        token = lexer.get_next_token()

        assert token.type_ == Token.SEMI_COLON
        assert token.value == ";"

        token = lexer.get_next_token()

        assert token.type_ == Token.IDENTIFIER
        assert token.value == "a"

        token = lexer.get_next_token()

        assert token.type_ == Token.ASSIGN
        assert token.value == "="

        token = lexer.get_next_token()

        assert token.type_ == Token.IDENTIFIER
        assert token.value == "a"

        token = lexer.get_next_token()

        assert token.type_ == Token.PLUS
        assert token.value == "+"

        token = lexer.get_next_token()

        assert token.type_ == Token.INT
        assert token.value == 20

        token = lexer.get_next_token()

        assert token.type_ == Token.SEMI_COLON
        assert token.value == ";"

        token = lexer.get_next_token()

        assert token.type_ == Token.EOF
        assert token.value is None
