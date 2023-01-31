import sys

from project_code.error import (
    LexerError,
    ParserError,
    SemnaticError,
    InterpreterError,
)
from project_code.lexer import Lexer
from project_code.parser_ import Parser
from project_code.semantic_analysis import SemanticAnalyzer
from project_code.interpreter import Interpreter


def main():
    text = """
    var(int) a = (4 + 5) * 2; /* 18 */
    """

    lexer = Lexer(text)

    try:
        parser = Parser(lexer)
        tree = parser.parse()

    except (LexerError, ParserError) as error:
        print(error.message)
        sys.exit(1)

    semantic_analyzer = SemanticAnalyzer()

    try:
        semantic_analyzer.visit(tree)
    except SemnaticError as error:
        print(error.message)
        sys.exit(1)

    interpreter = Interpreter(tree)

    try:
        interpreter.interpret()
    except InterpreterError as error:
        print(error.message)
        sys.exit(1)


if __name__ == "__main__":
    main()
