import re
from typing import List

grounds = ["True", "False"]
atoms = ["Var"]
classic_operators = ["And", "Or", "Neg", "Imp", "Iff", "Xor"]
temporal_operators = ["Until", "Next", "Ev", "Glob", "Previous", "Wuntil"]
all_operators = [grounds, atoms, classic_operators, temporal_operators]


def count_op(op: str, source: str) -> int:
    """
    Counts the given word op in the source string
    :param op: the word to match
    :param source: the text in which the word must be found
    :return: the number of occurrences of the word
    """
    return len(re.findall(op, source))


def count_set_ops(ops_set: List[str], source: str) -> List[int]:
    """
    Counts the given list of words in the given source string
    :param ops_set: set of words to match
    :param source: text in which the words must be found
    :return: positional list of numbers of occurrences,
    where the i-th number is the number of occurrences of the i-th word
    """
    return [count_op(op, source) for op in ops_set]


def count_all_ops(source: str) -> List[List[int]]:
    """
    Counts all the known words in the given source string
    :param source: text in which the words must be found
    :return: list of lists of numbers of occurrences,
    where each list corresponds to each list of known words
    """
    return [count_set_ops(ops_set, source) for ops_set in all_operators]
