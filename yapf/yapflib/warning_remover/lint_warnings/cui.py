import ast

def fix(node:ast.BoolOp):
    assert isinstance(node, ast.BoolOp)
    comparing = {value for value in node.values if isinstance(value, ast.Compare)}
    not_comparing = set(node.values) - comparing
    comparing = list(comparing)
    _ids = {c.left.id for c in comparing}
    comparisons = dict([(_id, set()) for _id in _ids])
    for comparison in comparing:
        assert len(comparison.comparators) == 1
        comparisons[comparison.left.id].add(comparison.comparators[0].value)
    comparing = _dict_to_compares(comparisons)
    values = []
    values.extend(comparing)
    values.extend(not_comparing)
    return ast.BoolOp(ast.Or(), values)

def _dict_to_compares(comparisons:dict):
    compare_tuples = [(key, comparisons[key]) for key in comparisons]
    return [_tuple_to_compare(t) for t in compare_tuples]

def _tuple_to_compare(compare_tuple:tuple) -> ast.Compare:
    code_str = '%s in %s' % (compare_tuple[0], list(compare_tuple[1]))
    node = ast.parse(code_str, mode='eval').body
    assert isinstance(node, ast.Compare)
    return node

def is_comparing_boolop(node:ast.BoolOp):
    '''
        Checks wheter an ast.BoolOp contains an Or chained comparing expression.
        Example: 'a == 1 or x > 0'
    '''
    assert isinstance(node, ast.BoolOp)
    if isinstance(node.op, ast.Or):
        comparing_exps = {value for value in node.values if isinstance(value, ast.Compare)}
        return len(comparing_exps) > 0
    return False