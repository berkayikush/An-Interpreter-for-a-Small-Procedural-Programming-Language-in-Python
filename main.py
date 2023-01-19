from project_code import interpreter
from project_code.lexer import Lexer
from project_code.parser_ import Parser
from project_code.semantic_analysis import SemanticAnalyzer
from project_code.interpreter import Interpreter


def main():
    text = """
    var(bool) x = true, y = false;
    
    if(x == true) {
        var(bool) y = true;
        
        if(y == true) {
            var(bool) y = false;
        };
    } elseif(x == false) {
        var(bool) y = false;
        x = y and x;
    } elseif(x == false) {
        var(bool) x = false;
    } else {
        var(bool) y = false;
    };
    
    if(x == true) {
        var(bool) y = true;
    }
    """

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()

    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.visit(tree)


if __name__ == "__main__":
    main()
