import sys
sys.path.append('../')

import consts
import pprint
from Stack import Stack



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
            isListAddress = (address > consts.LIMITS["LIST_LIM_L"] and address < consts.LIMITS["LIST_LIM_R"]) or (
                address > consts.LIMITS["TEMPORAL_LIST_LIM_L"] and address < consts.LIMITS["TEMPORAL_LIST_LIM_R"])
            if isListAddress:
                print("is list")
                (left, right) = self.getListPair(address)
                return (self.getPythonlistFromPointer(left), self.getPythonlistFromPointer(right))
            else:
                address = self.getValue(address)
                print("not a list")
                return (self.getPythonlistFromPointer(address), None)

        elif type(address) == float:
            print("value")
            return address
        else:
            raise Exception("This is not posible")

    def pythonlistToPointerList(self, pythonList):
        left = None
        right = None

        if type(pythonList[0]) == tuple:
            left = self.pythonlistToPointerList(pythonList[0])
        else:
            left = pythonList[0]

        if type(pythonList[1]) == tuple:
            right = self.pythonlistToPointerList(pythonList[1])
        else:
            right = pythonList[1]
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

        if address >= consts.LIMITS["GLOBAL_LIM_L"] and address < consts.LIMITS["GLOBAL_LIM_R"]:
            memorySegment = self.memory["global"]

        elif address >= consts.LIMITS["LOCAL_LIM_L"] and address < consts.LIMITS["LOCAL_LIM_R"]:
            memorySegment = self.memory["local"]

        elif address >= consts.LIMITS["TEMPORAL_LIM_L"] and address < consts.LIMITS["TEMPORAL_LIM_R"]:
            memorySegment = self.memory["temporal"]

        elif address >= consts.LIMITS["LIST_LIM_L"] and address < consts.LIMITS["LIST_LIM_R"]:
            memorySegment = self.memory["list"]

        elif address >= consts.LIMITS["TEMPORAL_LIST_LIM_L"] and address < consts.LIMITS["TEMPORAL_LIST_LIM_R"]:
            memorySegment = self.memory["temporalList"]

        return memorySegment
    
    def pointerIsList(self, address):
        return (address >= consts.LIMITS["LIST_LIM_L"] and address < consts.LIMITS["LIST_LIM_R"]) or (address >= consts.LIMITS["TEMPORAL_LIST_LIM_L"] and address < consts.LIMITS["TEMPORAL_LIST_LIM_R"])

    def pointerIsConstant(self, address):
        return address < consts.INITIAL_ADDRESS

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
            memory = memorySegment[address]
            if self.pointerIsConstant(memory):
                memorySegment = self.getMemorySegment(memory)
                return memorySegment[memory]

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
            
        print("Function Parameters:", paramsList)
        return paramsList

    def pushParams(self, paramsList):
        self.stackMemorySpace -= len(paramsList)
        self.stackMemoryCheck("Memory limit excedeed, Stack Overflow")

        for param in paramsList:
            self.params.push(param)
