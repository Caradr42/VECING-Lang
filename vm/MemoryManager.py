from consts import LIMITS
import pprint
import Stack

class MemoryManager():
    def __init__(self):
        self.memory = {
            'global': {},
            'local': {},
            'temporal': {}
        }

        self.localsStack = Stack()
        self.temporalsStack = Stack()

    def __str__(self):
        return "MemoryManager(\n{}\n)".format(pprint.pformat(self.memory))

    def getMemorySegment(self, address):
        memorySegment = None

        if address >= LIMITS["GLOBAL_LIM_L"] and address < LIMITS["GLOBAL_LIM_R"]
            memorySegment = self.memory["global"]

        elif address >= LIMITS["LOCAL_LIM_L"] and address < LIMITS["LOCAL_LIM_R"]
            memorySegment = self.memory["local"]
        
        elif address >= LIMITS["TEMPORAL_LIM_L"] and address < LIMITS["TEMPORAL_LIM_R"]
            memorySegment = self.memory["temporal"]
            
        return memorySegment

    def setValue(self, address, value):
        memorySegment = getMemorySegment(address)
        if memorySegment == None:
            raise Exception("Invalid memmory address set of {} at address {}".format(value, address))
        
        memorySegment[address] = value

    def getValue(self, address):
        memorySegment = getMemorySegment(address)
        if memorySegment == None:
            raise Exception("Invalid access to memmory address at {}".format(address))

        try:
            memory = memorySegment[address]:
            return memory
        except:
            raise Exception("Tried to access non existing memory at address {}".format(address))

    def popContext():
        try:
            self.memory["local"] = self.localsStack.pop()
            self.memory["temporal"] = self.temporalsStack.pop()
        except:
            raise Exception("Invalid context change, alredy at global context")
    
    def pushContext():
        self.localsStack.push(self.memory["local"])  
        self.temporalsStack.push(self.memory["temporal"]) 

        self.memory["local"] = {}
        self.memory["temporal"] = {}