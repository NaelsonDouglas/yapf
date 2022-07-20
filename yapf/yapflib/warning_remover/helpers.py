import ast

def dump(tree:ast.AST) -> None:
    print(ast.dump(tree, indent=4))