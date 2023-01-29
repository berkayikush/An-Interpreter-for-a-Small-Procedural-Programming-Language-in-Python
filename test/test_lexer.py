import unittest

from project_code.tokens import Token
from project_code.lexer import Lexer

# Create test cases to test get_next_token() method of Lexer class.
class TestLexer(unittest.TestCase):
    def test_get_next_token_with_empty_text(self):
        text = ""
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EOF)
        self.assertEqual(token.value, None)

    def test_get_next_token_with_multi_line_comment(self):
        text = "/* This is a multi line comment. */"
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EOF)
        self.assertEqual(token.value, None)

    def test_get_next_token_with_whitespace(self):
        text = "       \t\n\n"
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EOF)
        self.assertEqual(token.value, None)

    def test_get_next_token_with_identifier(self):
        text = "hello"
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.IDENTIFIER)
        self.assertEqual(token.value, text)

    def test_get_next_token_with_keyword(self):
        text = "var int float bool and or not"
        lexer = Lexer(text)

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.K_VAR)
        self.assertEqual(token.value, "var")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.K_INT)
        self.assertEqual(token.value, "int")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.K_FLOAT)
        self.assertEqual(token.value, "float")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.K_BOOL)
        self.assertEqual(token.value, "bool")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.K_AND)
        self.assertEqual(token.value, "and")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.K_OR)
        self.assertEqual(token.value, "or")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.K_NOT)
        self.assertEqual(token.value, "not")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EOF)
        self.assertEqual(token.value, None)

    def test_get_next_token_with_int(self):
        text = "123"
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.INT)
        self.assertEqual(token.value, int(text))

    def test_get_next_token_with_float(self):
        text = "123.456"
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.FLOAT)
        self.assertEqual(token.value, float(text))

    def test_get_next_token_with_bool(self):
        text = "true false"
        lexer = Lexer(text)

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.BOOL)
        self.assertEqual(token.value, "true")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.BOOL)
        self.assertEqual(token.value, "false")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EOF)
        self.assertEqual(token.value, None)

    def test_get_next_token_with_string(self):
        text = '"Hello World!"'
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.STR)

    def test_get_next_token_with_punctuation(self):
        text = "(),;{}"
        lexer = Lexer(text)

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.LEFT_PARENTHESIS)
        self.assertEqual(token.value, "(")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.RIGHT_PARENTHESIS)
        self.assertEqual(token.value, ")")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.COMMA)
        self.assertEqual(token.value, ",")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.SEMI_COLON)
        self.assertEqual(token.value, ";")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.LEFT_CURLY_BRACKET)
        self.assertEqual(token.value, "{")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.RIGHT_CURLY_BRACKET)
        self.assertEqual(token.value, "}")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EOF)
        self.assertEqual(token.value, None)

    def test_get_next_token_with_operator(self):
        text = "+ - * / // == != < > <= >="
        lexer = Lexer(text)

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.PLUS)
        self.assertEqual(token.value, "+")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.MINUS)
        self.assertEqual(token.value, "-")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.MULTIPLICATION)
        self.assertEqual(token.value, "*")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.FLOAT_DIVISION)
        self.assertEqual(token.value, "/")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.INT_DIVISION)
        self.assertEqual(token.value, "//")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EQUALS)
        self.assertEqual(token.value, "==")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.NOT_EQUALS)
        self.assertEqual(token.value, "!=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.LESS_THAN)
        self.assertEqual(token.value, "<")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.GREATER_THAN)
        self.assertEqual(token.value, ">")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.LESS_THAN_OR_EQUALS)
        self.assertEqual(token.value, "<=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.GREATER_THAN_OR_EQUALS)
        self.assertEqual(token.value, ">=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EOF)
        self.assertEqual(token.value, None)

    def test_get_next_token_with_asignment_operators(self):
        text = "= += -= *= /= //="
        lexer = Lexer(text)

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.ASSIGN)
        self.assertEqual(token.value, "=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.PLUS_ASSIGN)
        self.assertEqual(token.value, "+=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.MINUS_ASSIGN)
        self.assertEqual(token.value, "-=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.MULTIPLICATION_ASSIGN)
        self.assertEqual(token.value, "*=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.FLOAT_DIVISION_ASSIGN)
        self.assertEqual(token.value, "/=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.INT_DIVISION_ASSIGN)
        self.assertEqual(token.value, "//=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EOF)
        self.assertEqual(token.value, None)
