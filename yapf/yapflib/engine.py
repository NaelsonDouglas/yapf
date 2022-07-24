import ast
from ast import Assign

from yapf.yapflib import cui, ddv, cue, cuw, sc

def dump(tree:ast.AST) -> None:
    print(ast.dump(tree, indent=4))

class Visitor(ast.NodeTransformer):
    def visit_BoolOp(self, node:ast.BoolOp) -> ast.BoolOp:
        self.generic_visit(node)
        fixed = node
        if cui.is_comparing_boolop(node):
            fixed = cui.fix(node)
        return fixed

    def visit_FunctionDef(self, node:ast.FunctionDef) -> ast.FunctionDef:
        self.generic_visit(node)
        return ddv.fix(node)

    def visit_For(self, node:ast.For) -> ast.For:
        self.generic_visit(node)
        return cue.fix(node)

    def visit_Compare(self, node:ast.For) -> ast.For:
        self.generic_visit(node)
        return sc.fix(node)

    # def _visit(self, node:ast.AST) -> ast.AST:
    #     self.generic_visit(node)
    #     fixed = cuw.fix(node)
    #     return fixed
# def _ast_main():
#     with open('samples/sc_sample.py') as f:
#         text = f.read()

#     tree = ast.parse(text)
#     result = Visitor().visit(tree)
#     result = ast.unparse(result)
#     return tree, result

# if __name__ == '__main__':
#     tree, r = _ast_main()
#     print(ast.unparse(tree))