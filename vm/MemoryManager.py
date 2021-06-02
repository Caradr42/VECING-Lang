import sys
sys.path.append('../')

import consts
import pprint
from Stack import Stack
from utils import Debugger

debug = Debugger(consts.DEBUG_MODE)

class MemoryManager():
    """ This Class is in charge of managing all the structures necessary for virtual 
        memory storage and administration. It also contains the methods necessary to 
        access and edit the memory in various ways while keeping track of the current 
        context and memory usage 

    attributes
    ----------
    memory: the dictionary of dictinaries that stores the virtual memory separated in 
        multiple memory segments
    stackMemorySpace: tha amount of space available for the stacks, it acounts for 
       all the stacks
    localsStack: The stack for storing the context for the local segment of the memory
    temporalsStack: The stack for storing the context for the temporal segment of the memory
    listsStack: The stack for storing the context for the list segment of the memory
    temporalListsStack: The stack for storing the context for the temporallist segment of the memory
    params: the satch for storing function parameters
    returnPointers: The stack for storing an adress where to store the return of a function, and a 
        function pointer to retunr to at the end of a user function execution.
    functionsTable: a dictionary to store the number of parameters each user function receives

    methods
    -------
    reduceTempPointer(address)
    getPythonlistFromPointer(address)
    flatListToFunctionalList(flatList)
    pythonlistToPointerList(pythonList)
    stackMemoryCheck(message)
    addFunction(functionInstructionPointer, functionParamQty)
    getFunctionParamsCount(functionInstructionPointer)
    getContextSize()
    getMemorySegment(address)
    isAddress(address)
    pointerIsList(address)
    addressIsTemp(address)
    pointerIsConstant(address)
    setValue(address, value)
    getValue(address)
    setTemporalListPair(left, right)
    setListPair(address, left, right)
    getListPair(address)
    popContext()
    pushContext()
    popReturnPointers()
    pushReturnPointers(address, instructionPointer)
    popParams(size)
    pushParams(paramsList)
    """
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
    
    def reduceTempPointer(self, address):
        """ return the pointer at the end of a temp pointer chain

        parameters
        ----------
        address: the adress from were to get the value

        returns
        -------
        address: The value from pointer at the end of a temp pointer chain
        """
        if address is not None and self.addressIsTemp(address):
            return self.getValue(address)
        return address

    def getPythonlistFromPointer(self, address):
        """ obtains the values stored in a list from virtual memory and constructs a 
            python list from it 
            used by instructions.py

        parameters
        ----------
        address: the adress from were to obtain the values from v memory

        returns
        -------
        a funtional list made form nested python touples of the form:
             ((10.0, None), ((11.0, None), ((12.0, None), None)))
        """
        if type(address) == int:
            isListAddress = (address >= consts.LIMITS["LIST_LIM_L"] and address < consts.LIMITS["LIST_LIM_R"]) or (
                address >= consts.LIMITS["TEMPORAL_LIST_LIM_L"] and address < consts.LIMITS["TEMPORAL_LIST_LIM_R"])
 
            if self.addressIsTemp(address):
                address = self.getValue(address)
                return self.getPythonlistFromPointer(address)
            
            if isListAddress:
                debug.print("is list: ", address)
                
                (left, right) = self.getListPair(address)
                left = self.reduceTempPointer(left)
                right = self.reduceTempPointer(right)

                newRight = right
                
                if right is not None and self.pointerIsList(right):
                    (rightleft, rightright) = self.getListPair(right)
                    rightleft = self.reduceTempPointer(rightleft)
                    rightright = self.reduceTempPointer(rightright)

                    if rightleft is not None and self.pointerIsList(rightleft):
                        (rightleftleft, rightleftright) = self.getListPair(rightleft)
                        rightleftleft = self.reduceTempPointer(rightleftleft)
                        rightleftright = self.reduceTempPointer(rightleftright)

                        if rightleftleft is None and rightleftright is None and rightright is not None:
                            newRight = rightright
                        if rightleftleft is None and rightleftright is None:
                            return (self.getPythonlistFromPointer(left), None)
                
                # if left is None and right is not None:
                #     return self.getPythonlistFromPointer(right)
                # elif left is None:
                #     return None
                # if self.pointerIsTemp(left):
                #     left = self.getValue(left)
                # if self.pointerIsTemp(right):
                #     right = self.getValue(right)

                return (self.getPythonlistFromPointer(left), self.getPythonlistFromPointer(newRight))

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

    
    # [(10.0, 11.0, 12.0)]
    # (((10.0, None), ((11.0, None), ((12.0, None), None))), None)
    # ((10.0, None), ((11.0, None), ((12.0, None), None)))
    
    def flatListToFunctionalList(self, flatList):
        """Receives a list of regular python touples and converts each of them to lists of the 
            same form as returned by getPythonlistFromPointer()
            used by instructions.py

        parameters
        ----------
        flatList: a list of regular python touples

        returns
        -------
        a funtional list made form nested python touples of the form:
             ((10.0, None), ((11.0, None), ((12.0, None), None)))
        """
        if type(flatList) == float:
            return (flatList, None)

        if flatList == None or len(flatList) == 0:
            return flatList
        if len(flatList) == 1 and type(flatList[0]) == float:
            return (flatList[0], None)
        if type(flatList) == tuple:
            flatList = list(flatList)
        flatList.reverse()
        
        inside = flatList[0]
        if type(inside) == tuple and len(inside) == 1 and type(inside[0]) == tuple:
            funcList = (self.flatListToFunctionalList(inside[0]), None)
        elif type(inside) == tuple and len(inside) == 1:
            funcList = (self.flatListToFunctionalList(inside[0]), None)
        elif type(inside) == tuple:
            funcList = self.flatListToFunctionalList(inside)
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
        """Does the oposite as getPythonlistFromPointer(); receives a list of the form:
            [((10.0, None), ((11.0, None), ((12.0, None), None)))]
            and stores it in v memory apropiately, returning the list pointer to it
            used by instructions.py

        parameters
        ----------
        pythonList: a list of the form:
            ((10.0, None), ((11.0, None), ((12.0, None), None)))

        returns
        -------
        the list pointer to the stored list
        """
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
        """Adds a function to the functionsTable using its function Instruction Pointer
            as key, and the number of parameters as value.
            used by instructions.py

        parameters
        ----------
        functionInstructionPointer: the function Instruction Pointer of the function to add
        functionParamQty: the number of parameters as value of the function to add
        """
        self.functionsTable[functionInstructionPointer] = functionParamQty

    def getFunctionParamsCount(self, functionInstructionPointer):
        """returns the number of parameters of a registered function by using its function 
            Instruction Pointer
            used by instructions.py

        parameters
        ----------
        functionInstructionPointer: the function Instruction Pointer of the function we want 
            the number of parameters from

        returns
        -------
        the number of parameters of a registered function
        """
        try:
            paramCount = self.functionsTable[functionInstructionPointer]
            return paramCount
        except:
            raise Exception("Tried to access non registered function in memory")

    def getContextSize(self):
        return len(list(self.memory["local"].keys())) + len(list(self.memory["temporal"].keys())) + len(list(self.memory["list"].keys()))

    def getMemorySegment(self, address):
        memorySegment = None
        if not self.isAddress(address):
            raise Exception("cannot get memory segment from not an address: ", address)

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

    def isAddress(self, address):
        return type(address) == int
    
    def pointerIsList(self, address):
        """returns true if the pointer address belong to the list segment, may rise an
            exception if not sent an address
            used in instructions.py

        parameters
        ----------
        address: the pointer address to check

        returns
        -------
        Boolean True if the pointer address belong to the list segment
        """

        if address is None or type(address) == float:
            raise Exception("Tried to access non pointer as pointer")
        return self.isAddress(address) and ((address >= consts.LIMITS["LIST_LIM_L"] and address < consts.LIMITS["LIST_LIM_R"]) or (address >= consts.LIMITS["TEMPORAL_LIST_LIM_L"] and address < consts.LIMITS["TEMPORAL_LIST_LIM_R"]))

    def addressIsTemp(self, address):
        """returns true if the pointer address belong to the temp segment.
            used in instructions.py

        parameters
        ----------
        address: the pointer address to check

        returns
        -------
        Boolean True if the pointer address belong to the temp segment
        """
        return self.isAddress(address) and address >= consts.LIMITS["TEMPORAL_LIM_L"] and address < consts.LIMITS["TEMPORAL_LIM_R"]


    def pointerIsConstant(self, address):
        """returns true if the pointer address belong to the global segment. may rise an
            exception if not sent an address
            used in instructions.py

        parameters
        ----------
        address: the pointer address to check

        returns
        ------
        boolean True if the pointer address belong to the global segment
        """
        if address is None or type(address) == float:
            raise Exception("Tried to access non pointer as pointer")
        return self.isAddress(address) and address >= consts.LIMITS["GLOBAL_LIM_L"] and address < consts.LIMITS["GLOBAL_LIM_R"]

    def setValue(self, address, value):
        """sets some addresses value in the v memory

        parameters
        ----------
        address: the address were to store tha value
        value: the value to store
        """
        memorySegment = self.getMemorySegment(address)
        if memorySegment == None:
            raise Exception(
                "Invalid memmory address set of {} at address {}".format(value, address))

        memorySegment[address] = value

    def getValue(self, address):
        """returns the stored value of an address
            used in instructions.py

        parameters
        ----------
        address: the address from were the value is wanted

        returns
        ------
        the stored value of the address
        """
        memorySegment = self.getMemorySegment(address)
        if memorySegment == None:
            raise Exception(
                "Invalid access to memory  address at {}".format(address))

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
        """similar ot setValue() but for list pairs. sets values for both left and 
            right of the list
            used in instructions.py

        parameters
        ----------
        address: the address were to store tha value
        left: the left value to store
        right: the right value to store
        """
        self.setValue(address, left)
        self.setValue(address + 1, right)

    def getListPair(self, address):
        """similar ot getValue() but for list pairs. returns both left and 
            right values from the list
            used in instructions.py

        parameters
        ----------
        address: the address from were the value is wanted

        returns
        ------
        left: the left value from the list
        right: the right value from the list
        """
        left = self.getValue(address)
        right = self.getValue(address + 1)
        return (left, right)

    def popContext(self):
        """ goes back to the previous context by restoring the previous stack memory from the 
            stacks 
            used in instructions.py
        """
        try:
            self.memory["local"] = self.localsStack.pop()
            self.memory["temporal"] = self.temporalsStack.pop()
            self.memory["list"] = self.listsStack.pop()
            self.memory["temporalList"] = self.temporalListsStack.pop()

            contextSize = self.getContextSize()

            self.stackMemorySpace += contextSize

        except:
            raise Exception("Invalid context change, already  at global context")

    def pushContext(self):
        """ goes into a new context by storing the current memory in the 
            stacks and eliminating the current memory
            used in instructions.py
        """
        contextSize = self.getContextSize()

        self.stackMemorySpace -= contextSize
        self.stackMemoryCheck("Memory limit exceeded, Stack Overflow")

        self.localsStack.push(self.memory["local"])
        self.temporalsStack.push(self.memory["temporal"])
        self.listsStack.push(self.memory["list"])
        self.temporalListsStack.push(self.memory["temporalList"])

        self.memory["local"] = {}
        self.memory["temporal"] = {}
        self.memory["list"] = {}
        self.memory["temporalList"] = {}

    def popReturnPointers(self):
        """ Used at the end of a user function execution for retrieving the function 
            pointer were the vm execution needs to return to, and the address were to 
            store the result of the function
            used in instructions.py

            returns
            -------
            addressInstpointerPair: the function pointer were the vm execution needs to return to, and the address were to store the result of the function
        """
        self.stackMemorySpace += 2
        try:
            addressInstpointerPair = self.returnPointers.pop()
            return addressInstpointerPair
        except:
            raise Exception("Invalid stack call")

    def pushReturnPointers(self, address, instructionPointer):
        """ Used at the beggining of a user function execution for pushing the function 
            pointer were the vm execution needs to return to, and the address were to 
            store the result at the en of the function execution, later to retrieve them
            used in instructions.py

            parameters
            ----------
            address: address were to store the result of the function
            instructionPointer: the function pointer were the vm execution needs to 
                return to
        """
        self.stackMemorySpace -= 2
        self.stackMemoryCheck("Memory limit exceeded, Stack Overflow")
        return self.returnPointers.push((address, instructionPointer))

    def popParams(self, size):
        """ Used at the beggining of a function call for retrieving the function 
            parameters in a list
            used in instructions.py

            parameters
            ----------
            size: the number of parameters to pop from the stack
            
            returns
            -------
            paramsList: the function parameters
        """
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
        """ Used at the params quad instruction for pushing the function 
            parameters into the stack
            used in instructions.py

            parameters
            ----------
            paramsList: the function parameters to push
        """
        self.stackMemorySpace -= len(paramsList)
        self.stackMemoryCheck("Memory limit exceeded, Stack Overflow")

        for param in paramsList:
            self.params.push(param)
