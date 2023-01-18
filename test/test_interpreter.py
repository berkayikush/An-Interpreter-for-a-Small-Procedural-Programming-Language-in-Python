import unittest

from project_code.lexer import Lexer
from project_code.parser_ import Parser
from project_code.semantic_analysis import SemanticAnalyzer
from project_code.interpreter import Interpreter


class TestInterpreter(unittest.TestCase):
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

        self.assertEqual(interpreter.GLOBAL_MEMORY["x"], 2)
        self.assertEqual(interpreter.GLOBAL_MEMORY["y"], 3)
        self.assertEqual(interpreter.GLOBAL_MEMORY["z"], 5)

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

        self.assertEqual(interpreter.GLOBAL_MEMORY["x"], 7)
        self.assertEqual(interpreter.GLOBAL_MEMORY["y"], 1)
        self.assertEqual(interpreter.GLOBAL_MEMORY["z"], 7)

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

        self.assertEqual(interpreter.GLOBAL_MEMORY["x"], 7.0)
        self.assertEqual(interpreter.GLOBAL_MEMORY["y"], 4.0)
        self.assertEqual(interpreter.GLOBAL_MEMORY["z"], 7.0 / 4.0)

    def test_interpreter_with_bool(self):
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

        interpreter = Interpreter(tree)
        interpreter.interpret()

        self.assertEqual(interpreter.GLOBAL_MEMORY["x"], True)
        self.assertEqual(interpreter.GLOBAL_MEMORY["y"], False)
        self.assertEqual(interpreter.GLOBAL_MEMORY["z"], False)
        self.assertEqual(interpreter.GLOBAL_MEMORY["a"], True)

    def test_interpreter_with_comp(self):
        text = """
        var(int) x = 3, y = 2;
        var(bool) z = x > y;
        
        var(bool) a = x < y;
        var(bool) b = x == y;
        
        var(bool) c = x != y;
        """
        lexer = Lexer(text)
        parser = Parser(lexer)
        tree = parser.parse()

        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(tree)

        interpreter = Interpreter(tree)
        interpreter.interpret()

        self.assertEqual(interpreter.GLOBAL_MEMORY["x"], 3)
        self.assertEqual(interpreter.GLOBAL_MEMORY["y"], 2)
        self.assertEqual(interpreter.GLOBAL_MEMORY["z"], True)
        self.assertEqual(interpreter.GLOBAL_MEMORY["a"], False)
        self.assertEqual(interpreter.GLOBAL_MEMORY["b"], False)
        self.assertEqual(interpreter.GLOBAL_MEMORY["c"], True)

    def test_interpreter_with_plus_assign_and_logical(self):
        text = """
        var(int) x = 3, y = 2;
        x += 3 and y;
        """
        lexer = Lexer(text)
        parser = Parser(lexer)
        tree = parser.parse()

        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(tree)

        interpreter = Interpreter(tree)
        interpreter.interpret()

        self.assertEqual(interpreter.GLOBAL_MEMORY["x"], 5)
        self.assertEqual(interpreter.GLOBAL_MEMORY["y"], 2)
