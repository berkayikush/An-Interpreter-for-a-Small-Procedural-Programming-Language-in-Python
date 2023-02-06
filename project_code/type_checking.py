from .tokens import Token
from .scope_symbol_table import BuiltInTypeSymbol
from .error import SemnaticError


class TypeChecker:
    """
    Used the type rules from the programming language Java.
    """

    @staticmethod
    def check_unary_op(op_token, child_node_type):
        if op_token.type_ == Token.K_NOT:
            if child_node_type != Token.K_BOOL:
                TypeChecker.__error(
                    f'Operation "{op_token.val}" is not allowed on type "{child_node_type}"',
                    op_token,
                )

            return BuiltInTypeSymbol(Token.K_BOOL)

        if op_token.type_ in (Token.K_NOT, Token.MINUS, Token.PLUS):
            match child_node_type:
                case Token.K_STR | Token.K_BOOL:
                    TypeChecker.__error(
                        f'Operation "{op_token.val}" is not allowed on type "{child_node_type}"',
                        op_token,
                    )

                case Token.K_FLOAT:
                    return BuiltInTypeSymbol(Token.K_FLOAT)

                case Token.K_INT:
                    return BuiltInTypeSymbol(Token.K_INT)

    @staticmethod
    def check_binary_op(op_token, left_node_type, right_node_type):
        if op_token.type_ in (
            Token.PLUS,
            Token.MINUS,
            Token.MULTIPLICATION,
            Token.FLOAT_DIVISION,
            Token.INT_DIVISION,
            Token.MODULO,
        ):
            return TypeChecker.__check_arithmetic_op(
                op_token, left_node_type, right_node_type
            )

        if op_token.type_ in (Token.EQUALS, Token.NOT_EQUALS):
            if left_node_type != right_node_type:
                TypeChecker.__error(
                    f'Cannot compare "{left_node_type}" and "{right_node_type}"',
                    op_token,
                )

            return BuiltInTypeSymbol(Token.K_BOOL)

        if op_token.type_ in (
            Token.LESS_THAN,
            Token.LESS_THAN_OR_EQUALS,
            Token.GREATER_THAN,
            Token.GREATER_THAN_OR_EQUALS,
        ):
            return TypeChecker.__check_comparison_op(
                op_token, left_node_type, right_node_type
            )

        if op_token.type_ in (Token.K_AND, Token.K_OR):
            if Token.K_BOOL not in (left_node_type, right_node_type):
                TypeChecker.__error(
                    f'Operation "{op_token.val}" is not allowed between "{left_node_type}" and "{right_node_type}"',
                    op_token,
                )

            return BuiltInTypeSymbol(Token.K_BOOL)

    @staticmethod
    def check_assignment_statement(var_type, var_val_type, var_val_token):
        if var_type != var_val_type:
            TypeChecker.__error(
                f'Cannot assign "{var_val_type}" to "{var_type}"', var_val_token
            )

    @staticmethod
    def check_condition(condition_type, condition_token):
        if condition_type != Token.K_BOOL:
            TypeChecker.__error(
                f'Condition must be "bool", not "{condition_type}"', condition_token
            )

    @staticmethod
    def check_range_expr(start_type, end_type, step_type, range_token):
        if (start_type != Token.K_INT) or (end_type != Token.K_INT):
            TypeChecker.__error('Start and end of range must be "int"', range_token)

        if step_type is not None and step_type != Token.K_INT:
            TypeChecker.__error('Step of range must be "int"', range_token)

        return BuiltInTypeSymbol(Token.K_RANGE)

    @staticmethod
    def check_iterable(iterable_type, iterable_token):
        if iterable_type not in (Token.K_RANGE, Token.K_STR):
            TypeChecker.__error(
                f'Cannot iterate over "{iterable_type}"', iterable_token
            )

    @staticmethod
    def __check_arithmetic_op(op_token, left_node_type, right_node_type):
        match (left_node_type, right_node_type):
            case (Token.K_STR, _) | (_, Token.K_STR):
                if op_token.type_ == Token.PLUS:
                    return BuiltInTypeSymbol(Token.K_STR)

                if op_token.type_ in Token.MULTIPLICATION and Token.K_INT in (
                    left_node_type,
                    right_node_type,
                ):
                    return BuiltInTypeSymbol(Token.K_STR)

                TypeChecker.__error(
                    f'Operation "{op_token.val}" is not allowed between "{left_node_type}" and "{right_node_type}"',
                    op_token,
                )

            case (Token.K_BOOL, _) | (_, Token.K_BOOL):
                TypeChecker.__error(
                    f'Operation "{op_token.val}" is not allowed between "{left_node_type}" and "{right_node_type}"',
                    op_token,
                )

            case (Token.K_FLOAT, _) | (_, Token.K_FLOAT):
                if op_token.type_ in Token.INT_DIVISION:
                    return BuiltInTypeSymbol(Token.K_INT)

                return BuiltInTypeSymbol(Token.K_FLOAT)

            case (_, _):
                return BuiltInTypeSymbol(Token.K_INT)

    @staticmethod
    def __check_comparison_op(op_token, left_node_type, right_node_type):
        match (left_node_type, right_node_type):
            case (Token.K_STR, Token.K_STR):
                return BuiltInTypeSymbol(Token.K_BOOL)

            case (Token.K_STR, _) | (_, Token.K_STR) | (Token.K_BOOL, _) | (
                _,
                Token.K_BOOL,
            ):
                TypeChecker.__error(
                    f'Operation "{op_token.val}" is not allowed between "{left_node_type}" and "{right_node_type}"',
                    op_token,
                )

            case (_, _):
                return BuiltInTypeSymbol(Token.K_BOOL)

    @staticmethod
    def __error(error_message, token):
        raise SemnaticError(
            error_message + f" on line: {token.line}, column: {token.col}",
        )
