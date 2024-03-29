from decmon.runner import *
from decmon.constants import *

from os import chdir

COMPONENTS = 5  # CHANGE THIS TO RUN WITH MORE COMPONENTS

pts = range(len(formula_patterns))

chdir('decent')
try:
    ps = run_batch(f'../{OUTPUT_DIR}', pts, COMPONENTS)

    while some_running(ps):
        print("Printing outputs...")
        for p in ps:
            print_output(p)
finally:
    chdir('..')
