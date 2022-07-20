import ast
from typing import List, Tuple

MUTABLE_TYPES = (ast.List, ast.Dict, ast.Set) #TODO check if there is a built-in way to check if a node is mutable

def fix(node:ast.FunctionDef) -> ast.FunctionDef:
    new_defaults = _calc_new_defaults(node)
    defaults = _replace_defaults(new_defaults, node.args.defaults)
    initializers = _build_initializers(new_defaults, node)
    node.body = initializers + node.body
    node.args.defaults = defaults
    return node

def _build_initializers(defaults: List[ast.AST], node:ast.FunctionDef) -> List[ast.AST]:
    _body = node.body
    _args = [arg.arg for arg in node.args.args]
    initializers = []
    for index, new, old in defaults:
        if isinstance(old, MUTABLE_TYPES):
            initializer = 'if %s is None:\n   %s = %s' % (_args[index], _args[index], ast.unparse(defaults[index][2]))
            initializers.append(ast.parse(initializer))
    return initializers
def _replace_defaults(new_defaults:List[Tuple], old_defaults:List[ast.AST]) -> List[ast.AST]:
    result = []
    for index, new_value, old_value in new_defaults:
        if old_value:
            result.append(ast.Constant(value=None))
        else:
            result.append(old_defaults[index])
    return result

def _calc_new_defaults(node:ast.FunctionDef) -> List[Tuple]:
    new_defaults = []
    for index, default in enumerate(node.args.defaults):
        if isinstance(default, MUTABLE_TYPES):
            new_default = (index, ast.Constant(value=None), default)
        else:
            new_default = (index, default, None)
        new_defaults.append(new_default)
    return new_defaults