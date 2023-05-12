from typing import Callable

from decmon.extractor import split_internal_op

"""
We want to get BNF, so we need to normalize the formulae:
elif op == 'True':
        return 1
    elif op == 'False':
        return 2
    elif op == 'And':
        return 4
    elif op == 'Or':
        return 5
    elif op == 'Neg':
        return 6
    elif op == 'Imp':
        return 7
    elif op == 'Iff':
        return 8
    elif op == 'Ev':
        return 12
    elif op == 'Glob':
        return 13
    elif op == 'Xor':
        return 9
    elif op == 'Until':
        return 10
    elif op == 'Next':
        return 11
    elif op == 'Previous':
        return 14
    elif op == 'Wuntil':
"""


def normalize(formula: str) -> str:
    """
    Transforms the given ltl formula into an equivalent one using only basic operators
    :param formula: input formula
    :return: output formula
    """
    if formula.startswith("Or"):
        return normalize_binary(formula, "Or", normalize_or)
    elif formula.startswith("Xor"):
        return normalize_binary(formula, "Xor", normalize_xor)
    elif formula.startswith("Imp"):
        return normalize_binary(formula, "Imp", normalize_imp)
    elif formula.startswith("Iff"):
        return normalize_binary(formula, "Iff", normalize_iff)
    elif formula.startswith("Ev"):
        return normalize_unary(formula, "Ev", normalize_ev)
    elif formula.startswith("Glob"):
        return normalize_unary(formula, "Glob", normalize_glob)
    else:
        return basic_ops(formula)


def basic_ops(formula: str) -> str:
    unary = ["Neg", "Next", "Previous"]
    for prefix in unary:
        if formula.startswith(f'{prefix}'):
            operand = formula[len(prefix) + 2:-1]
            return f'{prefix} ({normalize(operand)})'

    # Basic operators (binary)
    binary = ["And", "Until", "Wuntil"]
    for prefix in binary:
        if formula.startswith(f'{prefix}'):
            left, right = split_internal_op(formula[len(prefix) + 1:])
            return f'{prefix} ({normalize(left)}, {normalize(right)})'

    return formula


def normalize_binary(formula: str, op: str, f: Callable[[str, str], str]) -> str:
    left, right = split_internal_op(formula[len(op) + 1:])
    return f(left, right)


def normalize_unary(formula: str, op: str, f: Callable[[str], str]) -> str:
    operand = formula[len(op) + 2:-1]
    return f(operand)


def normalize_or(left: str, right: str) -> str:
    return normalize(f"Neg (And (Neg ({left}), Neg ({right})))")


def normalize_xor(left: str, right: str) -> str:
    return normalize(f"Or (And ({left}, Neg ({right})), And ({right}, Neg ({left})))")


def normalize_imp(left: str, right: str) -> str:
    return normalize(f"Or (Neg ({left}), {right})")


def normalize_iff(left: str, right: str) -> str:
    return normalize(f"And (Imp ({left}, {right}), Imp ({right}, {left}))")


def normalize_ev(f: str) -> str:
    return normalize(f"Until (True, {f})")


def normalize_glob(f: str) -> str:
    return normalize(f"Neg (Ev (Neg ({f})))")
