import libs.sly as sly
from libs.sly import Lexer
import re


class LanguageLexer(Lexer):
    tokens = {'COMMENT', 'SEM_COL', 'COMMA', 'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS',
              'LEFT_BRAKET', 'RIGHT_BRAKET', 'OP_COMP', 'OP_MATH', 'NULL', 'DEFINE', 'RENDER', 'END',
              'LANGUAGE_FUNC', 'ID', 'CONST_INT', 'CONST_FLOAT', 'CONST_BOOL', 'CONST_LIST'}
    # characters to ignore
    ignore = ' \t'
    ignore_newline = r'\n+'

    # Tokens Regexes
    #COMMENT = r'\/\/.*;'
    @_(r'\/\/.*;')
    def COMMENT(self, t):
        pass

    SEM_COL = r'\;'
    COMMA = r'\,'
    LEFT_PARENTHESIS = r'\('
    RIGHT_PARENTHESIS = r'\)'
    LEFT_BRAKET = r'\['
    RIGHT_BRAKET = r'\]'
    OP_COMP = r'\<\=|\>\=|\<|\>|\!\=|\='
    OP_MATH = r'add|sub|mult|power|div|sqrt|abs'
    NULL = r'null|\(\)'
    DEFINE = r'define|def'
    RENDER = r'RENDER|render'
    END = r'END|end'
    LANGUAGE_FUNC = r'cond|else|map|apply'

    #CONST_FLOAT = r'(\-)?[0-9]+\.[0-9]+'
    # do not pay attention to IDE not recognizing the decorators
    @_(r'(\-)?[0-9]+\.[0-9]+')
    def CONST_FLOAT(self, t):
        t.value = float(t.value)
        return t

    #CONST_INT = r'\-?[0-9]+'
    @_(r'\-?[0-9]+')
    def CONST_INT(self, t):
        t.value = int(t.value)
        return t

    # CONST_BOOL = r'#false|#true'
    @_(r'#false|#true')
    def CTE_BOOL(self, t):
        t.value = False if t.value == '#false' else True
        return t

    "[1 2.3 #true]"
    # CONST_LIST = r'\"\(\s*(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true)(\s+(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true))*\s*\)\"|\"\[\s*(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true)(\s+(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true))*\s*\]\"'
    @_(r'\"\(\s*(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true)(\s+(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true))*\s*\)\"|\"\[\s*(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true)(\s+(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true))*\s*\]\"')
    def CONST_LIST(self, t):
        temp = list(re.split(r'\s+', t.value[2:-2]))
        li = []

        for elem in temp:
            if re.search(r'(\-)?[0-9]+\.[0-9]+', elem):
                li.append(float(elem))
            elif re.search(r'\-?[0-9]+', elem):
                li.append(int(elem))
            elif re.search(r'#false|#true', elem):
                boolean = False if elem == '#false' else True
                li.append(boolean)
        t.value = li
        return t

    ID = r'[a-zA-Z]\w*'

    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s' in line %i" % (t.value[0], self.lineno))
        raise Exception("Illegal character '%s' in line %i" %
                        (t.value[0], self.lineno))
