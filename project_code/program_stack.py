class ProgramStack:
    def __init__(self):
        self.stack = []

    def push(self, frame):
        self.stack.append(frame)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def size(self):
        return len(self.stack)


class StackFrame:
    ###############
    # Frame Types #
    ###############
    GLOBAL = "GLOBAL"
    CONDITIONAL_STATEMENT = "CONDITIONAL_STATEMENT"
    WHILE_STATEMENT = "WHILE_STATEMENT"
    FOR_STATEMENT = "FOR_STATEMENT"
    FUNC = "FUNC"

    def __init__(self, name, type_, scope_level, outer_scope=None):
        self.__name = name
        self.__type_ = type_

        self.__scope_level = scope_level
        self.__variables = {}
        self.__outer_scope = outer_scope

    @property
    def scope_level(self):
        return self.__scope_level

    @property
    def outer_scope(self):
        return self.__outer_scope

    def get(self, key, default=None):
        if self.__check_variable(key):
            return self.__variables[key]

        if self.__outer_scope is not None:
            return self.__outer_scope.get(key)

        return default

    def __check_variable(self, variable):
        return variable in self.__variables

    def set(self, key, val):
        if self.__check_variable(key):
            self.__variables[key] = val
            return

        self.__outer_scope.set(key, val)

    def __setitem__(self, key, val):
        self.__variables[key] = val
