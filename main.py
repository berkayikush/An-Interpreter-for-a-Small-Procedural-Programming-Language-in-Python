import sys

from project_code.error import (
    LexerError,
    ParserError,
    SemanticError,
    InterpreterError,
)
from project_code.lexer import Lexer
from project_code.parser_ import Parser
from project_code.semantic_analysis import SemanticAnalyzer
from project_code.interpreter import Interpreter


def main():
    text = """
    func(int) fibonacci(var(int) n) {
        if (n == 0) {
            return 0;
        }
        
        elseif (n == 1) {
            return 1;
        }
        
        else {
            return fibonacci(n - 1) + fibonacci(n - 2);
        }
    }
    
    var(int) result = fibonacci(7);
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
