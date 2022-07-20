import ast
from ast import Assign

from yapf.yapflib.warning_remover.engine import Visitor
from yapf.yapflib.warning_remover.detection import execute
from yapf.yapflib.warning_remover.lint_warnings import cui, ddv, cue, cuw, sc

from yapf.yapflib.warning_remover.helpers import dump

class Visitor(ast.NodeTransformer):
    def visit_BoolOp(self, node:ast.BoolOp) -> ast.BoolOp:
        fixed = node
        if cui.is_comparing_boolop(node):
            fixed = cui.fix(node)
        return self._visit(fixed)

    def visit_FunctionDef(self, node:ast.FunctionDef) -> ast.FunctionDef:
        fixed = ddv.fix(node)
        return self._visit(fixed)

    def visit_For(self, node:ast.For) -> ast.For:
        fixed = cue.fix(node)
        return self._visit(fixed)

    def visit_Compare(self, node:ast.For) -> ast.For:
        fixed = sc.fix(node)
        return self._visit(fixed)

    def _visit(self, node:ast.AST) -> ast.AST:
        self.generic_visit(node)
        fixed = cuw.fix(node)
        return fixed

def _ast_main():
    with open('samples/sc_sample.py') as f:
        text = f.read()

    tree = ast.parse(text)
    result = Visitor().visit(tree)
    result = ast.unparse(result)
    return tree, result

if __name__ == '__main__':
    tree, r = _ast_main()
    print(ast.unparse(tree))

# def _pylint_main():
#     FILE = 'samples/ddv_sample.py'
#     codes = {
#         'ddv' : 'W0102',
#         'cui' : 'R1714'
#     }

#     enabled = ','.join([
#         codes['ddv'],
#         codes['cui']
#     ])

#     r = execute(FILE, ['--disable=all', f'--enable={enabled}', '--output-format=json'])
#     return r