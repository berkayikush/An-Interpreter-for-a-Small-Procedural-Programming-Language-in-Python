class ASTNodeVisitor:
    def visit(self, ast_node):
        execute = getattr(self, "visit" + type(ast_node).__name__, self.no_visit_method)
        return execute(ast_node)

    def no_visit(self, node):
        """
        Raise an exception if no visit method is implemented for a node.
        """
        raise Exception(f"No visit_{type(node).__name__} method.")
