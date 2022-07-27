import re
from typing import List

grounds = ["True", "False"]
atoms = ["Var"]
classic_operators = ["And", "Or", "Neg", "Imp", "Iff", "Xor"]
temporal_operators = ["Until", "Next", "Ev", "Glob", "Previous", "Wuntil"]
all_operators = [grounds, atoms, classic_operators, temporal_operators]


def count_op(op: str, source: str) -> int:
    return len(re.findall(op, source))


def count_set_ops(ops_set: List[str], source: str) -> List[int]:
    return [count_op(op, source) for op in ops_set]


def count_all_ops(source: str) -> List[List[int]]:
    return [count_set_ops(ops_set, source) for ops_set in all_operators]


"""
    |  Var x ->  "Var \""^x^"\""
    =========================================================================================
    | True ->  "True"
    | False ->  "False"
    ==========================================================================================
    | SHARP -> "#"
    ==========================================================================================
    | Glob x -> "Glob ("^string_rep x^")"
    | Ev x ->  "Ev ("^ string_rep x^")"
    | Next x ->  "Next ("^ string_rep x^  ")"
    | Until (x, y) ->  "Until ("^ string_rep x^  ", "^string_rep y^  ")"
    | Previous x -> "Previous ("^string_rep x^")"
    | Wuntil (x, y) ->  "W-Until ("^ string_rep x^  ", "^string_rep y^  ")"
    ==========================================================================================
    | Neg x ->  "Neg ("^ string_rep x^")"
    | And (x, y) ->  "And ("^ string_rep x^  ", "^ string_rep y^  ")"
    | Or (x, y) ->  "Or ("^ string_rep x^  ", "^string_rep y^  ")"
    | Iff (x, y) ->  "Iff ("^ string_rep x^  ", "^string_rep y^  ")"
    | Imp (x, y) ->  "Imp ("^ string_rep x^  ", "^string_rep y^  ")"
    | Xor (x,y) -> "Xor ("^string_rep x^","^string_rep y^")"
"""