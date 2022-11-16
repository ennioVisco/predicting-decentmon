from os import makedirs
from time import sleep
from copy import deepcopy
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT

from decmon.extractor import flatten_once

base_cmd = ['dune', 'exec', 'decent', '--',
            '-prt_full', 'true',
            '-keep_samples', 'true',
            '-seed', '3',
            ]

options = [
    '-n', '500000',  # number of formulae to check for each formula size
    '-nb_samples', '1000',  # the number of target samples to obtain
    '-msf', '50',  # maximum size of the formulae to check
    '-st', '100',  # size of the trace against which formulae will be checked
    '-dalpha', '{a|b|c}',  # distributed alphabet to consider
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


def prepare_patterns(i: int, patterns: [[str]]) -> [str]:
    patterns = deepcopy(patterns)
    patterns[i][1] = 'true'
    return flatten_once(patterns)


def output(prefix):
    return ['-file', f'{prefix}_output.log']


def full_cmd(prefix: str, pattern: int, cmd_prefix: str = '') -> [str]:
    base_cmd[0] = cmd_prefix + base_cmd[0]
    return \
        base_cmd + options + \
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


def run_batch(prefix: str, patterns: range, cmd_prefix: str = '') -> [Popen]:
    current_time = datetime.now().strftime("%Y_%m_%d__%H_%M")
    path = f'./{prefix}/{current_time}'
    makedirs(path, exist_ok=True)
    processes = [run(full_cmd(f'{path}/{p}', p, cmd_prefix)) for p in patterns]
    return processes


def some_running(processes: [Popen]) -> bool:
    return any([p.poll() is None for p in processes])


if __name__ == '__main__':
    pts = range(len(formula_patterns))

    ps = run_batch("output", pts)

    while some_running(ps):
        print("Printing outputs...")
        for p in ps:
            print_output(p)