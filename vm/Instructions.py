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
    """ Instruction to add a const to v memory
    This function is executed by the VM in VENCING_VM.py by using the instructions 
        dictionary wich contains all the intructions functions paired to their name.  

    parameters
    ----------
    quad: a python list with the four elements of the quad being executed
    instructionPointer: an integer with the corresponding instructionPointer of the quad 
        in the list of quads. 
    """
    value = quad[1]
    address = quad[3]
    memoryManager.setValue(address, value)

def funcSize(quad, instructionPointer):
    """ Instruction to add a function to the functionsTable in the MemoryManager
    This function is executed by the VM in VENCING_VM.py by using the instructions 
        dictionary wich contains all the intructions functions paired to their name.  

    parameters
    ----------
    quad: a python list with the four elements of the quad being executed
    instructionPointer: an integer with the corresponding instructionPointer of the quad 
        in the list of quads. 
    """
    functionPointer = quad[1]
    functionParamsCount = quad[2]
    memoryManager.addFunction(functionPointer, functionParamsCount)

def goto(quad, instructionPointer):
    """ Instruction to make a jump during code execution
    This function is executed by the VM in VENCING_VM.py by using the instructions 
        dictionary wich contains all the intructions functions paired to their name.  

    parameters
    ----------
    quad: a python list with the four elements of the quad being executed
    instructionPointer: an integer with the corresponding instructionPointer of the quad 
        in the list of quads. 

    returns
    -------
    instructionPointer: the quad number to which the VM will jump next 
    """
    instructionPointer = quad[1]
    return instructionPointer

#(10, None)  => [10]
#((11, None), ((-5.0, None), ((10, None), None))) => [11, -5, 10]
def flattenPythonList(pythonList):
    """ receives a list of the form:
            [((10.0, None), ((11.0, None), ((12.0, None), None)))]
        and returns a normal python list with its contents 
    This function is used by Instructions.py

    parameters
    ----------
    pythonList: a list of the form:
        ((10.0, None), ((11.0, None), ((12.0, None), None)))

    returns
    -------
    flattenedList: a normal python list
    """
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
                raise Exception("language function does not accept list of depth greater than 1")
            
        elif type(pythonList[0]) == float and pythonList[1] == None:
            flattenedList.append(pythonList[0])
        else:
            raise Exception("Invalid list at flattenPythonList")

    helper(pythonList)
    return flattenedList

def gotoFalse(quad, instructionPointer):
    """ Instruction to make a jump during code execution if the value stored in the quad 
        parameter 1 is equal to 0.0 and thus False
        This function is executed by the VM in VENCING_VM.py by using the instructions 
        dictionary wich contains all the intructions functions paired to their name.  

    parameters
    ----------
    quad: a python list with the four elements of the quad being executed
    instructionPointer: an integer with the corresponding instructionPointer of the quad 
        in the list of quads. 

    returns
    -------
    instructionPointer: the quad number to which the VM will jump next 
    """
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
    """ Function that gets executed by the VM whenever a quad with the era
        instruction appears. The quads informs that a function call has started,
        and the name of instruction pointer of the function is saved.
        This function is executed by the VM in VENCING_VM.py by using the instructions 
        dictionary wich contains all the intructions functions paired to their name.  

    parameters
    ----------
    quad: a python list with the four elements of the quad being executed
    instructionPointer: an integer with the corresponding instructionPointer of the quad 
        in the list of quads.
    """
    funcName = quad[1]
    debug.print("Executing: {}".format(funcName))

def assign(quad, instructionPointer):
    """ Function that gets executed by the VM whenever a quad with the assign
        instruction appears. It simply tells the VM to put the value that the quad has in its
        second element, to the virtual address in the fourth element of the quad.
        This function is executed by the VM in VENCING_VM.py by using the instructions 
        dictionary wich contains all the intructions functions paired to their name.  

    parameters
    ----------
    quad: a python list with the four elements of the quad being executed
    instructionPointer: an integer with the corresponding instructionPointer of the quad 
        in the list of quads.
    """
    value = quad[1]
    address = quad[3]

    debug.print("assigned: ", value, " to ", address)
    memoryManager.setValue(address, value)

def endfunc(quad, instructionPointer):
    """ Instruction to make a jump at the end of a function execution, back to the 
        original quad the function was called from
        This function is executed by the VM in VENCING_VM.py by using the instructions 
        dictionary wich contains all the intructions functions paired to their name.  

    parameters
    ----------
    quad: a python list with the four elements of the quad being executed
    instructionPointer: an integer with the corresponding instructionPointer of the quad 
        in the list of quads. 

    returns
    -------
    instructionPointer: the quad number to which the VM will jump next 
    """
    tempReturnAddress = quad[1]

    debug.print("endFunc: ")    
    debug.print("Temp return address after function", tempReturnAddress)
    debug.print("meomry at endFunc: ", memoryManager.memory)
    debug.print("pointer to return result of func at endFunc: ", tempReturnAddress)
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
    """ Instruction to make a jump to the beginning of a function if the quad got
        an instruction pointer, else if it has a lang function name it executes it using 
        the langFunctions dictionary wich stores the functions imported form 
        languageFunctions.py
        This instruction also manages all the process of getting the params from the stack and saving
        them in the local context of the function, and then proceeds to create a new context.
        This function is executed by the VM in VENCING_VM.py by using the instructions 
        dictionary wich contains all the intructions functions paired to their name.  

    parameters
    ----------
    quad: a python list with the four elements of the quad being executed
    instructionPointer: an integer with the corresponding instructionPointer of the quad 
        in the list of quads. 

    returns
    -------
    instructionPointer: the quad number to which the VM will jump next, in this case
        the pointer to function geting executed
    """
    funcName = quad[1]
    returnAddress = quad[3]
    isUserDefinedFunction = type(funcName) == int

    debug.print("gosub: ", funcName)

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
    """ Function that gets executed by the VM whenever a quad with the list
        instruction appears. It tells to the memory manager to save in memory
        both given elements.
        This function is executed by the VM in VENCING_VM.py by using the instructions 
        dictionary wich contains all the intructions functions paired to their name.  

    parameters
    ----------
    quad: a python list with the four elements of the quad being executed
    instructionPointer: an integer with the corresponding instructionPointer of the quad 
        in the list of quads.
    """
    left = quad[1]
    right = quad[2]
    address = quad[3]

    memoryManager.setListPair(address, left, right)


def params(quad, instructionPointer):
    """ Function that gets executed by the VM whenever a quad with the params
        instruction appears. It gets the parameters from the specified virtual
        address in the quads and pushes those parameters indivdually into a stack
        in the VM.
        This function is executed by the VM in VENCING_VM.py by using the instructions 
        dictionary wich contains all the intructions functions paired to their name.  

    parameters
    ----------
    quad: a python list with the four elements of the quad being executed
    instructionPointer: an integer with the corresponding instructionPointer of the quad 
        in the list of quads.
    """
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
                    raise Exception("Error in parameters list in memory representation")
                
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
    'length': languageFunctions.length,
}


