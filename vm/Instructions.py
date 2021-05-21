import MemoryManager
memoryManager = MemoryManager()

instructions = {
    "VECT": VECT,
    "CONST": CONST,
    "goto": goto,
    "gosub": None,
    "gotoFalse": gotoFalse,
    "era": None,
    "params": None,
    "list": None,
    "VAR":None
    "endfunc": None,
    "PROGRAM": None,
}

langFunctions = {
    "add": lambda x,y: x + y   
}

def VECT(quad):
    pass

def CONST(quad):
    value = quad[1]
    address = quad[3]
    memoryManager.setValue(address, value)

def goto(quad):
    instructionPointer = quad[1]
    return instructionPointer

def gotoFalse(quad):
    value = memoryManager.getValue(quad[1])
    condition = False if value == 0.0 else True

    if(not condition):
        return quad[2]
    
def era(quad):
    funcName = quad[1]
    pass

def gosub(quad):
    funcName = quad[1]
    returnTemp = quad[3]

    if type(funcName) == int:
        return funcName
    else:
        pass

