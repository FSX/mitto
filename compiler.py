import re
import argparse
from os import getcwd, makedirs, path
from pprint import pprint

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


RE_COMMENT = re.compile(r'/\*.*?\*/')

RE_ENUM = re.compile(r'''
enum\s+
([a-z_][a-z0-9_]+)\s*
\{\s*
    ((?:
        [a-z][a-z0-9]+\s*
        (?:=\s*[0-9]+)?\s*
    )*)
\}
''', re.X | re.I | re.S)


def remove_comments(content):
    N_MODE = (1 << 0)
    C_MODE = (1 << 1)
    S_MODE = (1 << 2)

    buffer = StringIO()
    mode = N_MODE
    lc = ''

    for i, c in enumerate(content):
        if mode & C_MODE:
            if c == '*':
                lc = c
            elif lc and c == '/':
                mode = N_MODE
                lc = ''
        elif mode & N_MODE:
            if c == '"' or c == "'":
                mode = S_MODE
                lc = c
                buffer.write(c)
            elif c == '/' and not lc:
                lc = c
            elif lc and c == '*':
                mode = C_MODE
                lc = ''
            elif lc:
                buffer.write(lc + c)
                lc = ''
            else:
                buffer.write(c)
        elif mode & S_MODE:
            if c == lc:
                mode = N_MODE
                lc = ''
            buffer.write(c)

    try:
        return buffer.getvalue()
    finally:
        buffer.close()


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
            content = fd.read()

        # Strip multiline comments
        # TODO: Do this char by char so we can check if we're in a string or not
        #       this also makes it possible to remove // comments
        # content = ''.join(RE_COMMENT.split(content))
        content = remove_comments(content)

        print content

        # Read enums
        # enums = RE_ENUM.findall(content)

        # pprint(enums)

        # print content

    # Open input file
