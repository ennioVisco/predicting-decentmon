import unittest

from decmon.extractor import *


class TestExtractor(unittest.TestCase):
    test_string = 'Until (Ev (Var "b"), And (Var "c", Var "a"))'
    test_trace = "{a|b| } ; { | | } ; {a| | }"

    def tests_it_works(self):
        self.assertEqual(True, True)

    def tests_finds_single_op(self):
        self.assertEqual(1, count_op("Until", self.test_string))

    def tests_finds_multiple_ops(self):
        self.assertEqual(3, count_op("Var", self.test_string))

    def tests_finds_temporal_ops(self):
        actual_sum = sum(count_set_ops(temporal_operators, self.test_string))
        self.assertEqual(2, actual_sum)

    def tests_finds_classic_ops(self):
        actual_sum = sum(count_set_ops(classic_operators, self.test_string))
        self.assertEqual(1, actual_sum)

    def tests_finds_all_ops(self):
        ops_counts = count_all_ops(self.test_string)
        clustered_ops_counts = list(map(sum, ops_counts))
        self.assertEqual(6, sum(clustered_ops_counts))

    def tests_finds_all_the_right_ops(self):
        ops_counts = count_all_ops(self.test_string)
        self.assertEqual([0, 0], ops_counts[0])
        self.assertEqual([3], ops_counts[1])
        self.assertEqual([1, 0, 0, 0, 0, 0], ops_counts[2])
        self.assertEqual([1, 0, 1, 0, 0, 0], ops_counts[3])

    def tests_can_extract_right_number_of_events(self):
        events = extract_event_samples(self.test_trace)
        self.assertEqual(3, len(events))

    def tests_can_extract_right_events_per_sample(self):
        samples = extract_event_samples(self.test_trace)
        events = extract_events(samples[0])
        self.assertEqual(3, len(events))
        self.assertEqual("a", events[0])
        self.assertEqual("b", events[1])
        self.assertEqual(" ", events[2])

    def tests_extract_all_sampled_events(self):
        events = extract_sampled_events(self.test_trace)
        self.assertEqual(3, len(events))
        self.assertEqual(3, len(events[0]))
        self.assertEqual(3, len(events[1]))
        self.assertEqual(3, len(events[2]))
        self.assertEqual("a", events[0][0])
        self.assertEqual("b", events[0][1])
        self.assertEqual(" ", events[0][2])
        self.assertEqual(" ", events[1][0])
        self.assertEqual(" ", events[1][1])
        self.assertEqual(" ", events[1][2])
        self.assertEqual("a", events[2][0])
        self.assertEqual(" ", events[2][1])
        self.assertEqual(" ", events[2][2])

    def tests_can_convert_alphabet_item_to_int(self):
        event = convert_event_to_int('a')
        self.assertEqual(-1, event)

    def tests_can_flatten_list(self):
        input_list = [[1, 2], [3, 4], [5, 6]]
        flattened = flatten_once(input_list)
        self.assertEqual(6, len(flattened))
        self.assertEqual(input_list[0][0], flattened[0])
        self.assertEqual(input_list[0][1], flattened[1])
        self.assertEqual(input_list[1][0], flattened[2])
        self.assertEqual(input_list[1][1], flattened[3])
        self.assertEqual(input_list[2][0], flattened[4])
        self.assertEqual(input_list[2][1], flattened[5])

    test_unary_formula = "Next (Var \"b\")"
    test_binary_formula = "Until (Var \"b\", Var \"a\")"

    def tests_correct_binary_detection(self):
        encoded = tree_as_array(self.test_binary_formula)
        self.assertEqual(3, len(encoded))
        self.assertEqual(["Until", "Var \"b\"", "Var \"a\""], encoded)

    def tests_correct_unary_detection(self):
        encoded = tree_as_array(self.test_unary_formula)
        self.assertEqual(3, len(encoded))
        self.assertEqual(["Next", "Var \"b\"", "0"], encoded)

    def tests_correct_op_encoding(self):
        to_encode = ["Next", "Var \"b\"", "0"]
        encoded = encode_tree(to_encode)
        self.assertEqual(11, encoded[0])
        self.assertEqual(-2, encoded[1])
        self.assertEqual(0, encoded[2])

    def tests_correct_atom_encoding(self):
        to_encode = "Var \"b\""
        encoded = encode_tree(tree_as_array(to_encode))
        self.assertEqual(1, len(encoded))

    def test_nested_formula_correctly_encoded(self):
        encoded = encode_tree(tree_as_array(self.test_string))
        self.assertEqual([10, 12, -2, 0, 4, -3, -1], encoded)

    def test_nested_formula_correctly_encoded_alternative(self):
        to_encode = "Ev (And (Var \"a\", Var \"b\"))"
        encoded = encode_ops(to_encode)
        self.assertEqual([12, 4, -1, -2, 0], encoded)

    def test_no_out_most_comma(self):
        to_encode = "Next (Var \"a\")"
        encoded = find_outmost_comma(to_encode)
        self.assertEqual(None, encoded)

    def test_no_out_most_comma1(self):
        to_encode = "Var \"a\""
        encoded = find_outmost_comma(to_encode)
        self.assertEqual(None, encoded)

    def test_parse_event_basic(self):
        to_encode = "Var \"a\""
        encoded = parse_event(to_encode)
        self.assertEqual(-1, encoded)

    def test_parse_event_nested(self):
        to_encode = "Next (Var \"a\")"
        encoded = encode_ops(to_encode)
        self.assertEqual([11, -1, 0], encoded)
