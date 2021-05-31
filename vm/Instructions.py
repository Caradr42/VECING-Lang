from MemoryManager import MemoryManager
import languageFunctions
import consts
from utils import Debugger

debug = Debugger(consts.DEBUG_MODE)


memoryManager = MemoryManager()

semanticTable = consts.semanticTable

def backFromFunction(returnValue):
    (returnAddress, originalInstructionPointer) = memoryManager.popReturnPointers()
    debug.print("Back fF poped returnAddress: ", returnAddress)
    # Get list from pointer
    pythonList = memoryManager.getPythonlistFromPointer(returnValue)
    debug.print("Back fF python list: ", pythonList)
    memoryManager.popContext()
    # Store list in memory
    debug.print("Back fF memory before to PointerList: ", memoryManager.memory)
    newAddress = memoryManager.pythonlistToPointerList(pythonList)
    debug.print("Back fF newAddress: ", newAddress)
    debug.print("Back fF memory before set: ", memoryManager.memory)
    memoryManager.setValue(returnAddress, newAddress)
    debug.print("Back fF memory after set: ", memoryManager.memory)

    return originalInstructionPointer + 1


# INSTRUCTIONS DEFINITIONS =========

def VECT(quad, instructionPointer):
    pass


def CONST(quad, instructionPointer):
    value = quad[1]
    address = quad[3]
    memoryManager.setValue(address, value)

def funcSize(quad, instructionPointer):
    functionPointer = quad[1]
    functionParamsCount = quad[2]
    memoryManager.addFunction(functionPointer, functionParamsCount)

def goto(quad, instructionPointer):
    instructionPointer = quad[1]
    return instructionPointer

#(10, None)  => [10]
#((11, None), ((-5.0, None), ((10, None), None))) => [11, -5, 10]
def flattenPythonList(pythonList):
    if pythonList == None or len(pythonList) == 0 or (len(pythonList) == 1 and pythonList[0] == None):
        return [None]

    flattenedList = []
    
    def helper(pythonList):
        
        if type(pythonList[0]) == tuple:
            if type(pythonList[1]) == tuple:
                helper(pythonList[1])
            elif pythonList[1] != None:
                raise Exception("Invalid right side of tuple at flattenPythonList")
                
            if type(pythonList[0][0]) == float:
                helper(pythonList[0])
            else:
                raise Exception("can not flatten list of depth grater than 1")
            
        elif type(pythonList[0]) == float and pythonList[1] == None:
            flattenedList.append(pythonList[0])
        else:
            raise Exception("Invalid list at flattenPythonList")

    helper(pythonList)
    return flattenedList

def gotoFalse(quad, instructionPointer):
    #debug.print("goto cond address: ", quad[1])
    
    address = memoryManager.getValue(quad[1])
    condition = True

    debug.print("goto cond value: ", address)

    if address == None:
        condition = False
    elif type(address) == float:
        condition = False if address == 0.0 else True
    elif memoryManager.pointerIsList(address):
        #address = memoryManager.getValue(address)
        lista = memoryManager.getPythonlistFromPointer(address)
        #debug.print("flatenned goto cond list: ", lista)
        debug.print("goto list as pythonList", lista)
        lista = flattenPythonList(lista)
        debug.print("goto list as flattened pythonList", lista)

        condition = False
        if not(lista == None or (len(lista) == 1 and lista[0] == None)):
            for e in lista:
                if type(e) == tuple:
                    raise Exception("cannot evaluate truthness of nested list")
                if e != 0.0 and e != None:
                    condition = True
                    break
    
    if(not condition):
        #debug.print("jumped :)")
        return quad[2]
    #debug.print("did not jump :<")


def era(quad, instructionPointer):
    funcName = quad[1]
    debug.print("Executing: {}".format(funcName))

def assign(quad, instructionPointer):
    value = quad[1]
    address = quad[3]
    memoryManager.setValue(address, value)

def endfunc(quad, instructionPointer):
    tempReturnAddress = quad[1]

    debug.print("Temp return address after function", tempReturnAddress)
    debug.print("meomry at endFunc: ", memoryManager.memory)
    debug.print("pointer to return of func at endFunc: ", tempReturnAddress)
    returnValue = memoryManager.getValue(tempReturnAddress)
    if type(returnValue) == float:
        #returnValue = [returnValue]
        debug.print("Returned valued after function", returnValue)
        return backFromFunction(tempReturnAddress)

    debug.print("Returned valued after function", returnValue)

    # returnValue = memoryManager.flatListToFunctionalList(returnValue)
    # debug.print("Returned valued after list conversion", returnValue)
    
    return backFromFunction(returnValue)


def gosub(quad, instructionPointer):
    funcName = quad[1]
    returnAddress = quad[3]
    isUserDefinedFunction = type(funcName) == int

    if isUserDefinedFunction:
        # Get local lists to python list from parent function
        paramCount = memoryManager.getFunctionParamsCount(funcName)
        paramsList = memoryManager.popParams(paramCount)
        paramsList.reverse()
        debug.print("user Func paramsList: ", paramsList)

        pythonParamsList = []
        for e in paramsList:
            #debug.print("converting param address", e, " to list")
            pythonParamsList.append(memoryManager.getPythonlistFromPointer(e))
        
        debug.print("user Func pythonParamsList: ", pythonParamsList)

        memoryManager.pushContext()
        memoryManager.pushReturnPointers(returnAddress, instructionPointer)
        
        #convert python list back to memory in child function
        memoryParamsList = []
        for e in pythonParamsList:
            memoryParamsList.append(memoryManager.pythonlistToPointerList(e))

        debug.print("user Func memoryParamsList: ", memoryParamsList)

        for i in range(0, paramCount):
            memoryManager.setValue(consts.LIMITS["LOCAL_LIM_L"] + i , memoryParamsList[i])

        debug.print("Memory after gosub : ", memoryManager.memory)

        return funcName
    else:
        #memoryManager.pushReturnPointers(returnAddress, instructionPointer)

        paramCount = len(semanticTable[funcName][0])
        paramsList = memoryManager.popParams(paramCount)
        paramsList.reverse()

        debug.print("lang Func paramsList: ", paramsList)

        pythonParamsList = []
        for e in paramsList:
            pythonParamsList.append(memoryManager.getPythonlistFromPointer(e))
        
        debug.print("lang Func pythonParamsList: ", pythonParamsList)

        memoryManager.pushContext()
        
        returnList = None
        flattenedParams = languageFunctions.flattenPythonList(pythonParamsList)
        debug.print("lang Func pythonParamsList after flatten: ", flattenedParams)
        returnValue = list(langFunctions[funcName](memoryManager, flattenedParams))

        debug.print("Returned valued after lang function", returnValue)
        returnValue = memoryManager.flatListToFunctionalList(returnValue)
        debug.print("Returned valued after list conversion", returnValue)

        memoryManager.popContext()

        if returnValue is not None:
            returnList = memoryManager.pythonlistToPointerList(returnValue) #convert the returned python list from the language function to a pointer list in memory
            debug.print("lang Func memoryReturnList: ", returnList)
        #backFromFunction(returnValue)

        #(returnAddress, originalInstructionPointer) = memoryManager.popReturnPointers()
        # Get list from pointer
        #pythonList = memoryManager.getPythonlistFromPointer(returnValue)
        #memoryManager.popContext()
        # Store list in memory
        #newAddress = memoryManager.pythonlistToPointerList(pythonList)
        memoryManager.setValue(returnAddress, returnList)

        debug.print("Memory after gosub : ", memoryManager.memory)

        return instructionPointer + 1

def lista(quad, instructionPointer):
    left = quad[1]
    right = quad[2]
    address = quad[3]

    memoryManager.setListPair(address, left, right)


def params(quad, instructionPointer):
    head = quad[1]

    debug.print("Current Memory: ", memoryManager.memory)

    paramsList = flattenList(head)
    debug.print("function params ", paramsList)

    newParamsList = []
    for e in paramsList:
        condition = True
        if memoryManager.pointerIsList(e):
            (left, right) = memoryManager.getListPair(e)

            if memoryManager.addressIsTemp(left):
                if right == None:
                    condition = False
                    newParamsList.append(memoryManager.getValue(left))
                else:
                    raise Exception("This should not happen, when obtaining parameters from a temp pointer")
                
        if condition:
            newParamsList.append(e)
    
    debug.print("new function params ", newParamsList)
    # push params to params stack
    memoryManager.pushParams(newParamsList)

def PROGRAM(quad, instructionPointer):
    pass


def flattenList(headAddress):
    if headAddress == None:
        return []
    listArray = []
    #debug.print("flatenning: ", headAddress)
    flattenListRecursive(headAddress, listArray)
    #debug.print("getListPair in flattening list: ", listArray)
    if listArray[-1] == None:
        listArray = listArray[0:-1]
    return listArray


def flattenListRecursive(headAddress, listArray):
    #memoryManager.pointerIsList(headAddress)
    (left, right) = memoryManager.getListPair(headAddress)
    
    listArray.append(left)
    if right == None or type(right) == float or not memoryManager.pointerIsList(right):
        listArray.append(right)
    else:
        flattenListRecursive(right, listArray)

#=======================================================================

instructions = {
    "VECT": VECT,
    "CONST": CONST,
    "goto": goto,
    "gosub": gosub,
    "gotoFalse": gotoFalse,
    "era": era,
    "params": params,
    "list": lista,
    "endfunc": endfunc,
    "PROGRAM": PROGRAM,
    "funcSize": funcSize,
    "assign": assign
}

langFunctions = {
    "print": languageFunctions.printList,
    #Math operations
    "add": languageFunctions.add,
    "sub": languageFunctions.sub,
    "power": languageFunctions.power,
    "mult": languageFunctions.mult,
    "div": languageFunctions.div,
    "sqrt": languageFunctions.sqrt,
    "abs": languageFunctions.absop,
    #Logical operators 
    "and": languageFunctions.andOp,
    'or': languageFunctions.orOp,
    'not': languageFunctions.notOp,
    #Relational operators
    '>=': languageFunctions.biggerequal,
    '<=': languageFunctions.lessrequal,
    '>': languageFunctions.bigger,
    '<': languageFunctions.less,
    '!=': languageFunctions.notqueal,
    '=': languageFunctions.equal,
    #List Access
    'append': languageFunctions.append,
    'isList': languageFunctions.isList,
    'single': languageFunctions.single,
    'car': languageFunctions.car,
    'cdr': languageFunctions.cdr,
    'empty': languageFunctions.empty,
    'elemCount': languageFunctions.elemCount,
    'lenght': languageFunctions.lenght,
}


