from project_code.lexer import Lexer
from project_code.parser_ import Parser
from project_code.semantic_analysis import SemanticAnalyzer


def main():
    text = """
    var(float) x, y;
    """

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()

    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.visit(tree)


if __name__ == "__main__":
    main()
