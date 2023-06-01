import os
import sys

from project_code.error import (
    LexerError,
    ParserError,
    SemanticError,
    InterpreterError,
)
from project_code.interpreter import Interpreter
from project_code.lexer import Lexer
from project_code.parser_ import Parser
from project_code.semantic_analysis import SemanticAnalyzer


def open_program_file():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename>.co")
        sys.exit(1)

    filename = sys.argv[1]

    if os.path.splitext(filename)[1] != ".co":
        print("Error: File must be a .co file.")
        sys.exit(1)

    text = ""

    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
    except IOError:
        print(f"Error: File '{filename}' not found or could not be opened.")
        sys.exit(1)

    return text


def main():
    lexer = Lexer(open_program_file())

    try:
        parser = Parser(lexer)
        tree = parser.parse()
    except (LexerError, ParserError) as error:
        print(error.message)
        sys.exit(1)

    semantic_analyzer = SemanticAnalyzer()

    try:
        semantic_analyzer.visit(tree)
    except SemanticError as error:
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
