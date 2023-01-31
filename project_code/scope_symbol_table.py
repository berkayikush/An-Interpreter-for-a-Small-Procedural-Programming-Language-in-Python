from .tokens import Token


class ScopeSymbolTable:
    def __init__(self, scope_name, scope_level, outer_scope=None):
        self.__scope_name = scope_name
        self.__scope_level = scope_level

        self.__outer_scope = outer_scope
        self.__symbols = {}

    @property
    def scope_name(self):
        return self.__scope_name

    @property
    def scope_level(self):
        return self.__scope_level

    @property
    def outer_scope(self):
        return self.__outer_scope

    def add_built_in_symbols(self):
        self.__symbols = {
            "int": BuiltInTypeSymbol(Token.K_INT),
            "float": BuiltInTypeSymbol(Token.K_FLOAT),
            "bool": BuiltInTypeSymbol(Token.K_BOOL),
            "str": BuiltInTypeSymbol(Token.K_STR),
            "range": BuiltInTypeSymbol(Token.K_RANGE),
        }

    def add_symbol(self, symbol):
        self.__symbols[symbol.name] = symbol

    def get_symbol(self, name, check_outer_scope=True):
        if self.__check_symbol(name):
            return self.__symbols[name]

        if not check_outer_scope:
            return None

        if self.__outer_scope is not None:
            return self.__outer_scope.get_symbol(name)

    def __check_symbol(self, name):
        return name in self.__symbols


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


class VariableSymbol(Symbol):
    """
    Used to make sure that a variable is declared before it is used.
    """

    def __init__(self, name, type_):
        super().__init__(name, type_)


class ConditionalSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name=f"{name}_{id(self)}")


class LoopSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name=f"{name}_{id(self)}")
