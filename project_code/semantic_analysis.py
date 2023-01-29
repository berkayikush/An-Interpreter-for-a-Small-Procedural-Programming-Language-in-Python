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
        op_token_type = ast_node.op_token.type_
        child_node_type = self.visit(ast_node.child_node).name

        if op_token_type == Token.K_NOT:
            return BuiltInTypeSymbol(Token.K_BOOL)

        if op_token_type in (Token.MINUS, Token.PLUS):
            match child_node_type:
                case Token.K_STR:
                    self.__error(
                        SemanticAnalysisError.INVALID_OPERATION, ast_node.op_token.value
                    )

                case Token.K_FLOAT:
                    return BuiltInTypeSymbol(Token.K_FLOAT)

                case _:  # Token.K_INT, Token.K_BOOL
                    return BuiltInTypeSymbol(Token.K_INT)

    def visitBinaryOpNode(self, ast_node):
        left_node_type = self.visit(ast_node.left_node).name
        right_node_type = self.visit(ast_node.right_node).name
        op_token_type = ast_node.op_token.type_

        if op_token_type == Token.PLUS and (
            left_node_type == Token.K_STR and right_node_type == Token.K_STR
        ):
            return BuiltInTypeSymbol(Token.K_STR)

        if op_token_type in (
            Token.PLUS,
            Token.MINUS,
            Token.MULTIPLICATION,
            Token.FLOAT_DIVISION,
            Token.INT_DIVISION,
            Token.MODULO,
        ):
            if Token.K_STR in (left_node_type, right_node_type):
                self.__error(
                    SemanticAnalysisError.INVALID_OPERATION, ast_node.op_token.value
                )

            if (Token.K_FLOAT in (left_node_type, right_node_type)) and (
                op_token_type != Token.INT_DIVISION
            ):
                return BuiltInTypeSymbol(Token.K_FLOAT)

            return BuiltInTypeSymbol(Token.K_INT)

        if op_token_type in (Token.EQUALS, Token.NOT_EQUALS):
            return BuiltInTypeSymbol(Token.K_BOOL)

        if op_token_type in (
            Token.LESS_THAN,
            Token.LESS_THAN_OR_EQUALS,
            Token.GREATER_THAN,
            Token.GREATER_THAN_OR_EQUALS,
        ):
            if left_node_type == Token.K_STR and right_node_type == Token.K_STR:
                return BuiltInTypeSymbol(Token.K_BOOL)

            if Token.K_STR in (left_node_type, right_node_type):
                self.__error(
                    SemanticAnalysisError.INVALID_OPERATION, ast_node.op_token.value
                )

            return BuiltInTypeSymbol(Token.K_BOOL)

        if op_token_type == Token.K_AND:
            return BuiltInTypeSymbol(right_node_type)

        if op_token_type == Token.K_OR:
            return BuiltInTypeSymbol(left_node_type)

    def visitEmptyStatementNode(self, ast_node):
        pass

    def visitAssignStatementNode(self, ast_node):
        var_val_type = self.visit(ast_node.right_node).name
        var_type = self.visit(ast_node.left_node).name

        if var_val_type != var_type:
            self.__error(
                SemanticAnalysisError.INVALID_ASSIGNMENT,
                f"Cannot assign {var_val_type} to {var_type}",
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
            name, type_ = ("if", Token.K_IF) if i == 0 else ("elseif", Token.K_ELSEIF)

            if_elseif_symbol = ConditionalSymbol(name, BuiltInTypeSymbol(type_))
            symbol_names.append(if_elseif_symbol.name)

            self.__current_scope_symbol_table.add_symbol(if_elseif_symbol)

        if ast_node.else_case is not None:
            else_symbol = ConditionalSymbol("else", BuiltInTypeSymbol(Token.K_ELSE))
            symbol_names.append(else_symbol.name)

            self.__current_scope_symbol_table.add_symbol(else_symbol)

    def visitRangeExprNode(self, ast_node):
        start_type = self.visit(ast_node.start_node).name

        if start_type not in (Token.K_INT, Token.K_BOOL):
            self.__error(
                SemanticAnalysisError.INVALID_OPERATION,
                f"Range start value must be of type {Token.K_INT}",
            )

        end_type = self.visit(ast_node.end_node).name

        if end_type not in (Token.K_INT, Token.K_BOOL):
            self.__error(
                SemanticAnalysisError.INVALID_OPERATION,
                f"Range end value must be of type {Token.K_INT}",
            )

        if ast_node.step_node is not None:
            step_type = self.visit(ast_node.step_node).name

            if step_type not in (Token.K_INT, Token.K_BOOL):
                self.__error(
                    SemanticAnalysisError.INVALID_OPERATION,
                    f"Range step value must be of type {Token.K_INT}",
                )

        return BuiltInTypeSymbol(Token.K_RANGE)

    def visitForStatementNode(self, ast_node):
        to_loop_through_type = self.visit(ast_node.to_loop_through).name

        if to_loop_through_type not in (Token.K_RANGE, Token.K_STR):
            self.__error(
                SemanticAnalysisError.INVALID_OPERATION,
                f"Cannot loop through {to_loop_through_type}",
            )

        for_symbol = LoopSymbol("for", BuiltInTypeSymbol(Token.K_FOR))
        self.__current_scope_symbol_table.add_symbol(for_symbol)

        self.__current_scope_symbol_table = ScopeSymbolTable(
            scope_name=for_symbol.name,
            scope_level=self.__current_scope_symbol_table.scope_level + 1,
            outer_scope=self.__current_scope_symbol_table,
        )

        self.visit(ast_node.var_decl_statement_node)
        var_type = self.visit(ast_node.var_decl_statement_node.variables[0]).name
        var_val_type = (
            self.visit(ast_node.to_loop_through.start_node).name
            if to_loop_through_type == Token.K_RANGE
            else to_loop_through_type
        )

        if var_type != var_val_type:
            self.__error(
                SemanticAnalysisError.INVALID_OPERATION,
                f"Cannot loop through {to_loop_through_type} with {var_type}",
            )

        self.visit(ast_node.statement_list_node)
        self.__current_scope_symbol_table = (
            self.__current_scope_symbol_table.outer_scope
        )

    def visitWhileStatementNode(self, ast_node):
        self.visit(ast_node.condition)

        while_symbol = LoopSymbol("while", BuiltInTypeSymbol(Token.K_WHILE))
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
                variable_name = variable.value
            else:
                var_val_type = self.visit(variable.right_node).name

                if var_val_type != type_symbol.name:
                    self.__error(
                        SemanticAnalysisError.INVALID_ASSIGNMENT,
                        f"Cannot assign {var_val_type} to {type_symbol}",
                    )

                variable_name = variable.left_node.value

            variable_symbol = VariableSymbol(variable_name, type_symbol)

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
                    variable_name, check_outer_scope=check_outer_scope
                )
                is not None
            ):
                self.__error(
                    SemanticAnalysisError.IDENTIFIER_ALREADY_DEFINED, variable_name
                )

            self.__current_scope_symbol_table.add_symbol(variable_symbol)

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
