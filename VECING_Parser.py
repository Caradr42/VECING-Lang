import libs.sly as sly
from libs.sly import Parser
from VECING_Lexer import LanguageLexer
from SymbolTable import SymbolTable


class LanguageParser(Parser):
    def __init__(self):
        self.symbols = SymbolTable()
        self.lambdaCounter = 0

    tokens = LanguageLexer.tokens
    start = 'program'
    debugfile = 'parser.out'

    # precedence = (
    #     ('right', 'DEFINE'),
    #     ('right', 'RENDER')
    # )

    ################ program ################
    @_('ID a render')
    def program(self, p):
        pass

    @_('defContainer a')
    def a(self, p):
        pass

    @_('empty')
    def a(self, p):
        pass

    ################ render ################
    @_('RENDER listContainer b END')
    def render(self, p):
        pass

    @_('listContainer b')
    def b(self, p):
        pass

    @_('empty')
    def b(self, p):
        pass

    ################ defContainer ################
    @_('c SEM_COL',
        'd SEM_COL')
    def defContainer(self, p):
        pass

    @_('LEFT_BRAKET e RIGHT_BRAKET')
    def c(self, p):
        pass

    @_('LEFT_PARENTHESIS e RIGHT_PARENTHESIS')
    def d(self, p):
        pass

    @_('funcDef',
        'constDef')
    def e(self, p):
        pass

    ################ defParamContainer ################
    @_('f',
        'g',
        'pushSymbol')
    def defParamContainer(self, p):
        pass

    @_('LEFT_BRAKET defParam RIGHT_BRAKET')
    def f(self, p):
        pass

    @_('LEFT_PARENTHESIS defParam RIGHT_PARENTHESIS')
    def g(self, p):
        pass

    ################ listContainer ################
    @_('h',
        'i',
        'ID',
        'const',
        'structure')
    def listContainer(self, p):
        pass

    @_('LEFT_BRAKET flist RIGHT_BRAKET')
    def h(self, p):
        pass

    @_('LEFT_PARENTHESIS flist RIGHT_PARENTHESIS')
    def i(self, p):
        pass

    ################ flist ################
    @_('j flist')
    def flist(self, p):
        pass

    @_('j')
    def flist(self, p):
        pass

    @_('listContainer', 'functionList')
    def j(self, p):
        pass

    ################ comment  ################
    @_('COMMENT')
    def comment(self, p):
        pass

    ################ constDef  ################
    @_('CONST pushSymbol const')
    def constDef(self, p):
        pass

    ################ funcDef  ################
    @_('DEFINE pushFunction defParamContainer listContainer popFunction')
    def funcDef(self, p):
        pass

    ################ defParam  ################
    @_('pushSymbol defParam')
    def defParam(self, p):
        pass

    @_('pushSymbol')
    def defParam(self, p):
        pass

    ################ constNum ################
    @_('CONST_INT',
        'CONST_FLOAT',
        'CONST_BOOL')
    def constNum(self, p):
        pass

    ################ const ################
    @_('constNum',
        'CONST_LIST',
        'NULL')
    def const(self, p):
        pass

    ################ vector ################
    @_('constNum w',
        'listContainer w',
        'ID w')
    def vector(self, p):
        pass

    @_('COMMA vector')
    def w(self, p):
        pass

    @_('empty')
    def w(self, p):
        pass

    ################ structure ################
    @_('LEFT_BRAKET x RIGHT_BRAKET')
    def structure(self, p):
        pass

    @_('structure y',
        'vector y')
    def x(self, p):
        pass

    @_('COMMA x')
    def y(self, p):
        pass

    @_('empty')
    def y(self, p):
        pass

    ################ functionList ################
    @_('LANGUAGE_FUNC z',
        'ID z',
        'OP_COMP z',
        'OP_MATH z',
        'pushLambda z')
    def functionList(self, p):
        pass

    @_('listContainer z')
    def z(self, p):
        pass

    @_('empty')
    def z(self, p):
        pass

    ################ pushActions ################
    @_('ID')
    def pushFunction(self, p):
        self.symbols.addSymbol(p[0], "func")

    @_('ID')
    def pushSymbol(self, p):
        self.symbols.addSymbol(p[0], "symbol")

    @_('')
    def popFunction(self, p):
        self.symbols.pop()

    @_('LAMBDA')
    def pushLambda(self, p):
        self.symbols.addSymbol(str(self.lambdaCounter), "lambda")
        self.lambdaCounter += 1

    ################ empty ################
    @_('')
    def empty(self, p):
        pass

    def error(self, p):
        message = 'Error in tok \'{}\' identified as {} in line {}'.format(
            p.value, p.type, p.lineno)
        print(message)
        print(p)
        raise Exception(message)
