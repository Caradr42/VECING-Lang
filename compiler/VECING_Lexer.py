import libs.sly as sly
from libs.sly import Lexer
import re


class LanguageLexer(Lexer):
    """ This Class is in charge of the lexical analysis
        for the VECING-Lang, it is made using the Lexer class
        from sly. It contains all the possible tokens in the language
        and for some of them, a special function that modifies its value
        before returning it.

    attributes
    ----------
    lineno: counter of lines (\n) seen in the program

    constants
    ----------
    tokens: a list of all the possible tokens
    ignore: regular expression of the elements to ignore
    ignore_newline: regular expression of a new line
    SEM_COL: regular expression of the token called SEM_COL 
    COMMA: regular expression of the token called COMMA 
    LEFT_PARENTHESIS: regular expression of the token called LEFT_PARENTHESIS 
    RIGHT_PARENTHESIS: regular expression of the token called RIGHT_PARENTHESIS 
    LEFT_BRAKET: regular expression of the token called LEFT_BRAKET 
    RIGHT_BRAKET: regular expression of the token called RIGHT_BRAKET 
    OP_COMP: regular expression of the token called OP_COMP 
    OP_MATH: regular expression of the token called OP_MATH 
    DEFINE: regular expression of the token called DEFINE 
    CONST: regular expression of the token called CONST 
    LAMBDA: regular expression of the token called LAMBDA 
    RENDER: regular expression of the token called RENDER 
    END: regular expression of the token called END 
    LANGUAGE_FUNC: regular expression of the token called LANGUAGE_FUNC 
    ID: regular expression of the token called ID 

    methods
    -------
    COMMENT(t)
    CONST_FLOAT(t)
    CONST_INT(t)
    NULL(t)
    CONST_BOOL(t)
    CONST_LIST(t)
    ignore_newline(t)
    error(t)
    """

    tokens = {'COMMENT', 'SEM_COL', 'COMMA', 'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS',
              'LEFT_BRAKET', 'RIGHT_BRAKET', 'OP_COMP', 'OP_MATH', 'DEFINE', 'CONST', 'LAMBDA', 'RENDER', 'END', #'NULL',
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
    #NULL = r'null|NULL|\(\)'
    DEFINE = r'DEFINE|define|DEF|def'
    CONST = r'CONST|const'
    LAMBDA = r'lambda'
    RENDER = r'RENDER|render'
    END = r'END|end'
    LANGUAGE_FUNC = r'cond'

    #CONST_FLOAT = r'(\-)?[0-9]+\.[0-9]+'
    # do not pay attention to IDE not recognizing the decorators
    @_(r'(\-)?[0-9]+\.[0-9]+')
    def CONST_FLOAT(self, t):
        """ Function that receives as argument
            a parameter that matches the regex of the token CONST_FLOAT

        parameters
        ----------
        t: the token received

        returns
        -------
        t: token after being converted to float
        """
        t.value = float(t.value)
        return t

    #CONST_INT = r'\-?[0-9]+'
    @_(r'\-?[0-9]+')
    def CONST_INT(self, t):
        """ Function that receives as argument
            a parameter that matches the regex of the token CONST_INT

        parameters
        ----------
        t: the token received

        returns
        -------
        t: token after being converted to int
        """
        t.value = int(t.value)
        return t

    #NULL
    @_(r'null|NULL|\(\)')
    def NULL(self, t):
        """ Function that receives as argument
            a parameter that matches the regex of the token NULL

        parameters
        ----------
        t: the token received

        returns
        -------
        t: None
        """
        t.value = None
        return t

    # CONST_BOOL = r'#false|#true'
    @_(r'#false|#true')
    def CONST_BOOL(self, t):
        """ Function that receives as argument
            a parameter that matches the regex of the token CONST_BOOL

        parameters
        ----------
        t: the token received

        returns
        -------
        t: a boolean value representing the token
        """
        t.value = False if t.value == '#false' else True
        return t

    "[1 2.3 #true]"
    # CONST_LIST = r'\"\(\s*(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true)(\s+(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true))*\s*\)\"|\"\[\s*(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true)(\s+(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true))*\s*\]\"'
    @_(r'\"\(\s*(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true)(\s+(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true))*\s*\)\"|\"\[\s*(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true)(\s+(((\-)?[0-9]+\.[0-9]+)|((\-)?[0-9]+)|#false|#true))*\s*\]\"')
    def CONST_LIST(self, t):
        """ Function that receives as argument
            a parameter that matches the regex of the token CONST_LIST

        parameters
        ----------
        t: the token received

        returns
        -------
        t: token converted into a python list
        """
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
        """ Function that receives as argument
            a parameter that matches the regex of the token ignore_newline
            and increments the counter of new lines

        parameters
        ----------
        t: the token received
        """
        self.lineno += t.value.count('\n')

    def error(self, t):
        """ Function that receives as argument
            a parameter that does not match any previous token.
            It raises an exception.

        parameters
        ----------
        t: the value without a token assigned to it
        """
        print("Illegal character '%s' in line %i" % (t.value[0], self.lineno))
        raise Exception("Illegal character '%s' in line %i" %
                        (t.value[0], self.lineno))
