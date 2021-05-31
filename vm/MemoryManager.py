import sys
sys.path.append('../')

import consts
import pprint
from Stack import Stack
from utils import Debugger

debug = Debugger(consts.DEBUG_MODE)


class MemoryManager():
    def __init__(self):
        self.memory = {
            'global': {},
            'local': {},
            'list': {},
            'temporal': {},
            "temporalList": {}
        }

        self.stackMemorySpace = consts.LIMITS["STACK_SIZE"]
        self.localsStack = Stack()
        self.temporalsStack = Stack()
        self.listsStack = Stack()
        self.temporalListsStack = Stack()

        self.params = Stack()
        self.returnPointers = Stack()

        self.functionsTable = {}

    def __str__(self):
        return "MemoryManager(\n{}\n)".format(pprint.pformat(self.memory))

    def getPythonlistFromPointer(self, address):
        if type(address) == int:
            isListAddress = (address >= consts.LIMITS["LIST_LIM_L"] and address < consts.LIMITS["LIST_LIM_R"]) or (
                address >= consts.LIMITS["TEMPORAL_LIST_LIM_L"] and address < consts.LIMITS["TEMPORAL_LIST_LIM_R"])
 
            if self.addressIsTemp(address):
                address = self.getValue(address)
                return self.getPythonlistFromPointer(address)
            
            if isListAddress:
                #debug.print("is list")
                (left, right) = self.getListPair(address)

                # if self.pointerIsTemp(left):
                #     left = self.getValue(left)
                # if self.pointerIsTemp(right):
                #     right = self.getValue(right)

                return (self.getPythonlistFromPointer(left), self.getPythonlistFromPointer(right))

            #TODO: FIX this ##########################################################################################
            elif self.pointerIsConstant(address):
                address = self.getValue(address)
                
                return (self.getPythonlistFromPointer(address), None)
            else:
                address = self.getValue(address)
                # if self.pointerIsTemp(address):
                #     address = self.getValue(address)
                
                return self.getPythonlistFromPointer(address)
                #return (self.getPythonlistFromPointer(address), None)

        elif address is None or type(address) == float:
            #debug.print("value")
            return address
        else:
            raise Exception("This is not posible")

    #(1,2,3) => ((1, None), ((2, None), ((3, None), None)))'
    #((1,),2,3) => ((1, None), ((2, None), ((3, None), None)))

    #[(2.0,), (8.0,)] => ((((2.0, None), None), None), (((8.0, None), None), None))


    #[(8.0,), (2.0,)]
    def flatListToFunctionalList(self, flatList):
        if type(flatList) == float:
            return (flatList, None)

        if flatList == None or len(flatList) == 0:
            return flatList
        if len(flatList) == 1:
            return (flatList[0], None)
        if type(flatList) == tuple:
            flatList = list(flatList)
        flatList.reverse()
        
        inside = flatList[0]
        if type(inside) == tuple and len(inside) == 1:
            inside = (self.flatListToFunctionalList(inside[0]), None)
            funcList = (inside, None)
        elif type(inside) == tuple:
            funcList = (self.flatListToFunctionalList(inside), None)
        elif type(inside) == float:
            funcList = (self.flatListToFunctionalList(inside), None)
        else:
            funcList = self.flatListToFunctionalList(inside)

        for e in flatList[1:]:
            temp = e
            if type(e) == tuple and len(e) == 1:
                temp = ((self.flatListToFunctionalList(e[0]), None), None)
                funcList = (temp, funcList)
            elif type(e) == tuple:
                funcList = (self.flatListToFunctionalList(temp), funcList)
            else:
                funcList = (self.flatListToFunctionalList(temp), funcList)
        return funcList

    def pythonlistToPointerList(self, pythonList): # [((1.0, None), None)]
        debug.print("PLtPL: ", pythonList)
        left = None
        right = None

        if type(pythonList) == tuple or type(pythonList) == list:
            # Functional lists always have two elements or be None
            if len(pythonList) == 0:
                return None
            if len(pythonList) == 1 and pythonList[0] == None:
                return None
            if len(pythonList) == 1 and type(pythonList[0]) == float:
                #pythonList.append(None)
                pythonList = (pythonList[0], None)
            
            if type(pythonList[0]) == tuple or type(pythonList[0]) == list:
                left = self.pythonlistToPointerList(pythonList[0])
            else:
                left = pythonList[0]

            if type(pythonList[1]) == tuple or type(pythonList[1]) == list:
                right = self.pythonlistToPointerList(pythonList[1])
            else:
                right = pythonList[1]
        else:
            return pythonList
        return self.setTemporalListPair(left, right)

    def stackMemoryCheck(self, message):
        if self.stackMemorySpace <= 0:
            raise Exception(message)

    def addFunction(self, functionInstructionPointer, functionParamQty):
        self.functionsTable[functionInstructionPointer] = functionParamQty

    def getFunctionParamsCount(self, functionInstructionPointer):
        try:
            paramCount = self.functionsTable[functionInstructionPointer]
            return paramCount
        except:
            raise Exception(
                "Tried to access non registered function in memory")

    def getContextSize(self):
        return len(list(self.memory["local"].keys())) + len(list(self.memory["temporal"].keys())) + len(list(self.memory["list"].keys()))

    def getMemorySegment(self, address):
        memorySegment = None

        if address >= consts.LIMITS["GLOBAL_LIM_L"] and address <= consts.LIMITS["GLOBAL_LIM_R"]:
            memorySegment = self.memory["global"]

        elif address >= consts.LIMITS["LOCAL_LIM_L"] and address <= consts.LIMITS["LOCAL_LIM_R"]:
            memorySegment = self.memory["local"]

        elif address >= consts.LIMITS["TEMPORAL_LIM_L"] and address <= consts.LIMITS["TEMPORAL_LIM_R"]:
            memorySegment = self.memory["temporal"]

        # Since a list requires two adjacent address spaces in memory, the right limit is not inclusive
        elif address >= consts.LIMITS["LIST_LIM_L"] and address < consts.LIMITS["LIST_LIM_R"]:
            memorySegment = self.memory["list"]

        elif address >= consts.LIMITS["TEMPORAL_LIST_LIM_L"] and address < consts.LIMITS["TEMPORAL_LIST_LIM_R"]:
            memorySegment = self.memory["temporalList"]

        return memorySegment
    
    def pointerIsList(self, address):
        if address is None or type(address) == float:
            raise Exception("Tried to access non pointer as pointer")
        return (address >= consts.LIMITS["LIST_LIM_L"] and address < consts.LIMITS["LIST_LIM_R"]) or (address >= consts.LIMITS["TEMPORAL_LIST_LIM_L"] and address < consts.LIMITS["TEMPORAL_LIST_LIM_R"])

    def addressIsTemp(self, address):
        # if address is None or type(address) == float:
        #     raise Exception("Tried to access non pointer as pointer")
        return address >= consts.LIMITS["TEMPORAL_LIM_L"] and address < consts.LIMITS["TEMPORAL_LIM_R"]


    def pointerIsConstant(self, address):
        if address is None or type(address) == float:
            raise Exception("Tried to access non pointer as pointer")
        return address >= consts.LIMITS["GLOBAL_LIM_L"] and address < consts.LIMITS["GLOBAL_LIM_R"]

    def setValue(self, address, value):
        memorySegment = self.getMemorySegment(address)
        if memorySegment == None:
            raise Exception(
                "Invalid memmory address set of {} at address {}".format(value, address))

        memorySegment[address] = value

    def getValue(self, address):
        memorySegment = self.getMemorySegment(address)
        if memorySegment == None:
            raise Exception(
                "Invalid access to memmory address at {}".format(address))

        try:
       #     debug.print(self.memory)
            memory = memorySegment[address]
            #debug.print("Retuned getValue: ", memory)
            #check if address is pointer and points to a constant

            if not (memory is None or type(memory) == float) and self.pointerIsConstant(memory):
                memorySegment = self.getMemorySegment(memory)
                returnValue =  memorySegment[memory]
                return returnValue
            # Check if adress is a pointer, yet not a list pointer, and its value is a list pointer
            # elif address is not None and type(address) != float and not self.pointerIsList(address) and  self.pointerIsList(memory):
            #     return returnValue
                

            return memory
        except:
            raise Exception(
                "Tried to access non existing memory at address {}".format(address))

    def setTemporalListPair(self, left, right):
        address = len(self.memory["temporalList"].keys()) + \
            consts.LIMITS["TEMPORAL_LIST_LIM_L"]
        self.setListPair(address, left, right)
        return address

    def setListPair(self, address, left, right):
        self.setValue(address, left)
        self.setValue(address + 1, right)

    def getListPair(self, address):
        left = self.getValue(address)
        right = self.getValue(address + 1)
        return (left, right)

    def popContext(self):
        try:
            self.memory["local"] = self.localsStack.pop()
            self.memory["temporal"] = self.temporalsStack.pop()
            self.memory["list"] = self.listsStack.pop()
            self.memory["temporalList"] = self.temporalListsStack.pop()

            contextSize = self.getContextSize()

            self.stackMemorySpace += contextSize

        except:
            raise Exception("Invalid context change, alredy at global context")

    def pushContext(self):
        contextSize = self.getContextSize()

        self.stackMemorySpace -= contextSize
        self.stackMemoryCheck("Memory limit excedeed, Stack Overflow")

        self.localsStack.push(self.memory["local"])
        self.temporalsStack.push(self.memory["temporal"])
        self.listsStack.push(self.memory["list"])
        self.temporalListsStack.push(self.memory["temporalList"])

        self.memory["local"] = {}
        self.memory["temporal"] = {}
        self.memory["list"] = {}
        self.memory["temporalList"] = {}

    def popReturnPointers(self):
        self.stackMemorySpace += 2
        try:
            addressInstpointerPair = self.returnPointers.pop()
            return addressInstpointerPair
        except:
            raise Exception("Invalid stack call")

    def pushReturnPointers(self, address, instructionPointer):
        self.stackMemorySpace -= 2
        self.stackMemoryCheck("Memory limit excedeed, Stack Overflow")
        return self.returnPointers.push((address, instructionPointer))

    def popParams(self, size):
        paramsList = []
        try:
            for _ in range(size):
                paramsList.append(self.params.pop())
            self.stackMemorySpace += size
        except:
            raise Exception("Invalid stack call")
            
        #debug.print("Function Parameters:", paramsList)
        return paramsList

    def pushParams(self, paramsList):
        self.stackMemorySpace -= len(paramsList)
        self.stackMemoryCheck("Memory limit excedeed, Stack Overflow")

        for param in paramsList:
            self.params.push(param)
