from project_code import interpreter
from project_code.lexer import Lexer
from project_code.parser_ import Parser
from project_code.semantic_analysis import SemanticAnalyzer
from project_code.interpreter import Interpreter
from project_code.program_stack import ProgramStack, StackFrame


def main():
    text = """
    var(int) x, y;
    y = 7;
    x = (y + 3) * 3;
    
    if (x == 30) {
        x = 10;      
        var(int) x;
    };
    
    y = x;
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
