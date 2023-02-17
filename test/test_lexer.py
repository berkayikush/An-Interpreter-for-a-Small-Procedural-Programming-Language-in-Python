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
        self.assertEqual(token.val, None)

    def test_get_next_token_with_multi_line_comment(self):
        text = "/* This is a multi line comment. */"
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EOF)
        self.assertEqual(token.val, None)

    def test_get_next_token_with_whitespace(self):
        text = "       \t\n\n"
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EOF)
        self.assertEqual(token.val, None)

    def test_get_next_token_with_identifier(self):
        text = "hello"
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.IDENTIFIER)
        self.assertEqual(token.val, text)

    def test_get_next_token_with_keyword(self):
        text = "var int float bool and or not"
        lexer = Lexer(text)

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.K_VAR)
        self.assertEqual(token.val, "var")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.K_INT)
        self.assertEqual(token.val, "int")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.K_FLOAT)
        self.assertEqual(token.val, "float")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.K_BOOL)
        self.assertEqual(token.val, "bool")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.K_AND)
        self.assertEqual(token.val, "and")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.K_OR)
        self.assertEqual(token.val

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.K_NOT)
        self.assertEqual(token.valot")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EOF)
        self.assertEqual(token.val, None)

    def test_get_next_token_with_int(self):
        text = "123"
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.INT)
        self.assertEqual(token.val, int(text))

    def test_get_next_token_with_float(self):
        text = "123.456"
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.FLOAT)
        self.assertEqual(token.val, float(text))

    def test_get_next_token_with_bool(self):
        text = "true false"
        lexer = Lexer(text)

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.BOOL)
        self.assertEqual(token.val, "true")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.BOOL)
        self.assertEqual(token.val"false")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EOF)
        self.assertEqual(token.valne)

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
        self.assertEqual(token.val, "(")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.RIGHT_PARENTHESIS)
        self.assertEqual(token.val, ")")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.COMMA)
        self.assertEqual(token.val, ",")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.SEMICOLON)
        self.assertEqual(token.val, ";")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.LEFT_CURLY_BRACKET)
        self.assertEqual(token.val, "{")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.RIGHT_CURLY_BRACKET)
        self.assertEqual(token.val, "}")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EOF)
        self.assertEqual(token.val, None)

    def test_get_next_token_with_operator(self):
        text = "+ - * / // == != < > <= >="
        lexer = Lexer(text)

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.PLUS)
        self.assertEqual(token.val, "+")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.MINUS)
        self.assertEqual(token.val, "-")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.MULTIPLICATION)
        self.assertEqual(token.val, "*")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.FLOAT_DIVISION)
        self.assertEqual(token.val, "/")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.INT_DIVISION)
        self.assertEqual(token.val, "//")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EQUALS)
        self.assertEqual(token.val, "==")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.NOT_EQUALS)
        self.assertEqual(token.val, "!=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.LESS_THAN)
        self.assertEqual(token.val, "<")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.GREATER_THAN)
        self.assertEqual(token.val, ">")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.LESS_THAN_OR_EQUALS)
        self.assertEqual(token.val, "<=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.GREATER_THAN_OR_EQUALS)
        self.assertEqual(token.val, ">=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EOF)
        self.assertEqual(token.val, None)

    def test_get_next_token_with_asignment_operators(self):
        text = "= += -= *= /= //="
        lexer = Lexer(text)

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.ASSIGN)
        self.assertEqual(token.val, "=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.PLUS_ASSIGN)
        self.assertEqual(token.val, "+=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.MINUS_ASSIGN)
        self.assertEqual(token.val, "-=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.MULTIPLICATION_ASSIGN)
        self.assertEqual(token.val, "*=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.FLOAT_DIVISION_ASSIGN)
        self.assertEqual(token.val, "/=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.INT_DIVISION_ASSIGN)
        self.assertEqual(token.val, "//=")

        token = lexer.get_next_token()
        self.assertEqual(token.type_, Token.EOF)
        self.assertEqual(token.val, None)
