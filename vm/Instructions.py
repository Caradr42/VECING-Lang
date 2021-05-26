from MemoryManager import MemoryManager
import languageFunctions
import consts

memoryManager = MemoryManager()

semanticTable = consts.semanticTable

def backFromFunction(returnValue):
    (returnAddress, originalInstructionPointer) = memoryManager.popReturnPointers()
    # Get list from pointer
    pythonList = memoryManager.getPythonlistFromPointer(returnValue)
    memoryManager.popContext()
    # Store list in memory
    newAddress = memoryManager.pythonlistToPointerList(pythonList)

    memoryManager.setValue(returnAddress, newAddress)

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


def gotoFalse(quad, instructionPointer):
    value = memoryManager.getValue(quad[1])
    condition = False if value == 0.0 else True

    if(not condition):
        return quad[2]


def era(quad, instructionPointer):
    funcName = quad[1]
    print("Executing: {}".format(funcName))


def endfunc(quad, instructionPointer):
    tempReturnAddress = quad[1]
    returnValue = memoryManager.getValue(tempReturnAddress)

    return backFromFunction(returnValue)


def gosub(quad, instructionPointer):
    funcName = quad[1]
    returnAddress = quad[3]
    isUserDefinedFunction = type(funcName) == int

    

    if isUserDefinedFunction:
        memoryManager.pushContext()
        memoryManager.pushReturnPointers(returnAddress, instructionPointer)
        # push params to context
        paramCount = memoryManager.getFunctionParamsCount(funcName)
        paramsList = memoryManager.popParams(paramCount)
        paramsList.reverse()

        print(paramCount)

        for i in range(0, paramCount):
            memoryManager.setValue(consts.LIMITS["LOCAL_LIM_L"] + i , paramsList[i])

        return funcName
    else:
        #memoryManager.pushReturnPointers(returnAddress, instructionPointer)

        paramCount = len(semanticTable[funcName][0])
        paramsList = memoryManager.popParams(paramCount)
        paramsList.reverse()

        

        pythonParamsList = []
        for e in paramsList:
            pythonParamsList.append(memoryManager.getPythonlistFromPointer(e))
        print("parameters python list: ", pythonParamsList)
        
        returnList = None
        returnValue = langFunctions[funcName](memoryManager, pythonParamsList)
        if returnValue is not None:
            returnList = memoryManager.pythonlistToPointerList(returnValue) #convert the returned python list front the language function to a pointer list in memory
        #backFromFunction(returnValue)

        #(returnAddress, originalInstructionPointer) = memoryManager.popReturnPointers()
        # Get list from pointer
        #pythonList = memoryManager.getPythonlistFromPointer(returnValue)
        #memoryManager.popContext()
        # Store list in memory
        #newAddress = memoryManager.pythonlistToPointerList(pythonList)
        memoryManager.setValue(returnAddress, returnList)

        return instructionPointer + 1

def lista(quad, instructionPointer):
    left = quad[1]
    right = quad[2]
    address = quad[3]

    memoryManager.setListPair(address, left, right)


def params(quad, instructionPointer):
    head = quad[1]
    paramsList = flattenList(head)

    # push params to params stack
    memoryManager.pushParams(paramsList)


def PROGRAM(quad, instructionPointer):
    pass


def flattenList(headAddress):
    listArray = []
    flattenListRecursive(headAddress, listArray)
    return listArray


def flattenListRecursive(headAddress, listArray):
    #memoryManager.pointerIsList(headAddress)
    (left, right) = memoryManager.getListPair(headAddress)

    listArray.append(left)

    if type(right) == float or not memoryManager.pointerIsList(right):
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
    "funcSize": funcSize
}

langFunctions = {
    "add": languageFunctions.add,
    "sub": languageFunctions.sub
}

"""
list 1000 None 70000   (1000, None)
list 1001 None 70001   (1001, None)
list 70000 70001 70002 ((1000, None), (((1000, None), None), (1001, None)))

1000, 70000, 1001
params 70002 None param1


"""
