from .tokens import Token


class ScopeSymbolTable:
    def __init__(self, scope_name, scope_level, outside_scope=None):
        self.__scope_name = scope_name
        self.__scope_level = scope_level
        self.__outside_scope = outside_scope

        self.__symbols = {
            "int": BuiltInTypeSymbol(Token.K_INT),
            "float": BuiltInTypeSymbol(Token.K_FLOAT),
            "bool": BuiltInTypeSymbol(Token.K_BOOL),
            "if": BuiltInTypeSymbol(Token.K_IF),
            "elseif": BuiltInTypeSymbol(Token.K_ELSEIF),
            "else": BuiltInTypeSymbol(Token.K_ELSE),
        }

    @property
    def scope_name(self):
        return self.__scope_name

    @property
    def scope_level(self):
        return self.__scope_level

    @property
    def outside_scope(self):
        return self.__outside_scope

    def add_symbol(self, symbol):
        self.__symbols[symbol.name] = symbol

    def __check_symbol(self, name):
        return name in self.__symbols

    def get_symbol(self, name, check_outside_scope=True):
        if self.__check_symbol(name):
            return self.__symbols[name]

        if not check_outside_scope:
            return None

        if self.__outside_scope is not None:
            return self.__outside_scope.get_symbol(name)

    def __str__(self):
        return (
            f"Scope: {self.__scope_name}\n"
            f"Level: {self.__scope_level}\n"
            f"Outside scope: {self.__outside_scope.scope_name if self.__outside_scope else None}\n"
            "Content:\n"
            "{" + "\n".join(f"\t{k}: {v}," for k, v in self.__symbols.items()) + "\n}"
        )

    def __repr__(self):
        return self.__str__()


class Symbol:
    def __init__(self, name, type_=None):
        self._name = name
        self._type_ = type_

    @property
    def name(self):
        return self._name

    @property
    def type_(self):
        return self._type_


class BuiltInTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return f"BuiltInType({self._name})"

    def __repr__(self):
        return self.__str__()


class VariableSymbol(Symbol):
    """
    Used to make sure that we assign the correct type to a variable.
    Also used to make sure that a variable is declared before it is used.
    """

    def __init__(self, name, type_):
        super().__init__(name, type_)

    def __str__(self):
        return f"Variable({self._name}:{self._type_})"

    def __repr__(self):
        return self.__str__()


class IfElseIfElseSymbol(Symbol):
    def __init__(self, name, type_):
        super().__init__(name=f"{name}_{id(self)}", type_=type_)

    def __str__(self):
        return f"IfElseIfElse({self._name}:{self._type_})"

    def __repr__(self):
        return self.__str__()
