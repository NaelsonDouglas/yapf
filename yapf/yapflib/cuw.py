import ast
from ast import Call, For, Load, Name, Store, Assign, Expr, Attribute, Constant
from typing import List, Tuple

_OPEN_STREAM = Assign(value=Call(func=Name(id='open')))
_CLOSE_STREAM = Expr(value=Call(func=Attribute(value=Name(ctx=Load()),attr='close',ctx=Load())))

def fix(node:ast.AST) -> ast.AST:
    if hasattr(node, 'body'):
        match node.body:
            case (_OPEN_STREAM, _, _CLOSE_STREAM, *_) | (*_, _OPEN_STREAM, _, _CLOSE_STREAM):
                node.body = _update_body(node.body)
                return node
            case _:
                return node
    else:
        return node

def _update_body(body:List[ast.AST]) -> List[ast.AST]:
    pairs = _mark_open_close_pairs(body)
    new_body = body[0::]
    for pair in pairs:
        (var_name,
        opening_leaf,
        resource) = pair[0]
        closing_leaf = pair[1]
        content = body[opening_leaf+1:closing_leaf]
        with_node = _build_with_node(var_name,resource,content,body[opening_leaf].lineno)
        new_body[opening_leaf:closing_leaf+1] = (closing_leaf-opening_leaf)*[None]+[with_node]
    new_body = [node for node in new_body if node is not None]
    return new_body

def _build_with_node(var_name:str, resource:str, content:List, lineno:int):
    with_statement = ast.With()
    open_call = Call(func=Name(id='open', ctx=Load()),args=[Constant(value=resource)],keywords=[])
    with_item = ast.withitem(context_expr=open_call, optional_vars=Name(id=var_name, ctx=Store()))

    with_statement.body = content
    with_statement.items = [with_item]
    with_statement.lineno = lineno
    return with_statement

def _mark_open_close_pairs(body:List[ast.AST]) -> Tuple:
    pairs = {}
    for index, node in enumerate(body):
        if isinstance(node, Assign) and _is_open_function_call(node): #Marks where the stream is opened
            var_name = node.targets[0].id
            pairs[var_name] = pairs.get(var_name, [])
            resource = node.value.args[0].value
            pairs[var_name].append((var_name, index, resource))
        elif isinstance(node, Expr) and _is_close_function_call(node): #Marks where the stream is closed
            var_name = node.value.func.value.id
            pairs[var_name].append(index)
    pairs = pairs.values()
    pairs = sorted(pairs, key=lambda x: x[0][1])
    return pairs

def _has_field(node:ast.AST, field:str, field_type:object):
    return hasattr(node,field) and isinstance(getattr(node, field), field_type)

def _is_open_function_call(node):
    return (_has_field(node, 'value', ast.Call) and
            _has_field(node.value, 'func', ast.Name) and
            node.value.func.id == 'open'
        )

def _is_close_function_call(node):
    return (_has_field(node, 'value', ast.Call) and
            _has_field(node.value, 'func', ast.Attribute) and
            node.value.func.attr == 'close'
        )
def _replace_leafs(node: ast.For) -> ast.For:
    #TODO
    return node

