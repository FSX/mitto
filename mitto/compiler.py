import re

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


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


class Parser(object):

    def __init__(self, source):
        self.source = source
        self.buffer = StringIO()

        self.comment()

    def comment(self):
        """Remove multi-line and single-ling (/* */ and  //) comments from a
        Thrift file. Strings are ignored.

        :param content: the source code that needs to be stripped from comments.
        """
        N_MODE = 1 # Normal mode
        C_MODE = 2 # Comment mode
        S_MODE = 3 # String mode

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
                    self.buffer.write(c)
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
                    self.buffer.write(lc + c)
                    lc = ''
                # Nothing happened, just write to the buffer
                else:
                    self.buffer.write(c)
            elif mode == S_MODE:
                # End of the string, enter normal mode
                if c == lc:
                    mode = N_MODE
                    lc = ''
                self.buffer.write(c)

    def enum(self):
        # RE_ENUM.findall(content)
        pass

    def list(self):
        pass

    def set(self):
        pass

    def map(self):
        pass
