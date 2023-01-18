from project_code import interpreter
from project_code.lexer import Lexer
from project_code.parser_ import Parser
from project_code.semantic_analysis import SemanticAnalyzer
from project_code.interpreter import Interpreter


def main():
    text = """
    var(bool) x = true, y = false;
    var(bool) z = x and y;
    var(bool) a = x or y;
    """

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()

    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.visit(tree)

    hello = Interpreter(tree)
    hello.interpret()


if __name__ == "__main__":
    main()
