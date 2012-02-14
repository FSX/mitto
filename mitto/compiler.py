import re
from pprint import pprint

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


RE_COMMENT_TOKEN = re.compile('(?:/[*/]|#|["\']|\*/|\n)', re.S)

IDENTIFIER = '[a-zA-Z_][a-zA-Z0-9_.]*'
INT_CONSTANT = '[-+]?[0-9]+'

# 'enum' Identifier '{' (Identifier ('=' IntConstant)? ListSeparator?)* '}'
RE_ENUM = re.compile(r'enum\s+(%s)\s*\{\s*(.*?)\}' % IDENTIFIER, re.S)
RE_ENUM_ITEM = re.compile(r'(%s)\s*(?:=\s*(%s))?\s*' % (
    IDENTIFIER, INT_CONSTANT))


class Parser(object):

    def __init__(self, source):
        self.source = source
        self._objects = {}

        self.comment()
        self.enum()

    def _add_object(self, name, type, value):
        self._objects[name] = {
            'type': type,
            'value': value
        }

    def comment(self):
        """Remove multi-line and single-line (/* */, // and #) comments from a
        Thrift file. Comment patterns in strings are ignored.
        """
        N_MODE = 1 # Code
        C_MODE = 2 # Comment
        S_MODE = 3 # String

        position = 0
        mode = N_MODE
        prev_position = 0
        prev_token = ''
        comments = []

        while True:
            match = RE_COMMENT_TOKEN.search(self.source[position:])
            if not match:
                break

            token = match.group(0)
            position += match.start() + len(token)

            if mode == N_MODE:
                if token == '/*':
                    mode = C_MODE
                    prev_position = position
                elif token in ('//', '#'):
                    mode = C_MODE
                    prev_position = position
                    prev_token = token
                elif token in ('"', "'"):
                    mode = S_MODE
            elif mode == C_MODE:
                if token == '*/':
                    mode = N_MODE
                    comments.append(self.source[prev_position-2:position])
                elif token == '\n' and prev_token in ('//', '#'):
                    mode = N_MODE
                    prev_token = ''
                    comments.append(self.source[prev_position-2:position-1])
            elif mode == S_MODE:
                if token == prev_token:
                    mode = N_MODE

        for comment in comments:
            self.source = self.source.replace(comment, '')


    def enum(self):
        enums = RE_ENUM.findall(self.source)
        for name, items in enums:
            ln = 0 # Last item value
            value = []
            items = RE_ENUM_ITEM.findall(items)
            for n, v in items:
                if not v:
                    ln += 1
                    v = ln
                else:
                    v = int(v)
                    ln = v
                value.append((n, v))
            self._add_object(name, 'enum', value)

    def const(self):
        pass

    def list(self):
        pass

    def set(self):
        pass

    def map(self):
        pass
