from os import makedirs
from time import sleep
from copy import deepcopy
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT

from decmon.constants import ALPHABET
from decmon.extractor import flatten_once


base_cmd = ['opam', 'exec', '--',
            'dune', 'exec', 'decent', '--',
            '-prt_full', 'true',
            '-keep_samples', 'true',
            '-seed', '3',
            ]

options = [
    '-n', '500000',  # number of formulae to check for each formula size
    '-nb_samples', '1000',  # the number of target samples to obtain
    '-msf', '50',  # maximum size of the formulae to check
    '-st', '100',  # size of the trace against which formulae will be checked
]

formula_patterns = [
    ['-abs', 'false'],
    ['-exis', 'false'],
    ['-bexis', 'false'],
    ['-univ', 'false'],
    ['-prec', 'false'],
    ['-resp', 'false'],
    ['-precc', 'false'],
    ['-respc', 'false'],
    ['-consc', 'false']
]


def alphabet(n: int) -> list[str]:
    letters = ALPHABET[0:n]
    return ['-dalpha', f'{{{"|".join(letters)}}}']


def prepare_patterns(i: int, patterns: [[str]]) -> [str]:
    patterns = deepcopy(patterns)
    patterns[i][1] = 'true'
    return flatten_once(patterns)


def output(prefix):
    return ['-file', f'{prefix}_output.log']


def full_cmd(prefix: str, pattern: int, components: int) -> [str]:
    return base_cmd + options + alphabet(components) + \
            prepare_patterns(pattern, formula_patterns) + \
            output(prefix)


def run(command: [str], pause_for: int = 0) -> Popen:
    print(f'Running: {" ".join(command)}')
    process = Popen(command, stdout=PIPE, stderr=STDOUT)
    sleep(pause_for)
    return process


def print_output(process: Popen):
    to_print = process.communicate()[0].decode('utf-8')
    print(to_print, end='')
    return to_print


def run_batch(prefix: str, patterns: range, components: int) -> [Popen]:
    current_time = datetime.now().strftime("%Y_%m_%d__%H_%M")
    path = f'./{prefix}/{current_time}'
    makedirs(path, exist_ok=True)
    processes = [run(full_cmd(f'{path}/{p}', p, components)) for p in patterns]
    return processes


def some_running(processes: [Popen]) -> bool:
    return any([p.poll() is None for p in processes])
