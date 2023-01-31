from .tokens import Token
from .scope_symbol_table import BuiltInTypeSymbol


class TypeChecker:
    @staticmethod
    def check_unary_op(op_token_type, child_node_type):
        if op_token_type == Token.K_NOT:
            return BuiltInTypeSymbol(Token.K_BOOL)

        if op_token_type in (Token.MINUS, Token.PLUS):
            match child_node_type:
                case Token.K_STR:
                    TypeChecker.__error()

                case Token.K_FLOAT:
                    return BuiltInTypeSymbol(Token.K_FLOAT)

                case _:  # Token.K_INT, Token.K_BOOL
                    return BuiltInTypeSymbol(Token.K_INT)

    @staticmethod
    def check_binary_op(op_token_type, left_node_type, right_node_type):
        if op_token_type in (
            Token.PLUS,
            Token.MINUS,
            Token.MULTIPLICATION,
            Token.FLOAT_DIVISION,
            Token.INT_DIVISION,
            Token.MODULO,
        ):
            return TypeChecker.__check_arithmetic_op(
                op_token_type, left_node_type, right_node_type
            )

        if op_token_type in (Token.EQUALS, Token.NOT_EQUALS):
            return BuiltInTypeSymbol(Token.K_BOOL)

        if op_token_type in (
            Token.LESS_THAN,
            Token.LESS_THAN_OR_EQUALS,
            Token.GREATER_THAN,
            Token.GREATER_THAN_OR_EQUALS,
        ):
            return TypeChecker.__check_comparison_op(left_node_type, right_node_type)

        if op_token_type == Token.K_AND:
            return BuiltInTypeSymbol(right_node_type)

        if op_token_type == Token.K_OR:
            return BuiltInTypeSymbol(left_node_type)

    @staticmethod
    def check_assignment_statement(var_type, var_val_type):
        if var_type != var_val_type:
            TypeChecker.__error()

    @staticmethod
    def check_range_expr(start_type, end_type, step_type):
        if start_type not in (Token.K_INT, Token.K_BOOL) or end_type not in (
            Token.K_INT,
            Token.K_BOOL,
        ):
            TypeChecker.__error()

        if step_type is not None and step_type not in (Token.K_INT, Token.K_BOOL):
            TypeChecker.__error()

        return BuiltInTypeSymbol(Token.K_RANGE)

    @staticmethod
    def check_iterable(iterable_type):
        if iterable_type not in (Token.K_RANGE, Token.K_STR):
            TypeChecker.__error()

    @staticmethod
    def __check_arithmetic_op(op_token_type, left_node_type, right_node_type):
        match (left_node_type, right_node_type):
            case (Token.K_STR, Token.K_STR):
                if op_token_type == Token.PLUS:
                    return BuiltInTypeSymbol(Token.K_STR)

                TypeChecker.__error()

            case (Token.K_STR, _):
                if op_token_type == Token.MULTIPLICATION:
                    return BuiltInTypeSymbol(Token.K_STR)

                TypeChecker.__error()

            case (_, Token.K_STR):
                if op_token_type == Token.MULTIPLICATION:
                    return BuiltInTypeSymbol(Token.K_STR)

                TypeChecker.__error()

            case (Token.K_FLOAT, Token.K_FLOAT):
                if op_token_type in Token.INT_DIVISION:
                    return BuiltInTypeSymbol(Token.K_INT)

                return BuiltInTypeSymbol(Token.K_FLOAT)

            case (Token.K_FLOAT, _):
                if op_token_type in Token.INT_DIVISION:
                    return BuiltInTypeSymbol(Token.K_INT)

                return BuiltInTypeSymbol(Token.K_FLOAT)

            case (_, Token.K_FLOAT):
                if op_token_type in Token.INT_DIVISION:
                    return BuiltInTypeSymbol(Token.K_INT)

                return BuiltInTypeSymbol(Token.K_FLOAT)

            case (_, _):
                return BuiltInTypeSymbol(Token.K_INT)

    @staticmethod
    def __check_comparison_op(left_node_type, right_node_type):
        match (left_node_type, right_node_type):
            case (Token.K_STR, Token.K_STR):
                return BuiltInTypeSymbol(Token.K_BOOL)

            case (Token.K_STR, _):
                TypeChecker.__error()

            case (_, Token.K_STR):
                TypeChecker.__error()

            case (_, _):
                return BuiltInTypeSymbol(Token.K_BOOL)

    @staticmethod
    def __error():
        raise Exception("Type error")
