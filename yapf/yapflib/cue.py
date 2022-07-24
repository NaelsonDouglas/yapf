import ast
from ast import Call, For, Load, Name, Store


def fix(node:ast.For) -> ast.For:
    match node:
        case For(target=Name(ctx=Store()),
                    iter=Call(
                            func=Name(id='range'),
                            args=[Call(func=Name(id='len'))],
                        ),
                    body=[*_, _]
                ):
                return _replace_leafs(node)
        case _:
            return node

def _replace_leafs(node: ast.For) -> ast.For:
    iterable = node.iter.args[0].args[0].id
    target_id = node.target.id
    new_loop = ast.parse(f'for {target_id}, value in {iterable}:\t pass')
    new_body = ast.parse(ast.unparse(node.body).replace(f'{iterable}[{target_id}]', 'value'))
    new_loop.lineno = node.lineno
    new_loop.body[0].body = [new_body]
    return new_loop
