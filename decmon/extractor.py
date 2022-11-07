from re import findall, match

op_sets = ["grounds", "atoms", "classic_operators", "temporal_operators"]
grounds = ["True", "False"]
atoms = ["Var"]
classic_operators = ["And", "Or", "Neg", "Imp", "Iff", "Xor"]
temporal_operators = ["Until", "Next", "Ev", "Glob", "Previous", "Wuntil"]
all_operators = [grounds, atoms, classic_operators, temporal_operators]

ALPHABET_OFFSET = 96


def count_op(op: str, source: str) -> int:
    """
    Counts the given word op in the source string
    :param op: the word to match
    :param source: the text in which the word must be found
    :return: the number of occurrences of the word
    """
    return len(findall(op, source))


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
    return findall(r'{.*?}', source)


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


############################################
#   FORMULA ENCODING FUNCTIONS             #
############################################


def flatten_once(ls: list[list]) -> list:
    """
    Flattens a list of lists, not recursively
    :param ls: list of lists of elements to flatten
    :return: a list of elements
    """
    return [item for sublist in ls for item in sublist]


def encode_ops(source: str) -> list[int]:
    """
    Encodes the given source string in a list of integers
    :param source: text to encode
    :return: list of integers
    """
    return encode_tree(tree_as_array(source.strip()))


def encode_tree(source: list[str]) -> list[int]:
    """
    Encodes the given source string in a list of integers
    :param source: text to encode
    :return: list of integers
    """
    return [convert_op_to_int(op) for op in source]


def tree_as_array(source: str) -> list[str]:
    """
    Encodes the given source string in a list of integers
    :param source: text to encode
    :return: list of integers
    """
    if convert_op_to_int(source) <= 0:
        return [source]

    left, right = split_op(source)
    inner_left, inner_right = split_internal_op(right)
    return [left] + tree_as_array(inner_left) + tree_as_array(inner_right)


def split_op(op: str) -> (str, str):
    """
    Splits the given operator in a list of its arguments
    :param op: operator to split
    :return: list of arguments
    """
    split = op.split(" ", 1)
    return split[0], split[1]


def split_internal_op(op: str) -> (str, str):
    """
    Splits the given operator in a list of its arguments
    :param op: operator to split
    :return: list of arguments
    """
    split = find_outmost_comma(op)
    if split is None:
        return op[1:-1], "0"
    return op[1:split], op[split + 2:-1]


def find_outmost_comma(source: str) -> int | None:
    """
    Finds the outmost comma in the given source string
    :param source: text in which the comma must be found
    :return: index of the outmost comma
    """
    count = 0
    for(i, c) in enumerate(source):
        if c == "(":
            count += 1
        elif c == ")":
            count -= 1
        elif c == "," and count == 1:
            return i


def convert_op_to_int(op: str) -> int:
    """
    We categorize operators
    :param op: operator
    :return: integer encoding of the operator
    """
    if op == "0":
        return 0
    elif op == 'True':
        return 1
    elif op == 'False':
        return 2
    elif match(r'Var "\w+"', op):
        return parse_event(op)
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
        return 15
    else:
        return 3


def parse_event(event: str) -> int:
    """
    Parses the given event
    :param event: event to parse
    :return: parsed event
    """
    _, right = event.split(" ", 1)
    return convert_event_to_int(right[1:-1])


def convert_event_to_int(label: str) -> int:
    """
    We categorize observed events
    :param label: observed events
    :return: integer encoding of the event
    """
    value = ord(label) - ALPHABET_OFFSET
    print("Event: " + label + " -> " + str(-value))
    if value < 0 or value > 25:
        raise Exception("Invalid event label: " + label)
    return - value
    # else:
    #     return 0    # TODO: used by trace encoding, was only considering
    #                 # events like a, b, or c.
    #                 # can end in inf loop with formula, needs refactoring
