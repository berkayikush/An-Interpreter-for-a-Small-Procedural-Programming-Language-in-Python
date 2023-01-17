from project_code.lexer import Lexer
from project_code.parser_ import Parser
from project_code.interpreter import Interpreter
from project_code.semantic_analysis import SemanticAnalyzer


class TestInterpreter:
    def test_interpreter(self):
        text = """
        var(int) x, y;
        x = 2;
        y = 3;
        var(int) z = x + y;
        """
        lexer = Lexer(text)
        parser = Parser(lexer)
        tree = parser.parse()

        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(tree)

        interpreter = Interpreter(tree)
        interpreter.interpret()

        assert interpreter.GLOBAL_MEMORY["x"] == 2
        assert interpreter.GLOBAL_MEMORY["y"] == 3
        assert interpreter.GLOBAL_MEMORY["z"] == 5

    def test_interpreter_2(self):
        text = """
        var(int) x = 4, y = 2;
        x += 3;
        y -= 1;
        var(int) z = x // y;
        """
        lexer = Lexer(text)
        parser = Parser(lexer)
        tree = parser.parse()

        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(tree)

        interpreter = Interpreter(tree)
        interpreter.interpret()

        assert interpreter.GLOBAL_MEMORY["x"] == 7
        assert interpreter.GLOBAL_MEMORY["y"] == 1
        assert interpreter.GLOBAL_MEMORY["z"] == 7

    def test_interpreter_with_float(self):
        text = """
        var(float) x = 4.0, y = 2.0;
        x += 3.0;
        y *= 2.0;
        var(float) z = x / y;
        """
        lexer = Lexer(text)
        parser = Parser(lexer)
        tree = parser.parse()

        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(tree)

        interpreter = Interpreter(tree)
        interpreter.interpret()

        assert interpreter.GLOBAL_MEMORY["x"] == 7.0
        assert interpreter.GLOBAL_MEMORY["y"] == 4.0
        assert interpreter.GLOBAL_MEMORY["z"] == 7.0 / 4.0
