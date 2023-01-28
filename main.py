from project_code import interpreter
from project_code.lexer import Lexer
from project_code.parser_ import Parser
from project_code.semantic_analysis import SemanticAnalyzer
from project_code.interpreter import Interpreter
from project_code.program_stack import ProgramStack, StackFrame


def main():
    text = """
    var(int) a = 5;
    
    if (a == 5) {
        var(int) b = 10;
    }
    
    var(int) b = 15;
    """

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()

    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.visit(tree)

    interpreter = Interpreter(tree)
    interpreter.interpret()


if __name__ == "__main__":
    main()
