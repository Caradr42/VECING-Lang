from consts import LIMITS
import pprint
import Stack


class MemoryManager():
    def __init__(self):
        self.memory = {
            'global': {},
            'local': {},
            'list': {},
            'temporal': {}
        }

        self.stackMemorySpace = LIMITS["STACK_SIZE"]
        self.localsStack = Stack()
        self.temporalsStack = Stack()
        self.listsStack = Stack()

        self.params = Stack()
        self.returnPointers = Stack()

    def __str__(self):
        return "MemoryManager(\n{}\n)".format(pprint.pformat(self.memory))

    def stackMemoryCheck(self, message):
        if self.stackMemorySpace <= 0:
            raise Exception(message)

    def getContextSize(self):
        return len(list(self.memory["local"].keys())) + len(list(self.memory["temporal"].keys())) + len(list(self.memory["list"].keys()))

    def getMemorySegment(self, address):
        memorySegment = None

        if address >= LIMITS["GLOBAL_LIM_L"] and address < LIMITS["GLOBAL_LIM_R"]:
            memorySegment = self.memory["global"]

        elif address >= LIMITS["LOCAL_LIM_L"] and address < LIMITS["LOCAL_LIM_R"]:
            memorySegment = self.memory["local"]

        elif address >= LIMITS["TEMPORAL_LIM_L"] and address < LIMITS["TEMPORAL_LIM_R"]:
            memorySegment = self.memory["temporal"]

        elif address >= LIMITS["LIST_LIM_L"] and address < LIMITS["LIST_LIM_R"]:
            memorySegment = self.memory["list"]

        return memorySegment

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
            return memory
        except:
            raise Exception(
                "Tried to access non existing memory at address {}".format(address))

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

        self.memory["local"] = {}
        self.memory["temporal"] = {}
        self.memory["list"] = {}

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
            for _ in range(size - 1):
                paramsList.append(self.params.pop())
            self.stackMemorySpace += size
        except:
            raise Exception("Invalid stack call")
        return paramsList

    def pushParams(self, paramsList):
        self.stackMemorySpace -= len(paramsList)
        self.stackMemoryCheck("Memory limit excedeed, Stack Overflow")

        for param in paramsList:
            self.params.push(param)
