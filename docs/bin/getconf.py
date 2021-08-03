"""
Dump the output of a file in reqres/conf to stdout.
"""

import pathlib
import sys

import hjson


def get_file(path):
    return pathlib.Path(path).read_text()


    fp = pathlib.Path("../../reqres/conf") / conf_name
    print(fp.read_text())

if __name__ == "__main__":

    print(getconf(sys.argv[0]))
