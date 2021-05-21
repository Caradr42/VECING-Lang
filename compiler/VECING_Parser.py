import libs.sly as sly
from libs.sly import Parser
from .VECING_Lexer import LanguageLexer
from .SymbolTable import SymbolTable
import consts
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
        self.lCounter = 0
        self.currentFunction = ""
        
        #constants definfition variables
        self.constsCuads = []
        self.constValues = {}
        self.address = consts.LIMITS['GLOBAL_LIM_L']
    
        #add all language functions to the symbols table
        for name in languageFunctions:
            self.symbols.addSymbol(name, "func")
            self.symbols.pop()
        
        self.tempAddress = self.addressSetterGenerator(consts.LIMITS['TEMPORAL_LIM_L'])
        self.localAddress = self.addressSetterGenerator(consts.LIMITS['LOCAL_LIM_L'])


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
        return (p[0], None)

    @_('listContainer', 'functionList', 'functionLambda')
    def j(self, p):
        return p[0]

    # functionLambda

    ################ comment  ################
    @_('COMMENT')
    def comment(self, p):
        pass

    ################ constDef  ################
    @_('CONST pushFunction const')
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
    
    def constCuadGenerator(self, value):
        if type(value) == list or type(value) == tuple:
            initialListAddress = self.constArrayCuadGenerator(value)
            return initialListAddress
        else:
            if value in self.constValues.keys():
                address = self.constValues[value]
                return address
            else:
                
                if value == None:
                    value = 0.0
                elif type(value) == bool:
                    value = 1.0 if value else 0.0
                elif type(value) == int:
                    value = float(value)
                
                if(self.address > consts.LIMITS['GLOBAL_LIM_R']):
                    raise Exception("MemoryError")
                    
                self.constValues[value] = self.address
                
                self.constsCuads.append(('CONST', "{:.9f}".format(value), "None" , self.address))
                
        self.address += 1
        return self.address - 1


    def constArrayCuadGenerator(self, constList):
        initialAddress = self.address
        size = len(constList)
        if(size == 0):
            self.address += 1
            self.constsCuads.append(('CONST', "{:.9f}".format(0.0), "None" , self.address - 1))
            return self.address - 1

        self.constsCuads.append(('VECT', size, "None" , self.address))
        
        for e in constList:
            self.constCuadGenerator(e)
        return initialAddress


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
        return (self.constCuadGenerator(p[0]), None)

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


    def addressSetterGenerator(self, initialLimit):
        def addressFunction(index):
            if index == None or index == 'None':
                return index
                
            index += initialLimit - 1
            return index
        return addressFunction

    def flatten(head):
        elements = []
        while(head != None):
            elements.append( head[0] )
            head = head[1]
        return elements

    def cuadGenerator(self, tree, cuads):
        if type(tree) == tuple:
            if tree[0] == 'PROGRAM':
                cuads += self.constsCuads

                #initial goto
                cuads.append(['goto', None, None, None])
                mainGotoPos = len(cuads) - 1

                programBody = tree[1][1]
                programName = tree[1][0]

                definitions = []
                head = programBody[0]

                while(head != None):
                    definitions.append( head[0] )
                    head = head[1]

                for define in definitions:
                    self.cuadGenerator(define, cuads)
                
                #######
                renderPosition = len(cuads)
                cuads[mainGotoPos][1] = renderPosition + 1
                cuads[mainGotoPos] = tuple(cuads[mainGotoPos])
                #######
                self.cuadGenerator(programBody[1], cuads)

                self.tCounter += 1
                cuads.append(('PROGRAM', programName, 'None', 'END'))

                return self.tempAddress(self.tCounter)

            elif tree[0] == 'DEFINE' or tree[0] == 'CONSTDEF':
                self.tCounter = 0
                self.lCounter = 0
                paramsList = []
                
                functionBody = tree[1][1]
                functionName = tree[1][0]

                symbol = self.symbols.getFunctionSymbol(functionName)

                if(symbol != None):
                    paramCount = len(paramsList)
                    symbol["funcExtras"] = { "params": paramsList }

                self.currentFunction = functionName
                
                t = None
                if(type(functionBody) == tuple and type(functionBody[0]) == tuple and functionBody[0][0] == "params"):
                    functionsParams = functionBody[0][1]
                    
                    def treeTraverse(head):
                        if head[0] == "param":
                            paramsList.append(head[1])
                            return
                        
                        treeTraverse(head[0])
                        treeTraverse(head[1])
                        
                    treeTraverse(functionsParams)

                    t = self.cuadGenerator(functionBody[1][0], cuads)
                else:
                    t = self.cuadGenerator(functionBody, cuads)
                cuads.append(('endfunc', t, 'None', "None"))

               
                paramCount = len(paramsList)
                symbol["funcExtras"]['size'] = self.tCounter + paramCount

                return None

            # elif tree[0] == 'CONSTDEF':
            #     self.tCounter = 0
            #     functionBody = tree[1][1]
            #     functionName = tree[1][0]

            #     t = self.cuadGenerator(functionBody, cuads)

            #     cuads.append(('endfunc', self.tempAddress(t), 'None', "None"))
            #     return None

            elif tree[0] == 'RENDER':
                self.tCounter = 0
                self.lCounter = 0
                renderBody = tree[1]

                calls = []
                head = renderBody

                while(head != None):
                    calls.append( head[0] )
                    head = head[1]

                for call in calls:
                    self.cuadGenerator(call[0], cuads) #if problems just remove "[0]"
                return None

            elif tree[0] == 'LAMBDA':
                pass
            elif tree[0] == 'params':
                pass
                
            elif tree[0] == 'var':
                varName = tree[1]

                self.lCounter += 1

                #cuads.append(('VAR', varName, 'None', self.localAddress(self.lCounter)))

                #buscar posicion de la variable en la lista de parametros de la funcion
                #generar una direccionde memoria y devolverla
                
                
                symbol = self.symbols.getFunctionSymbol(self.currentFunction)
                
                paramsList = symbol["funcExtras"]["params"]

                position = paramsList.index(varName) + 1 #TODO: Check if symbols is not defines as param

                return self.localAddress(position)
            
            elif tree[0] == 'cond':
                conditionals = []
                head = tree[1]

                while(head != None):
                    conditionals.append( (head[0][0], head[1][0][0]) )
                    head = head[1][1]

                #print('------------------COND------------------\n')
                #print(conditionals)

                startCond = len(cuads)
                endOfCond = startCond + 1

                endsOfExpr = []
                
                for (expr , body) in conditionals:
                    endOfExpr = endOfCond 


                    conditionLine =  self.cuadGenerator(expr, cuads) 
                    cuads.append(["gotoFalse", conditionLine, None, None])
                    self.cuadGenerator(body, cuads) 

                    endOfCond = len(cuads) + 1
                    endOfExpr = endOfCond + 1
                    endsOfExpr.append(endOfExpr)

                    cuads.append(["goto", None, "None", None])
                    endOfCond = len(cuads) + 1

                endsCounter = 0
                for i in range(startCond, endOfCond - 1):
                    if cuads[i][0] == "goto":
                        cuads[i][1] = endOfCond
                        cuads[i] = tuple(cuads[i])
                    elif cuads[i][0] == "gotoFalse":
                        cuads[i][2] = endsOfExpr[endsCounter]
                        cuads[i] = tuple(cuads[i])
                        endsCounter += 1
                            
            elif self.symbols.isSymbolInContext(tree[0]):  #if the  instruction is a defined  
                funcName = tree[0]
                funcParams = tree[1]

                cuads.append(("era", funcName, 'None', 'None'))

                def treeTraverse(head):
                    if type(head[0]) != tuple:
                        return 1
                    return treeTraverse(head[0]) + treeTraverse(head[1])
                    
                        
                paramsSize = treeTraverse(funcParams)
                symbol = self.symbols.getFunctionSymbol(funcName)
                
                # TODO: Put funcExtras to language functions
                if symbol["funcExtras"] != None:
                    functionParamCount = len(symbol["funcExtras"]["params"])
                    #TODO:  CHANGE IF USING LAMBDAS
                    if paramsSize != functionParamCount:
                        raise Exception("Invalid param count of {} for function {}, this function only accepts {} parameters".format(paramsSize, funcName, functionParamCount))
                
                t = self.cuadGenerator(funcParams, cuads)

                cuads.append(("params", t, 'None', 'param1'))

                self.tCounter += 1
                cuads.append(("gosub", funcName, "None", self.tempAddress(self.tCounter)))

                # self.tCounter += 1
                # cuads.append((funcName, t, 'None', self.tCounter))
                return self.tempAddress(self.tCounter)
            else:
                t1 = self.cuadGenerator(tree[0], cuads)
                t2 = self.cuadGenerator(tree[1], cuads)

                self.tCounter += 1

                t1Value = None
                t2Value = None
                if(type(t1) == tuple and t1[0] == 'const'):
                    t1Value = t1[1]
                else:
                    t1Value = t1

                if(type(t2) == tuple and t1[0] == 'const'):
                    t1Value = t2[1]
                else:
                    t2Value = t2
                
                cuads.append(('list', t1Value, t2Value, self.tempAddress(self.tCounter)))

                return self.tempAddress(self.tCounter)
        elif tree == None or tree == 'None': #for None
            return 'None'
        elif type(tree) == int or type(tree) == float or type(tree) == bool: #for a constant
            return ('const', tree)
        else: #for god knows what
            return tree
        

        
        




