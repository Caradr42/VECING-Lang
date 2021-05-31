import operator
import math

def handleEmpty(paramsList, operationName='handle'):
    if len(paramsList) == 0 or paramsList == None or paramsList[0] == None:
        raise Exception("cannot {} empty list".format(operationName))

def binaryFunctionGenerator(op, operationName):
    def binaryFunction(memoryManager, paramsList):
        def binaryOperation(a , b):
            if a is None or b is None:
                return None
            if type(a) is not float or type(b) is not float:
                raise Exception("Cannot {} anidated lists".format(operationName))
            return op(a, b)
        
        handleEmpty(paramsList, operationName)
        A = paramsList[0]
        B = paramsList[1]

        if type(A) != type(B):
            raise Exception("Cannot {} elements of different types".format(operationName))
        
        if type(A) == float:
            return binaryOperation(A, B)

        lenghtA = len(A)
        lengthB = len(B)
        if lenghtA != lengthB:
            raise Exception("cannot {} list of different dimensions: {} <> {}".format(operationName, lenghtA, lengthB))

        result = []
        for i in range(lenghtA):
            result.append(binaryOperation(A[i], B[i]))
        return result

    return binaryFunction

def unaryFunctionGenerator(op, operationName):
    def unaryFunction(memoryManager, paramsList):
        def unaryOperation(a):
            if a is None:
                return None
            if type(a) is not float:
                raise Exception("Cannot {} anidated list".format(operationName))
            return op(a)

        handleEmpty(paramsList, operationName)
        A = paramsList[0]
        
        if type(A) == float:
            return unaryOperation(A)

        lenghtA = len(A)

        result = []
        for i in range(lenghtA):
            result.append(unaryOperation(A[i]))
        return result

    return unaryFunction

def flattenPythonList(pythonList):
    if pythonList == None or len(pythonList) == 0 or (len(pythonList) == 1 and pythonList[0] == None):
        return []

    def flattenHelper(lista):
        if type(lista) is not tuple:
            raise Exception("not handled")

        izq = lista[0]
        der = lista[1]
        
        if type(izq) is float: #no need to check right because constants always have None right
            return izq 
        
        if type(izq[0]) is float: #check left depth
            izqResult = izq[0]
        else:
            izqResult = flattenHelper(izq)

            if type(izq[0][0]) is float and der is None and izq[1] is None:
                return (izqResult, )

        if der is None:
            return izqResult

        temp = []
        if  der[1] is not None:
            temp.append(izqResult)
            derResult = flattenHelper(der)
            temp = temp + list(derResult)
        else:
            temp.append(izqResult)
            derResult = flattenHelper(der)
            temp.append(derResult)
        return tuple(temp)
        
    elems = []
    for tupleList in pythonList:
        if type(tupleList) == float:
            return elems.append(tupleList)
    
        temp = flattenHelper(tupleList)
        if type(temp) is float:
            temp = (temp,)
        elif len(temp) == 1:
            temp = (temp, )
        elems.append(temp)
    return elems
    
#Math operations
add = binaryFunctionGenerator(operator.add, 'add')
sub = binaryFunctionGenerator(operator.sub, 'subtract')
power = binaryFunctionGenerator(operator.pow, 'get power of')
mult = binaryFunctionGenerator(operator.mul, 'multiply')
div = binaryFunctionGenerator(operator.truediv, 'divide')

sqrt = unaryFunctionGenerator(math.sqrt, 'get square root of')
absop = unaryFunctionGenerator(operator.abs, 'get absolute value of')

#Logical operators 
andOp = binaryFunctionGenerator(lambda x, y: 1.0 if x != 0.0 and y != 0.0 else 0.0, 'evaluate logical AND of')
orOp = binaryFunctionGenerator(lambda x, y: 1.0 if x != 0.0 or y != 0.0 else 0.0, 'evaluate logical OR of')

notOp = unaryFunctionGenerator(lambda x: 1.0 if x == 0.0 else 0.0, 'cannot evaluate logical NOT of')

#Relational operators
biggerequal = binaryFunctionGenerator(lambda x, y: 1.0 if x >= y else 0.0, 'evaluate >= of')
lessrequal = binaryFunctionGenerator(lambda x, y: 1.0 if x <= y else 0.0, 'evaluate <= of')
bigger = binaryFunctionGenerator(lambda x, y: 1.0 if x > y else 0.0, 'evaluate >= of')
less = binaryFunctionGenerator(lambda x, y: 1.0 if x < y else 0.0, 'evaluate < of')
notqueal = binaryFunctionGenerator(lambda x, y: 1.0 if x != y else 0.0, 'evaluate != of')
equal = binaryFunctionGenerator(lambda x, y: 1.0 if x == y else 0.0, 'evaluate == of')

#list Access

def validateList(pythonList):
    return type(pythonList) == tuple or type(pythonList) == list

def isList(memoryManager, paramsList):
    handleEmpty(paramsList, "check if list of")
    return [float(validateList(paramsList[0]))]

def append(memoryManager, paramsList):
    handleEmpty(paramsList, "append lists of")
    A = paramsList[0]
    B = paramsList[1]
    if type(A) == float:
        A = [A]
    if type(B) == float:
        B = [B]
    A =list(A)
    B =list(B)
    return A + B

#true if list of format (1.2, None)
def single(memoryManager, paramsList):
    handleEmpty(paramsList, "check if single value of")
    A = paramsList[0]
    if type(A) == float:
        return [1.0]
    if type(A[0]) == float and A[1] == None:
        return [1.0]
    return [0.0]

def car(memoryManager, paramsList):
    handleEmpty(paramsList, "car")
    #print("paramsList car: ", paramsList)
    A = paramsList[0]
    if not validateList(A):
        raise Exception('Tried to get car of non-list element')
    print("result car: ", [A[0]])
    return [A[0]]

def cdr(memoryManager, paramsList):
    handleEmpty(paramsList, "cdr")
    #print("paramsList cdr: ", paramsList)
    A = paramsList[0]
    if not validateList(A):
        raise Exception('Tried to get cdr of non-list element')
    if len(A) == 1:
        raise Exception('Tried to apply cdr in single element list')
    print("result cdr: ", [A[1:]])
    return [A[1:]]
    
def empty(memoryManager, paramsList):
    if len(paramsList) == 0:
        return [1.0]
    A = paramsList[0]
    if validateList(A) and A[0] == None:
        return [1.0]
    return [float(len(A) == 0)]

def elemCount(memoryManager, paramsList):
    handleEmpty(paramsList, "count elements of")
    head = paramsList[0]
    size = 0
    
    if not validateList(head):
        raise Exception('Tried to get element count of non-list')
    
    def countHelper(head):
        if (validateList(head)):
            if head == None:
                return
            if single(None, head):
                size += 1
            else:
                countHelper(head[0])
                countHelper(head[1])
    countHelper(head)
    return [size]

def lenght(memoryManager, paramsList):
    handleEmpty(paramsList, "cannot get length of")
    head = paramsList[0]
    size = 0

    if not validateList(head):
        raise Exception('Tried to get lenght of non-list')
    if single(head):
        return [1.0]

    def lenHelper(head):
        if (validateList(head)):
            if head == None:
                return
            if single(head):
                size += 1
            else:
                size += 1
                if(head[1] != None):
                    lenHelper(head[1])
    lenHelper(head)
    return [size]


def printList(memoryManager, paramsList):
    if len(paramsList) == 0 or paramsList == None or paramsList[0] == None:
        print(paramsList)
        return paramsList

    A = paramsList[0]
    
    if type(A) is not tuple:
        print("> ", A)
        return A
    else:
        print("> (", end =" ")
        for e in A:
            print(e, end =" ")
        print(")")
        return A