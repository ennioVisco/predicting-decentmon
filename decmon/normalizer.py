from re import sub, search, compile, Pattern

from decmon.extractor import split_internal_op

"""
We want to get BNF, so we need to normalize the formulae:
- Or (a, b) -> Neg (And (Neg (a), Neg (b)))
- Imp (a, b) -> Or (Neg (a), b) -> Neg (And (a, Neg (b)))
- Iff (a, b) -> And (Imp (a, b), Imp (b, a)) -> 
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
    elif op == 'Xor':
        return 9
    elif op == 'Until':
        return 10
    elif op == 'Next':
        return 11
    elif op == 'Ev':
        return 12
    elif op == 'Glob':
        return 13
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

    matches = binary_op("Or").fullmatch(formula)
    if matches is not None:
        return normalize_or(matches.group(1), matches.group(2))

    matches = binary_op("Imp").fullmatch(formula)
    if matches is not None:
        return normalize_imp(matches.group(1), matches.group(2))

    matches = binary_op("Iff").fullmatch(formula)
    if matches is not None:
        return normalize_iff(matches.group(1), matches.group(2))

    # Basic operators
    matches = unary_op("Neg").fullmatch(formula)
    if matches is not None:
        return f'Neg ({normalize(matches.group(1))})'

    if formula.startswith("And "):
        left, right = split_internal_op(formula[4:])
        print(left, right)
        return f'And ({normalize(left)}, {normalize(right)})'

    return formula


def normalize_or(left: str, right: str) -> str:
    return normalize(f"Neg (And (Neg ({left}), Neg ({right})))")


def normalize_and(left: str, right: str) -> str:
    return f"And ({normalize(left)}, {normalize(right)})"


def normalize_imp(left: str, right: str) -> str:
    return normalize(f"Or (Neg ({left}), {right})")


def normalize_iff(left: str, right: str) -> str:
    return normalize(f"And (Imp ({left}, {right}), Imp ({right}, {left}))")


def binary_op(op: str) -> Pattern:
    return compile(fr"{op} \((.+), (.+)\)")


def unary_op(op: str) -> Pattern:
    return compile(fr"{op} \((.+)\)")

