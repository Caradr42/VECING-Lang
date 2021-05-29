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
    #print("goto cond address: ", quad[1])
    
    address = memoryManager.getValue(quad[1])
    condition = True

    print("goto cond value: ", address)

    if address == None:
        condition = False
    elif type(address) == float:
        condition = False if address == 0.0 else True
    elif memoryManager.pointerIsList(address):
        #address = memoryManager.getValue(address)
        lista = memoryManager.getPythonlistFromPointer(address)
        #print("flatenned goto cond list: ", lista)

        condition = False
        for e in lista:
            if type(e) == tuple:
                raise Exception("cannot evaluate truthness of nested list")
            if e != 0.0 and e != None:
                condition = True
                break
    
    if(not condition):
        #print("jumped :)")
        return quad[2]
    #print("did not jump :<")


def era(quad, instructionPointer):
    funcName = quad[1]
    print("Executing: {}".format(funcName))


def endfunc(quad, instructionPointer):
    tempReturnAddress = quad[1]
    print("Temp return address after function", tempReturnAddress)
    returnValue = memoryManager.getValue(tempReturnAddress)
    print("Returned valued after function", returnValue)
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
        print("user Func paramsList: ", paramsList)

        pythonParamsList = []
        for e in paramsList:
            #print("converting param address", e, " to list")
            pythonParamsList.append(memoryManager.getPythonlistFromPointer(e))
        
        print("user Func pythonParamsList: ", pythonParamsList)

        memoryManager.pushContext()
        memoryManager.pushReturnPointers(returnAddress, instructionPointer)
        
        #convert python list back to memory in child function
        memoryParamsList = []
        for e in pythonParamsList:
            memoryParamsList.append(memoryManager.pythonlistToPointerList(e))

        print("user Func memoryParamsList: ", memoryParamsList)

        for i in range(0, paramCount):
            memoryManager.setValue(consts.LIMITS["LOCAL_LIM_L"] + i , memoryParamsList[i])

        print("Memory after gosub : ", memoryManager.memory)

        return funcName
    else:
        #memoryManager.pushReturnPointers(returnAddress, instructionPointer)

        paramCount = len(semanticTable[funcName][0])
        paramsList = memoryManager.popParams(paramCount)
        paramsList.reverse()

        print("lang Func paramsList: ", paramsList)

        pythonParamsList = []
        for e in paramsList:
            pythonParamsList.append(memoryManager.getPythonlistFromPointer(e))
        
        print("lang Func pythonParamsList: ", pythonParamsList)
        
        returnList = None
        flattenedParams = languageFunctions.flattenPythonList(pythonParamsList)
        returnValue = langFunctions[funcName](memoryManager, flattenedParams)

        print("Returned valued after lang function", returnValue)
        returnValue = memoryManager.flatListToFunctionalList(returnValue)
        print("Returned valued after list conversion", returnValue)

        if returnValue is not None:
            returnList = memoryManager.pythonlistToPointerList(returnValue) #convert the returned python list from the language function to a pointer list in memory
            print("lang Func memoryParamsList: ", returnList)
        #backFromFunction(returnValue)

        #(returnAddress, originalInstructionPointer) = memoryManager.popReturnPointers()
        # Get list from pointer
        #pythonList = memoryManager.getPythonlistFromPointer(returnValue)
        #memoryManager.popContext()
        # Store list in memory
        #newAddress = memoryManager.pythonlistToPointerList(pythonList)
        memoryManager.setValue(returnAddress, returnList)

        print("Memory after gosub : ", memoryManager.memory)

        return instructionPointer + 1

def lista(quad, instructionPointer):
    left = quad[1]
    right = quad[2]
    address = quad[3]

    memoryManager.setListPair(address, left, right)


def params(quad, instructionPointer):
    head = quad[1]

    print("Current Memory: ", memoryManager.memory)

    paramsList = flattenList(head)
    print("function params ", paramsList)

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
    
    print("new function params ", newParamsList)
    # push params to params stack
    memoryManager.pushParams(newParamsList)

def PROGRAM(quad, instructionPointer):
    pass


def flattenList(headAddress):
    listArray = []
    #print("flatenning: ", headAddress)
    flattenListRecursive(headAddress, listArray)
    #print("getListPair in flattening list: ", listArray)
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
    "funcSize": funcSize
}

langFunctions = {
    "print": languageFunctions.printList,
    "add": languageFunctions.add,
    "sub": languageFunctions.sub,
    "power": languageFunctions.power,
    "mult": languageFunctions.mult,
    "div": languageFunctions.div,
    "sqrt": languageFunctions.sqrt,
    "abs": languageFunctions.absop
}

