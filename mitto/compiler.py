import re

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


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
        """Remove multi-line and single-ling (/* */ and  //) comments from a
        Thrift file. Strings are ignored.

        :param content: the source code that needs to be stripped from comments.
        """
        N_MODE = 1 # Normal mode
        C_MODE = 2 # Comment mode
        S_MODE = 3 # String mode

        buffer = StringIO()
        mode = N_MODE
        lc = '' # Last character

        for i, c in enumerate(self.source):
            if mode == C_MODE:
                # Could this be the end of a multi-line comment?
                if c == '*':
                    lc = c
                # The end of a single- or multi-line comment, enter normal mode
                elif (lc == '*' and c == '/') or (lc == '/' and c == '\n'):
                    mode = N_MODE
                    lc = ''
            elif mode == N_MODE:
                # The start of a string (" or '), enter string mode. Store the opening
                # character of the string in lc so it can be used to detect the end
                # of the string correctly.
                if c == '"' or c == "'":
                    mode = S_MODE
                    lc = c
                    buffer.write(c)
                # Could this be the start of a single- or multi-line comment?
                elif c == '/' and not lc:
                    lc = c
                # Start of a multi-line comment, enter comment mode
                elif lc and c == '*':
                    mode = C_MODE
                    lc = ''
                # Start of a single-line comment, enter comment mode. The lc is not
                # cleared, because it is used to detect the end of the comment.
                elif lc and c == '/':
                    mode = C_MODE
                # No single- or multi-line comment found so write lc and c to the buffer
                elif lc:
                    buffer.write(lc + c)
                    lc = ''
                # Nothing happened, just write to the buffer
                else:
                    buffer.write(c)
            elif mode == S_MODE:
                # End of the string, enter normal mode
                if c == lc:
                    mode = N_MODE
                    lc = ''
                buffer.write(c)

        self.source = buffer.getvalue()
        buffer.close()

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
