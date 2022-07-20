import ast
from ast import Call, For, Load, Name, Store

from helpers import dump

def fix(node:ast.For) -> ast.For:
    match node:
        case For(target=Name(ctx=Store()),
                    iter=Call(
                            func=Name(id='range', ctx=Load()),
                            args=[Call(func=Name(id='len', ctx=Load()), args=[Name(ctx=Load())])],
                            keywords=[]
                        ),
                    body=[*_, _]
                ):
                return _replace_leafs(node)
        case _:
            return node

def _replace_leafs(node: ast.For) -> ast.For:
    #TODO
    return node
