import ast
from ast import Compare, Constant, Eq, Is
from typing import List, Tuple

from helpers import dump

def fix(node:ast.Compare) -> ast.Compare:
    match node:
        case (Compare(ops=[Eq()],comparators=[Constant(value=True)]) |
                Compare(ops=[Eq()],comparators=[Constant(value=False)]) |
                Compare(ops=[Eq()],comparators=[Constant(value=None)]) |
                Compare(ops=[Eq()], left=Constant(value=True)) |
                Compare(ops=[Eq()], left=Constant(value=False)) |
                Compare(ops=[Eq()], left=Constant(value=None))
            ):
                return _eq_to_is(node)
        case _:
            return node

def _eq_to_is(node:ast.Compare):
    node.ops = [Is()]
    return node