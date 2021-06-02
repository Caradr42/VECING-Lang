import libs.sly as sly
from libs.sly import Parser
from .VECING_Lexer import LanguageLexer
from .SymbolTable import SymbolTable
import consts
import array
import sys
array.array

semanticTable = consts.semanticTable

languageFunctions = list(semanticTable.keys())


class LanguageParser(Parser):
    """ This Class is in charge of the parsing and thus grammatical analisis of VECING-Lang code.
        The 

        The beggining of the class consists of functions for all the grammatical rules of this 
        language. At the end of parsing the code, a program tree is generated containing important 
        keywords for the quadruples generation while having a functional language structure.
        This class is used by the copiler.py and ParserTest.py files


    constants
    ----------
    semanticTable: The table from wich the seantic checks to language functions are 
        compared to
    languageFunctions: a list of all language functions names
    tokens: The list of recognized tokesn as imported from the Lexer
    start: the name of the starting grammar rule for the formal grammar
    
    attributes
    ---------
    symbols: the simbols table created from the class SymbolTabe. Ii is used for semantic 
        cheking
    lambdaCounter: the number of lambda functions created in the code
    programTree: the resulting tree after parsing the code
    tCounter: the current index for the temporal addresses
    lCounter: the current index for the local variables addresses
    listCounter: the current index for the list addresses
    currentFunction: the name or address of the function meant to be executing at some point 
        in the quadruples
    constsCuads: the quadruples for the CONST instruction generated during parsing 
    functionSizeCuads: the quadruples for the functionSize instruction generated at the beginnig 
        of quadruple generation 
    constValues: the actual values of the declared constants paired to their address
    address: the initial address for all variable addresses

    methods
    -------
    #the grammar rules are not listed here else this would be to long yet not useful
    #consult the docs
    constCuadGenerator(value) 
    constArrayCuadGenerator(constList)
    flatListToFunctionalList(flatList)
    error(p)
    getCuads()
    addressSetterGenerator(initialLimit, offset=1)
    cuadGenerator(tree, cuads)
    """

    def __init__(self):
        self.symbols = SymbolTable()
        self.lambdaCounter = 0
        self.programTree = ""
        self.tCounter = 0
        self.lCounter = 0
        self.listCounter = 0

        self.currentFunction = ""

        # constants definfition variables
        self.constsCuads = []
        self.functionSizeCuads = []
        self.constValues = {}
        self.address = consts.LIMITS['GLOBAL_LIM_L']

        # add all language functions to the symbols table
        for name in languageFunctions:
            self.symbols.addSymbol(name, "func")
            self.symbols.pop()

        self.tempAddress = self.addressSetterGenerator(
            consts.LIMITS['TEMPORAL_LIM_L'], offset=1)
        self.localAddress = self.addressSetterGenerator(
            consts.LIMITS['LOCAL_LIM_L'], offset=1)
        # listCounter increments by two each time
        self.listAddress = self.addressSetterGenerator(
            consts.LIMITS['LIST_LIM_L'], offset=2)

    tokens = LanguageLexer.tokens
    start = 'program'

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
    @_('h',
        'i',
        'const',
        'structure')
    def listContainer(self, p):
        return p[0]

    @_('ID')
    def listContainer(self, p):
        symbol = self.symbols.getFunctionSymbol(p[0])
        if symbol is not None:
            return (p[0], None)
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
    @_('CONST pushFunction const popFunction')
    def constDef(self, p):
        return ('CONSTDEF', (p[1], p[2]))

    ################ funcDef  ################
    @_('DEFINE pushFunction defParamContainer listContainer popFunction')
    def funcDef(self, p):
        return ('DEFINE', (p[1], (("params", p[2]), p[3])))

    ################ defParam  ################
    @_('pushSymbol defParam')
    def defParam(self, p):
        return (('param', p[0]), p[1])

    @_('pushSymbol')
    def defParam(self, p):
        return ('param', p[0])

    def constCuadGenerator(self, value):
        """ Generates all the quads needed for a constant
            which can be a boolean value, numeric value, or
            a structured value like a list.

        parameters
        ----------
        value: the python value from which create quads

        returns
        -------
        the address counter that is increaed with every constant declared
        """
        if type(value) == list or type(value) == tuple:
            pythonList = self.constArrayCuadGenerator(value)
            return pythonList
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

                self.constsCuads.append(
                    ('CONST', "{:.9f}".format(value), "None", self.address))

        self.address += 1
        return self.address - 1

    def constArrayCuadGenerator(self, constList):
        newConstList = []
        for const in constList:
            newConstList.append(self.constCuadGenerator(const))

        functionalList = self.flatListToFunctionalList(newConstList)
        #print(functionalList)
        return functionalList
    
    def flatListToFunctionalList(self, flatList):
        if flatList == None or len(flatList) == 0:
            return flatList
        if len(flatList) == 1:
            return (flatList[0], None)
            
        flatList.reverse()
        funcList = ((flatList[0], None), None)
        
        for e in flatList[1:]:
            funcList = ((e, None), funcList)
        return funcList

    ################ constNum ################

    @_('CONST_INT',
        'CONST_FLOAT',
        'CONST_BOOL')
    def constNum(self, p):
        return p[0]

    ################ const ################
    @_('constNum',
        'CONST_LIST')
        #'NULL')
    def const(self, p):
        return (self.constCuadGenerator(p[0]), None)
    
    @_('structure')
    def const(self, p):
        print(p[0])
        return (p[0], None)

    ################ vector ################
    @_('constNum w')
    def vector(self, p):
        return ((self.constCuadGenerator(p[0]), None), p[1])

    @_('ID w')
    def vector(self, p):
        return (p[0], p[1])

    @_('COMMA vector')
    def w(self, p):
        return p[1]

    @_('empty')
    def w(self, p):
        return None

    ################ structure ################ [[],[]]
    @_('LEFT_BRAKET x RIGHT_BRAKET', 'LEFT_BRAKET zz RIGHT_BRAKET')
    def structure(self, p):
        return p[1]

    @_('structure y')
    def x(self, p):
        return (p[0], p[1])

    @_('structure')
    def x(self, p):
        return (p[0], None)

    @_('vector')
    def zz(self, p):
        return p[0]

    @_('COMMA x')
    def y(self, p):
        return p[1]

    ################ functionList ################
    @_('LANGUAGE_FUNC z',
        'ID z',
        'OP_COMP z',
        'OP_MATH z')
    def functionList(self, p):
        if(not self.symbols.isSymbolInContext(p[0])):
            raise NameError(
                '--SEMANTIC ERROR-- at line {}:\n\t{} not found in scope'.format(p.lineno, p[0]))
        return (p[0], p[1])

    @_('listContainer z')
    def z(self, p):
        return (p[0], p[1])

    @_('listContainer')
    def z(self, p):
        return (p[0], None)

    # @_('empty')
    # def z(self, p):
    #     None

    ################ functionLambda ################
    @_('pushLambda defParamContainer lambdaContent listContainer popFunction')
    def functionLambda(self, p):
        return ('LAMBDA', (p[2], (("params", p[1]), p[3])))

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
        """ At the beginning it identifies the first element of the tree head, 
            which is the keyword PROGRAM and generates some quadruples (quads) used 
            for constant definition and the main goto that goes to render. Since the 
            starting goto does not know yet to which line it must jump, the generate quads 
            function must first make several recursive calls to process all the program 
            tree elements, and only after it generates the needed quads it calculates 
            the line to where the main goto must jump. This same principle is applied for 
            other instructions that require jumps in code, including function definition. 
            In an abstract way, the programm tree works as a proto quadruples list as it 
            includes instructions in the left side, and a right side with the data it 
            operates on to. Other more keywords in the program are DEFINE, CONSTDEF, 
            RENDER, LAMBDA, params, var, and cond; all of them are identified by the 
            recursive function, this way each call knows what to do with its given piece of 
            the program tree, and how to execute following recursive calls and what to do 
            before and after them.
            Used by compile.py and ParserTest.py

        returns
        -------
        cuads: all the cuads generated after executing the recursive process of cuadGenerator
                with the programTree.
        """
        #tCounter = 0
        cuads = []
        self.cuadGenerator(self.programTree, cuads)
        self.tCounter = 0
        return cuads

    def addressSetterGenerator(self, initialLimit, offset=1):
        def addressFunction(index):
            if index == None or index == 'None':
                return index

            index += initialLimit - offset
            return index
        return addressFunction

    # def flatten(head):
    #     elements = []
    #     while(head != None):
    #         elements.append(head[0])
    #         head = head[1]
    #     return elements

    def cuadGenerator(self, tree, cuads):
        global semanticTable

        if type(tree) == tuple:
            if tree[0] == 'PROGRAM':
                cuads += self.constsCuads

                # Putting empty quads to replace later with function information
                functionsCuadsIndex = len(cuads)
                functionsCount = len(list(self.symbols.dict.keys())) - \
                    len(list(semanticTable.keys()))

                emptyQuads = map(lambda _: (), list(range(functionsCount)))
                cuads += emptyQuads

                # initial goto
                cuads.append(['goto', None, None, None])
                mainGotoPos = len(cuads) - 1

                programBody = tree[1][1]
                programName = tree[1][0]

                definitions = []
                head = programBody[0]

                while(head != None):
                    definitions.append(head[0])
                    head = head[1]

                for define in definitions:
                    self.cuadGenerator(define, cuads)

                #######
                renderPosition = len(cuads)
                cuads[mainGotoPos][1] = renderPosition + 1
                cuads[mainGotoPos] = tuple(cuads[mainGotoPos])
                #######
                self.cuadGenerator(programBody[1], cuads)

                for i in range(functionsCuadsIndex, functionsCuadsIndex + functionsCount):
                    cuads[i] = self.functionSizeCuads[i - functionsCuadsIndex]

                # cuads = cuads[0:functionsCuadsIndex - 1] + self.functionSizeCuads + \
                #     cuads[functionsCuadsIndex + functionsCount - 1:]

                self.tCounter += 1
                cuads.append(('PROGRAM', programName, 'None', 'END'))

                return self.tempAddress(self.tCounter)

            elif tree[0] == 'DEFINE' or tree[0] == 'CONSTDEF':
                self.tCounter = 0
                self.lCounter = 0
                self.listCounter = 0
                paramsList = []

                functionBody = tree[1][1]
                functionName = tree[1][0]

                symbol = self.symbols.getFunctionSymbol(functionName)

                if(symbol != None):
                    #paramCount = len(paramsList)
                    symbol["funcExtras"] = {
                        "params": paramsList, "instructionPointer": len(cuads) + 1}
                else:
                    pass  # TODO: check this

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

                if t == None:
                    t = self.tempAddress(self.tCounter)
                    cuads.append(('assign', 'None', 'None', t))
                    self.tCounter += 1

                cuads.append(('endfunc', t, 'None', "None"))

                paramCount = len(paramsList)
                symbol["funcExtras"]['size'] = self.tCounter + self.listCounter + paramCount

                self.functionSizeCuads.append(
                    ('funcSize', symbol["funcExtras"]["instructionPointer"], paramCount, "None"))
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
                self.listCounter = 0
                renderBody = tree[1]

                calls = []
                head = renderBody

                while(head != None):
                    calls.append(head[0])
                    head = head[1]

                for call in calls:
                    # if problems just remove "[0]"
                    self.cuadGenerator(call[0], cuads)
                return None

            elif tree[0] == 'LAMBDA':
                pass
            elif tree[0] == 'params':
                pass

            elif tree[0] == 'var':
                varName = tree[1]

                self.lCounter += 1

                #cuads.append(('VAR', varName, 'None', self.localAddress(self.lCounter)))

                # buscar posicion de la variable en la lista de parametros de la funcion
                # generar una direccionde memoria y devolverla

                symbol = self.symbols.getFunctionSymbol(self.currentFunction)

                paramsList = symbol["funcExtras"]["params"]

                if varName not in paramsList:
                    raise Exception('--SEMANTIC ERROR--:\n\t{} not found in scope'.format(varName))


                position = paramsList.index(varName) + 1

                return self.localAddress(position)

            elif tree[0] == 'cond':
                conditionals = []
                head = tree[1][0]
                CONDRESULT = 'CONDRESULT'

                while(head != None):
                    conditionals.append((head[0][0], head[1][0][0]))
                    head = head[1][1]

                # print('------------------COND------------------\n')
                # print(conditionals)

                startCond = len(cuads)
                endOfCond = startCond + 1

                endsOfExpr = []

                # Returns last return address where something was stored
                def getLastStoredAddress():
                    #cuadsIndex = len(cuads) - 1
                    for i in range(len(cuads) - 1, -1, -1):
                        returnValue = cuads[i][3]
                        isAddress = type(returnValue) == int
                        if isAddress:
                            return returnValue
                    return None

                for (expr, body) in conditionals:
                    endOfExpr = endOfCond

                    conditionLine = self.cuadGenerator(expr, cuads)
                    cuads.append(["gotoFalse", conditionLine, None, None])
                    t = self.cuadGenerator(body, cuads)
                    
                    cuads.append(["assign", getLastStoredAddress(), "None", CONDRESULT])
                    
                    endOfCond = len(cuads) + 1
                    endOfExpr = endOfCond + 1
                    endsOfExpr.append(endOfExpr)

                    cuads.append(["goto", None, "None", None])
                    endOfCond = len(cuads) + 1
                
                # endsOfExpr[-1] += 1
                
                self.tCounter += 1
                condReturnAddress = self.tempAddress(self.tCounter)

                cuads.append(["assign", None, "None", condReturnAddress])
                endOfCond = len(cuads) + 1

                endsCounter = 0
                for i in range(startCond, endOfCond - 1):
                    if cuads[i][0] == "goto":
                        cuads[i][1] = endOfCond
                        cuads[i] = tuple(cuads[i])
                    if cuads[i][0] == "gotoFalse":
                        cuads[i][2] = endsOfExpr[endsCounter]
                        cuads[i] = tuple(cuads[i])
                        endsCounter += 1
                    elif cuads[i][0] == "assign":
                        if cuads[i][3] == CONDRESULT:
                            cuads[i][3] = condReturnAddress
                        cuads[i] = tuple(cuads[i])
                
                #isTemporal = (condReturnAddress >= consts.LIMITS["TEMPORAL_LIM_L"] and condReturnAddress <= consts.LIMITS["TEMPORAL_LIM_R"] )
                # if(not isTemporal):
                    
                #     cuads.append(["assign", condReturnAddress, "None", self.tempAddress(self.tCounter)])
                    
                #     return self.tempAddress(self.tCounter)
                # else:
                return condReturnAddress

            # if the  instruction is a defined
            elif self.symbols.isSymbolInContext(tree[0]):
                funcName = tree[0]
                funcParams = tree[1]

                #self.currentFunction = funcName
                cuads.append(("era", funcName, 'None', 'None'))

                # try:
                def paramCount(head):
                    if head == None:
                        return 0
                    return paramCount(head[1]) + 1

                paramsSize = paramCount(funcParams)
                symbol = self.symbols.getFunctionSymbol(funcName)

                # TODO: Put funcExtras to language functions
                if symbol["funcExtras"] != None:
                    functionParamCount = len(symbol["funcExtras"]["params"])
                    # TODO:  CHANGE IF USING LAMBDAS
                    if paramsSize != functionParamCount:
                        raise Exception("--SEMANTIC ERROR--:\n\tInvalid param count of {} for function {}, this function only accepts {} parameters".format(
                            paramsSize, funcName, functionParamCount))

                t = self.cuadGenerator(funcParams, cuads)

                cuads.append(("params", t, 'None', 'param1'))
                # except:
                #     e = sys.exc_info()[2]
                    
                #     print(cuads)
                #     raise Exception("error in params of function call")

                self.tCounter += 1

                funcReference = funcName if funcName in languageFunctions else symbol[
                    "funcExtras"]["instructionPointer"]
                cuads.append(("gosub", funcReference, "None",
                              self.tempAddress(self.tCounter)))

                # self.tCounter += 1
                # cuads.append((funcName, t, 'None', self.tCounter))
                return self.tempAddress(self.tCounter)
            else:
                t1 = self.cuadGenerator(tree[0], cuads)
                t2 = self.cuadGenerator(tree[1], cuads)

                self.listCounter += 2

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

                cuads.append(('list', t1Value, t2Value,
                              self.listAddress(self.listCounter)))

                return self.listAddress(self.listCounter)
        elif tree == None or tree == 'None':  # for None
            return 'None'
        elif type(tree) == int or type(tree) == float or type(tree) == bool:  # for a constant
            return ('const', tree)
        else:  # for god knows what
            return tree
