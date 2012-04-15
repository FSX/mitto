import re
from pprint import pprint

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


def doc_string_comment(lexer, token):
    lines = token[3:-2].strip().splitlines()
    token = '\n'.join([re.sub(r'^\s*\*\s*', '', line) for line in lines])
    return token


def c_comment(lexer, token):
    return token[2:-2].strip()


def cpp_comment(lexer, token):
    return token[2:].strip()


def unix_comment(lexer, token):
    return token[1:].strip()


def string(lexer, token):
    return token[1:-1].strip()


_RULES = (
    ('WORD',                 r'[a-zA-Z_][a-zA-Z0-9_.-]*'),

    ('INT_CONSTANT',         r'(?:\+|-)?[0-9]+'),
    ('DOUBLE_CONSTANT',      r'(?:\+|-)?[0-9.]+(?:[Ee][0-9]+)?'),

    ('DOC_STRING_COMMENT',  (r'/\*\*(?:.|\n)*?\*/', doc_string_comment)),
    ('C_COMMENT',           (r'/\*(?:.|\n)*?\*/', c_comment)),
    ('CPP_COMMENT',         (r'//.*\n', cpp_comment)),
    ('UNIX_COMMENT',        (r'#.*\n', unix_comment)),

    ('LIST_SEPARATOR',       r'(?:,|;)'),
    ('COLON',                r':'),

    ('STRING_DQ',           (r'".*?"', string)),
    ('STRING_SQ',           (r"'.*?'", string)),

    ('CURLY_BRACKET_OPEN',   r'\{'),
    ('CURLY_BRACKET_CLOSE',  r'\}'),
    ('POINTY_BRACKET_OPEN',  r'<'),
    ('POINTY_BRACKET_CLOSE', r'>'),
    ('ROUND_BRACKET_OPEN',   r'\('),
    ('ROUND_BRACKET_CLOSE',  r'\)'),
    ('SQUARE_BRACKET_OPEN',  r'\['),
    ('SQUARE_BRACKET_CLOSE', r'\]'),
    ('STAR',                 r'\*'),
    ('ASSIGNMENT',           r'='),

    # The parser should ignore the whitespace, it's not important
    ('WHITESPACE',           r'\s+'),
)


class Token(object):
    def __init__(self, type, value, line_nr):
        self.type = type
        self.value = value
        self.line_nr = line_nr

    def __str__(self):
        return "Token(%s, %r, %d)" % (self.type,
            self.value, self.line_nr)

    def __repr__(self):
        return str(self)


class UnknownTokenError(Exception):
    def __init__(self, token, line_nr):
        self.token = token
        self.line_nr = line_nr

    def __str__(self):
        return "Line #%s, Found token: %s" % (self.line_nr, self.token)


class Lexer(object):
    def __init__(self, rules, source):
        self._source = source.strip()
        self._callbacks = {}
        self._position = 0
        self._line_nr = 1

        parts = []
        for name, rule in rules:
            if not isinstance(rule, str):
                rule, callback = rule
                self._callbacks[name] = callback
            parts.append('(?P<%s>%s)' % (name, rule))

        self.regex = re.compile('|'.join(parts))

    def scan(self):
        token = self._scan_next()
        while token is not None:
            yield token
            token = self._scan_next()

    def _scan_next(self):
        if self._position >= len(self._source):
            return None

        match = self.regex.match(self._source, self._position)
        if match is None:
            raise UnknownTokenError(self._source[self._position], self._line_nr)

        value = match.group(match.lastgroup)
        add_line_count = value.count('\n')
        if match.lastgroup in self._callbacks:
            value = self._callbacks[match.lastgroup](self, value)

        token = Token(match.lastgroup, value, self._line_nr)
        self._line_nr += add_line_count
        self._position = match.end()

        return token


class Parser(object):
    def __init__(self, tokens):
        pass


class Generator(object):
    def __init__(self, tree):
        pass


class Compiler(object):
    def __init__(self, source):
        lexer = Lexer(_RULES, source)

        for v in lexer.scan():
            print v
