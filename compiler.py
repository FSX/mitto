import re
import argparse
from os import getcwd, makedirs, path
from pprint import pprint

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from mitto import compiler


if __name__ == '__main__':
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description=
        'Compile Thrift IDL files into Python Tornado code.')
    parser.add_argument('files', metavar='files', nargs='+', type=str, help='the input file(s)')
    parser.add_argument('-o', '--dir', type=str, help='the output directory',
        default=path.join(getcwd(), 'gen-tornado'))
    args = parser.parse_args()

    # Create output directory and __init__.py
    if not path.exists(args.dir):
        makedirs(args.dir)
    if not path.exists(path.join(args.dir, '__init__.py')):
        with open(path.join(args.dir, '__init__.py'), 'w'):
            pass

    # Parse Thrift files
    for file in args.files:
        input_path = path.abspath(file)
        with open(input_path, 'r') as fd:
            source = fd.read()

        # Parse source code
        parser = compiler.Parser(source)

        pprint(parser._objects)
