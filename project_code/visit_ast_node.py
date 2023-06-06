class ASTNodeVisitor:
    def visit(self, ast_node):
        execute = getattr(self, "visit" + type(ast_node).__name__, self.no_visit)
        return execute(ast_node)

    def no_visit(self, ast_node):
        """
        Raise an exception if no visit method is implemented for a node.
        """
        raise NotImplementedError(
            f'NotImplementedError: "visit{type(ast_node).__name__}" not implemented.'
        )
