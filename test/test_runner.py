import unittest

from decmon.runner import prepare_patterns, full_cmd, output, run, print_output, \
    alphabet


class TestRunner(unittest.TestCase):
    sample_patterns = [
        ['-first', 'false'],
    ]

    def test_prepares_alphabet_correctly(self):
        result = alphabet(3)
        self.assertEqual('-dalpha', result[0])
        self.assertEqual('{a|b|c}', result[1])

    def test_can_prepare_patterns(self):
        result = prepare_patterns(0, self.sample_patterns)
        self.assertEqual(2, len(result))
        self.assertEqual('-first', result[0])
        self.assertEqual('true', result[1])
        self.assertEqual('false', self.sample_patterns[0][1])

    def test_can_prepare_output(self):
        result = output("irrelevant")
        self.assertEqual(2, len(result))
        self.assertEqual('-file', result[0])
        self.assertEqual('irrelevant_output.log', result[1])

    def test_final_command_to_run_is_complete(self):
        command = full_cmd("irrelevant", 0, 3)
        self.assertEqual('opam',    command[0])
        self.assertEqual('dune',    command[3])
        self.assertEqual('-n',      command[13])
        self.assertEqual('-abs',    command[23])
        self.assertEqual('-consc',  command[39])
        self.assertEqual('-file',   command[41])

    def test_can_run_commands(self):
        p = run(['echo', 'hello'])
        self.assertEqual(b'hello\n', p.communicate()[0])
        self.assertEqual(0, p.returncode)

    def test_can_run_in_parallel(self):
        cmd = ['sleep', '1000']
        p1 = run(cmd)
        p2 = run(cmd)
        self.assertEqual(None, p1.poll())
        self.assertEqual(None, p2.poll())
        p1.kill()
        p2.kill()
        p1.communicate()
        p2.communicate()

    def test_print_output_correctly(self):
        p = run(['echo', 'hello'])
        result = print_output(p)
        self.assertEqual('hello\n', result)
