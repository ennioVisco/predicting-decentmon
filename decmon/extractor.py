import re

op_sets = ["grounds", "atoms", "classic_operators", "temporal_operators"]
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


def count_set_ops(ops_set: list[str], source: str) -> list[int]:
    """
    Counts the given list of words in the given source string
    :param ops_set: set of words to match
    :param source: text in which the words must be found
    :return: positional list of numbers of occurrences,
    where the i-th number is the number of occurrences of the i-th word
    """
    return [count_op(op, source) for op in ops_set]


def count_all_ops(source: str) -> list[list[int]]:
    """
    Counts all the known words in the given source string
    :param source: text in which the words must be found
    :return: list of lists of numbers of occurrences,
    where each list corresponds to each list of known words
    """
    return [count_set_ops(ops_set, source) for ops_set in all_operators]


def extract_event_samples(source: str) -> list[str]:
    """
    Extracts the event samples from the given source string
    :param source: text in which the samples must be found
    :return: list of samples
    """
    return re.findall(r'{.*?}', source)


def extract_events(source: str) -> list[str]:
    """
    Extracts the events from the given source string
    :param source: text in which the events must be found
    :return: list of events
    """
    source = source[1:-1]
    return [event for event in source.split("|")]


def extract_sampled_events(source: str) -> list[list[str]]:
    """
    Extracts the samples and for each, the respective events,
     from the given source string
    :param source: text in which the events must be found
    :return: list of lists of events
    """
    samples = extract_event_samples(source)
    return [extract_events(sample) for sample in samples]


def convert_event_to_int(label: str) -> int:
    """
    We categorize observed events
    :param label: observed events
    :return: integer encoding of the event
    """
    if label == 'a':
        return 1
    elif label == 'b':
        return 2
    elif label == 'c':
        return 3
    else:
        return 0


def flatten_once(ls: list[list]) -> list:
    """
    Flattens a list of lists, not recursively
    :param ls: list of lists of elements to flatten
    :return: a list of elements
    """
    return [item for sublist in ls for item in sublist]
