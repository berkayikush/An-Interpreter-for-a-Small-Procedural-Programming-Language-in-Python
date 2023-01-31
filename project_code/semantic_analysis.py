from .tokens import Token
from .abstract_syntax_tree import VarNode
from .visit_ast_node import ASTNodeVisitor
from .scope_symbol_table import (
    ScopeSymbolTable,
    BuiltInTypeSymbol,
    VariableSymbol,
    ConditionalSymbol,
    LoopSymbol,
)
from .type_checking import TypeChecker
from .error import SemanticAnalysisError


class SemanticAnalyzer(ASTNodeVisitor):
    def __init__(self):
        self.__current_scope_symbol_table = ScopeSymbolTable(
            scope_name="global", scope_level=1, outer_scope=None
        )
        self.__current_scope_symbol_table.add_built_in_symbols()

    def visitVarNode(self, ast_node):
        variable_symbol = self.__current_scope_symbol_table.get_symbol(ast_node.value)

        if variable_symbol is None:
            self.__error(SemanticAnalysisError.IDENTIFIER_NOT_FOUND, ast_node.value)

        return variable_symbol.type_

    def visitNumberNode(self, ast_node):
        if isinstance(ast_node.value, int):
            return BuiltInTypeSymbol(Token.K_INT)

        return BuiltInTypeSymbol(Token.K_FLOAT)

    def visitBoolNode(self, ast_node):
        return BuiltInTypeSymbol(Token.K_STR)

    def visitStrNode(self, ast_node):
        return BuiltInTypeSymbol(Token.K_STR)

    def visitUnaryOpNode(self, ast_node):
        return TypeChecker.check_unary_op(
            ast_node.op_token.type_,
            child_node_type=self.visit(ast_node.child_node).name,
        )

    def visitBinaryOpNode(self, ast_node):
        return TypeChecker.check_binary_op(
            ast_node.op_token.type_,
            left_node_type=self.visit(ast_node.left_node).name,
            right_node_type=self.visit(ast_node.right_node).name,
        )

    def visitEmptyStatementNode(self, ast_node):
        pass

    def visitAssignmentStatementNode(self, ast_node):
        TypeChecker.check_assignment_statement(
            var_type=self.visit(ast_node.left_node).name,
            var_val_type=self.visit(ast_node.right_node).name,
        )

    def visitConditionalStatementNode(self, ast_node):
        symbol_names = []
        self.__add_conditional_symbols_to_current_scope(ast_node, symbol_names)

        for i, (_, statement_list_node) in enumerate(ast_node.if_cases):
            self.__current_scope_symbol_table = ScopeSymbolTable(
                scope_name=symbol_names[i],
                scope_level=self.__current_scope_symbol_table.scope_level + 1,
                outer_scope=self.__current_scope_symbol_table,
            )

            self.visit(statement_list_node)

            self.__current_scope_symbol_table = (
                self.__current_scope_symbol_table.outer_scope
            )

        if ast_node.else_case is not None:
            self.__current_scope_symbol_table = ScopeSymbolTable(
                scope_name=symbol_names[-1],
                scope_level=self.__current_scope_symbol_table.scope_level + 1,
                outer_scope=self.__current_scope_symbol_table,
            )

            self.visit(ast_node.else_case)

            self.__current_scope_symbol_table = (
                self.__current_scope_symbol_table.outer_scope
            )

    def __add_conditional_symbols_to_current_scope(self, ast_node, symbol_names):
        for i, (condition, _) in enumerate(ast_node.if_cases):
            self.visit(condition)
            name = "if" if i == 0 else "elseif"

            if_elseif_symbol = ConditionalSymbol(name)
            symbol_names.append(if_elseif_symbol.name)

            self.__current_scope_symbol_table.add_symbol(if_elseif_symbol)

        if ast_node.else_case is not None:
            else_symbol = ConditionalSymbol("else")
            symbol_names.append(else_symbol.name)

            self.__current_scope_symbol_table.add_symbol(else_symbol)

    def visitRangeExprNode(self, ast_node):
        return TypeChecker.check_range_expr(
            start_type=self.visit(ast_node.start_val).name,
            end_type=self.visit(ast_node.end_val).name,
            step_type=self.visit(ast_node.step_val).name if ast_node.step_val else None,
        )

    def visitForStatementNode(self, ast_node):
        iterable_type = self.visit(ast_node.iterable).name
        TypeChecker.check_iterable(iterable_type)

        for_symbol = LoopSymbol("for")
        self.__current_scope_symbol_table.add_symbol(for_symbol)

        self.__current_scope_symbol_table = ScopeSymbolTable(
            scope_name=for_symbol.name,
            scope_level=self.__current_scope_symbol_table.scope_level + 1,
            outer_scope=self.__current_scope_symbol_table,
        )

        self.visit(ast_node.var_decl_statement_node)
        TypeChecker.check_assignment_statement(
            var_type=self.visit(ast_node.var_decl_statement_node.variables[0]).name,
            var_val_type=(
                self.visit(ast_node.iterable.start_val).name
                if iterable_type == Token.K_RANGE
                else iterable_type
            ),
        )

        self.visit(ast_node.statement_list_node)
        self.__current_scope_symbol_table = (
            self.__current_scope_symbol_table.outer_scope
        )

    def visitWhileStatementNode(self, ast_node):
        self.visit(ast_node.condition)

        while_symbol = LoopSymbol("while")
        self.__current_scope_symbol_table.add_symbol(while_symbol)

        self.__current_scope_symbol_table = ScopeSymbolTable(
            scope_name=while_symbol.name,
            scope_level=self.__current_scope_symbol_table.scope_level + 1,
            outer_scope=self.__current_scope_symbol_table,
        )

        self.visit(ast_node.statement_list_node)
        self.__current_scope_symbol_table = (
            self.__current_scope_symbol_table.outer_scope
        )

    def visitVarDeclStatementNode(self, ast_node, check_outer_scope=False):
        type_symbol = self.__current_scope_symbol_table.get_symbol(
            ast_node.var_type_node.value
        )

        for variable in ast_node.variables:
            if isinstance(variable, VarNode):
                var_name = variable.value
            else:
                TypeChecker.check_assignment_statement(
                    var_type=type_symbol.name,
                    var_val_type=self.visit(variable.right_node).name,
                )
                var_name = variable.left_node.value

            variable_symbol = VariableSymbol(var_name, type_symbol)
            check_outer_scope = (
                self.__current_scope_symbol_table.scope_name == "global"
                or self.__current_scope_symbol_table.scope_name.startswith("if")
                or self.__current_scope_symbol_table.scope_name.startswith("elseif")
                or self.__current_scope_symbol_table.scope_name.startswith("else")
                or self.__current_scope_symbol_table.scope_name.startswith("while")
                or self.__current_scope_symbol_table.scope_name.startswith("for")
            )

            if (
                self.__current_scope_symbol_table.get_symbol(
                    var_name, check_outer_scope=check_outer_scope
                )
                is not None
            ):
                self.__error(SemanticAnalysisError.IDENTIFIER_ALREADY_DEFINED, var_name)

            self.__current_scope_symbol_table.add_symbol(variable_symbol)

    def visitFuncDeclStatementNode(self, ast_node):
        pass

    def visitStatementListNode(self, ast_node):
        for statement in ast_node.statements:
            self.visit(statement)

    def visitProgramNode(self, ast_node):
        self.visit(ast_node.statement_list_node)

        self.__current_scope_symbol_table = (
            self.__current_scope_symbol_table.outer_scope
        )

    def __error(self, error_code, value):
        raise SemanticAnalysisError(error_message=f"{error_code}: {value}", value=value)
