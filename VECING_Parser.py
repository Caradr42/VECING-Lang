import libs.sly as sly
from libs.sly import Parser
from VECING_Lexer import LanguageLexer
from SymbolTable import SymbolTable
import array 
array.array
languageFunctions = [
        "add",
        "sub",
        "mult",
        "power",
        "div",
        "sqrt",
        "abs",
        "<=",
        ">=",
        "<",
        ">",
        "!=",
        "=",
        "map",
        "apply",
        "cond",
        "lambda",
        "print",
        "car",
        "cdr",
        "cons",
        "and",
        "or",
        "isEmpy",
        "screen",
        "pixel",
        "pixels",
        "getPixels",
        "background",
        "clear",
        "timeStep",
        "deltaTime",
        "line",
        "curve",
        "spline",
        "triangle",
        "ellipse",
        "isNumber",
        "isMatrix",
        "isVector",
        "isList",
        "isFunc",
        "isBool",
        "shape",
        "get"
    ]

semanticTable = {
    "add":      ((tuple, tuple), (tuple)),   #("add", ((1, None), (2, None)))
    "sub":      ((tuple, tuple), (tuple)),
    "mult":     ((tuple, tuple), (tuple)),
    "power":    ((tuple, tuple), (tuple)),
    "div":      ((tuple, tuple), (tuple)),
    "sqrt":     ((tuple), (tuple)),
    "abs":      ((tuple), (tuple)),
    "<=":       ((tuple, tuple), (bool)),
    ">=":       ((tuple, tuple), (bool)),
    "<":        ((tuple, tuple), (bool)),
    ">":        ((tuple, tuple), (bool)),
    "!=":       ((tuple, tuple), (bool)),
    "=":        ((tuple, tuple), (bool)),
    "map":      ((tuple, tuple), (tuple)),      
    "apply":    ((tuple, tuple), (tuple)),    
    "cond":     ((tuple), (None)),
    "lambda":   ((tuple, tuple), (tuple)),
    "print":    ((tuple), (None)),
    "car":      ((tuple), (tuple)),
    "cdr":      ((tuple), (tuple)),
    "cons":     ((tuple, tuple), (tuple)),
    "and":      ((tuple), (tuple)),
    "or":       ((tuple), (tuple)),
    "isEmpty":  ((tuple), (bool)),
    "screen":   ((array.array, (array.array, tuple)), (None)),
    "pixel":    ((array.array, array.array), (None)),
    "pixels":   ((array.array, array.array), (None)),
    "getPixels":((None), (None)),
    "background":((array.array), (None)),
    "clear":    ((None), (None)),    
    "timeStep": ((None), (tuple)),
    "deltaTime":((None), (tuple)),
    "line":     ((array.array, (array.array, array.array)), (None)),
    "curve":    ((array.array, (array.array, (array.array, array.array))), (None)),
    "spline":   ((tuple), (None)),
    "triangle": ((array.array, (array.array, (array.array, array.array))), (None)),
    "ellipse":  ((array.array, (array.array, array.array)), (None)),
    "isNumber": ((tuple), (bool)),
    "isMatrix": ((tuple), (bool)),
    "isVector": ((tuple), (bool)),
    "isList":   ((tuple), (bool)),
    "isFunc":   ((tuple), (bool)),
    "isBool":   ((tuple), (bool)),
    "shape":    ((array.array), (tuple)),
    "get":      ((array.array), (tuple)) 
}

class LanguageParser(Parser):

    def __init__(self):
        self.symbols = SymbolTable()
        self.lambdaCounter = 0
        self.programTree = ""
        self.tCounter = 0
    
        #add all language functions to the symbols table
        for name in languageFunctions:
            self.symbols.addSymbol(name, "func")
            self.symbols.pop()

    tokens = LanguageLexer.tokens
    start = 'program'
    debugfile = 'parser.out'

    # precedence = (
    #     ('right', 'DEFINE'),
    #     ('right', 'RENDER')
    # )

    def reduceVar(x):
        if (type(x)==bool):
            return 1 if x else 0

    ################ program ################
    @_('ID a render')
    def program(self, p):
        programTree = ("PROGRAM", (p[0], (p[1], p[2])))
        self.programTree = programTree
        return programTree

    @_('defContainer a')
    def a(self, p):
        return (p[0], p[1])

    @_('empty')
    def a(self, p):
        return None

    ################ render ################
    @_('RENDER listContainer b END')
    def render(self, p):
        return ("RENDER", (p[1], p[2]))

    @_('listContainer b')
    def b(self, p):
        return (p[0], p[1])

    @_('empty')
    def b(self, p):
        return None

    ################ defContainer ################
    @_('c SEM_COL',
        'd SEM_COL')
    def defContainer(self, p):
        return p[0]

    @_('LEFT_BRAKET e RIGHT_BRAKET')
    def c(self, p):
        return p[1]

    @_('LEFT_PARENTHESIS e RIGHT_PARENTHESIS')
    def d(self, p):
        return p[1]

    @_('funcDef',
        'constDef')
    def e(self, p):
        return p[0]

    ################ defParamContainer ################
    @_('f',
        'g')
    def defParamContainer(self, p):
        return p[0]

    @_('pushSymbol')
    def defParamContainer(self, p):
        return (p[0], None)

    @_('LEFT_BRAKET defParam RIGHT_BRAKET')
    def f(self, p):
        return p[1]

    @_('LEFT_PARENTHESIS defParam RIGHT_PARENTHESIS')
    def g(self, p):
        return p[1]

    ################ listContainer ################
    @_( 'h',
        'i',
        'const',
        'structure')
    def listContainer(self, p):
        return p[0]
    @_('ID')
    def listContainer(self, p):
        return ('var', p[0])

    @_('LEFT_BRAKET flist RIGHT_BRAKET')
    def h(self, p):
        return p[1]

    @_('LEFT_PARENTHESIS flist RIGHT_PARENTHESIS')
    def i(self, p):
        return p[1]

    ################ flist ################
    @_('j flist')
    def flist(self, p):
        return (p[0], p[1])

    @_('j')
    def flist(self, p):
        return p[0]

    @_('listContainer', 'functionList', 'functionLambda')
    def j(self, p):
        return p[0]

    # functionLambda

    ################ comment  ################
    @_('COMMENT')
    def comment(self, p):
        pass

    ################ constDef  ################
    @_('CONST pushSymbol const')
    def constDef(self, p):
        return ('CONSTDEF', (p[1], p[2]))

    ################ funcDef  ################
    @_('DEFINE pushFunction defParamContainer listContainer popFunction')
    def funcDef(self, p):
        return ('DEFINE', (p[1], (("params", p[2]), p[3]) ))

    ################ defParam  ################
    @_('pushSymbol defParam')
    def defParam(self, p):
        return (('param', p[0]), p[1])

    @_('pushSymbol')
    def defParam(self, p):
        return ('param', p[0])

    ################ constNum ################
    @_('CONST_INT',
        'CONST_FLOAT',
        'CONST_BOOL')
    def constNum(self, p):
        return p[0]

    ################ const ################
    @_('constNum',
        'CONST_LIST',
        'NULL')
    def const(self, p):
        return (p[0], None)

    ################ vector ################
    @_('constNum w',
        'listContainer w')
    def vector(self, p):
        return ('vect', (p[0], p[1]))

    @_('ID w')
    def vector(self, p):
        return (('var', p[0]), p[1]) 

    @_('COMMA vector')
    def w(self, p):
        return p[1]

    @_('empty')
    def w(self, p):
        return None

    ################ structure ################
    @_('LEFT_BRAKET x RIGHT_BRAKET')
    def structure(self, p):
        return p[1]

    @_('structure y',
        'vector y')
    def x(self, p):
        return ('struct', (p[0], p[1]))

    @_('COMMA x')
    def y(self, p):
        return p[1]

    @_('empty')
    def y(self, p):
        return None

    ################ functionList ################
    @_( 'LANGUAGE_FUNC z',
        'ID z',
        'OP_COMP z',
        'OP_MATH z')
    def functionList(self, p):
        if(not self.symbols.isSymbolInContext(p[0])):
            raise NameError('--SEMANTIC ERROR-- at line {}:\n\t{} not found in scope'.format(p.lineno, p[0]))
        return (p[0], p[1])

    @_('listContainer')
    def z(self, p):
        return p[0]

    @_('listContainer z')
    def z(self, p):
        return (p[0], p[1])

    # @_('empty')
    # def z(self, p):
    #     None

    ################ functionLambda ################
    @_('pushLambda defParamContainer lambdaContent listContainer popFunction')
    def functionLambda(self, p):
        return ('LAMBDA', (p[2], (("params", p[1]), p[3]) ))

    @_('')
    def lambdaContent(self, p):
        return str(self.lambdaCounter - 1)

    ################ pushActions ################
    @_('ID')
    def pushFunction(self, p):
        self.symbols.addSymbol(p[0], "func")
        return p[0]

    @_('ID')
    def pushSymbol(self, p):
        self.symbols.addSymbol(p[0], "symbol")
        return p[0]

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
        return None

    def error(self, p):
        message = 'Error in tok \'{}\' identified as {} in line {}'.format(
            p.value, p.type, p.lineno)
        print(message)
        print(p)
        raise Exception(message)

    def getCuads(self):
        #tCounter = 0
        cuads = []
        self.cuadGenerator(self.programTree, cuads)
        self.tCounter = 0
        return cuads

    def cuadGenerator(self, tree, cuads):
        if type(tree) == tuple:
            if tree[0] == 'PROGRAM':
                programBody = tree[1][1]
                programName = tree[1][0]
                t = self.cuadGenerator(programBody, cuads)
                cuads.append(('PROGRAM', programName, t, 'END'))
                self.tCounter += 1
                return self.tCounter

            elif tree[0] == 'DEFINE':
                functionBody = tree[1][1]
                functionName = tree[1][0]

                t = self.cuadGenerator(functionBody, cuads)
                self.tCounter += 1
                cuads.append(('DEF', functionName, t, self.tCounter))
                return self.tCounter

            elif tree[0] == 'RENDER':
                renderBody = tree[1]

                t = self.cuadGenerator(renderBody, cuads)
                self.tCounter += 1
                cuads.append(('RENDER', t, 'None', self.tCounter))
                return self.tCounter

            elif tree[0] == 'LAMBDA':
                pass
            elif tree[0] == 'params':
                paramsBody = tree[1]

                t = self.cuadGenerator(paramsBody, cuads)
                self.tCounter += 1
                cuads.append(('PARAMS', t, 'None', self.tCounter))
                return self.tCounter

            elif tree[0] == 'param':
                paramName = tree[1]

                self.tCounter += 1
                cuads.append(('PARAM', paramName, 'None', self.tCounter))
                return self.tCounter
                
            elif tree[0] == 'var':
                varName = tree[1]

                self.tCounter += 1
                cuads.append(('VAR', varName, 'None', self.tCounter))
                return self.tCounter
            
            elif self.symbols.isSymbolInContext(tree[0]):  #if the  instruction is a defined  
                funcName = tree[0]
                funcParams = tree[1]

                t = self.cuadGenerator(funcParams, cuads)
                self.tCounter += 1
                cuads.append((funcName, t, 'None', self.tCounter))
                return self.tCounter
            else:
                t1 = self.cuadGenerator(tree[0], cuads)
                t2 = self.cuadGenerator(tree[1], cuads)

                self.tCounter += 1
                cuads.append(('list', t1, t2, self.tCounter))
                return self.tCounter
        elif tree == None: #for None or a constant
            return 'None'
        else: #for None or a constant
            return tree
        

        
        




