import operator
import math

def isEmptyList(paramsList):
    return  paramsList == None or len(paramsList) == 0 or (len(paramsList) == 1 and paramsList[0] == None)

def handleEmpty(paramsList, operationName='handle'):
    if isEmptyList(paramsList):
        raise Exception("cannot {} empty list".format(operationName))

def binaryFunctionGenerator(op, operationName):
    def binaryFunction(memoryManager, paramsList):
        def binaryOperation(a , b):
            if a is None or b is None:
                return None
            if type(a) is not float or type(b) is not float:
                raise Exception("Cannot {} nested lists".format(operationName))
            return op(a, b)
        
        handleEmpty(paramsList, operationName)
        A = paramsList[0]
        B = paramsList[1]

        if type(A) != type(B):
            raise Exception("Cannot {} elements of different shapes".format(operationName))
        
        if type(A) == float:
            return binaryOperation(A, B)

        lengthA = len(A)
        lengthB = len(B)
        if lengthA != lengthB:
            raise Exception("cannot {} list of different dimensions: {} <> {}".format(operationName, lengthA, lengthB))

        result = []
        for i in range(lengthA):
            result.append(binaryOperation(A[i], B[i]))
        return result

    return binaryFunction

def unaryFunctionGenerator(op, operationName):
    def unaryFunction(memoryManager, paramsList):
        def unaryOperation(a):
            if a is None:
                return None
            if type(a) is not float:
                raise Exception("Cannot {} nested list".format(operationName))
            return op(a)

        handleEmpty(paramsList, operationName)
        A = paramsList[0]
        
        if type(A) == float:
            return unaryOperation(A)

        lengthA = len(A)

        result = []
        for i in range(lengthA):
            result.append(unaryOperation(A[i]))
        return result

    return unaryFunction

#[(((16.0, None), ((17.0, None), ((18.0, None), None))), None)]
#[((16.0, 17.0, 18.0),)]

def flattenPythonList(pythonList):
    if isEmptyList(pythonList):
        return []

    def flattenHelper(lista):
        if type(lista) is not tuple:
            raise Exception("Error in parameter list representation")

        izq = lista[0]
        der = lista[1]
        
        if type(izq) is float: #no need to check right because constants always have None right
            return izq 
        
        if type(izq[0]) is float: #check left depth
            izqResult = izq[0]
        else:
            izqResult = flattenHelper(izq)

            # if type(izq[0][0]) is float and der is None and izq[1] is None:
            #     return (izqResult, )
            if der is None and izq[1] is None:
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
        # elif type(tupleList[0]) is tuple and type(tupleList[0][0]) is tuple and tupleList[1] is None:
        #     temp = (flattenHelper(tupleList), )
        else:
            temp = flattenHelper(tupleList)

        if type(temp) is float:
            temp = (temp,)
        elif len(temp) == 1:
            temp = (temp, )
        # elif  type(temp[0]) is tuple and type(temp[0][0]) is tuple and temp[1] is None:
        #     temp (temp, )
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
    if isEmptyList(paramsList):
        return [1.0]
    A = paramsList[0]
    if validateList(A):
        return [0.0] if len(A) <= 1  else [1.0]
    return [0.0]

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

#true if list of format (1.2,)
def single(memoryManager, paramsList):
    if isEmptyList(paramsList):
        return [0.0]
    A = paramsList[0]
    if type(A) == float:
        return [1.0]
    if len(A) == 1 and type(A[0]) == float:
        return [1.0]
    return [0.0]

def car(memoryManager, paramsList):
    handleEmpty(paramsList, "car")
    #print("paramsList car: ", paramsList)
    A = paramsList[0]
    if not validateList(A):
        raise Exception('Tried to get car of non-list element')
    return [A[0]]

def cdr(memoryManager, paramsList):
    handleEmpty(paramsList, "cdr")
    #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #print("paramsList cdr: ", paramsList)
    A = paramsList[0]
    if not validateList(A):
        raise Exception('Tried to get cdr of non-list element')
    if len(A) == 1:
        return []
    # if len(A) == 1:
    #     return [(A[1:],])
        #raise Exception('Tried to apply cdr in single element list')
    return [A[1:]]
    
def empty(memoryManager, paramsList):
    if isEmptyList(paramsList):
        return [1.0]
    A = paramsList[0]
    if validateList(A) and A[0] == None:
        return [1.0]
    return [float(len(A) == 0)]

def elemCount(memoryManager, paramsList):
    handleEmpty(paramsList, "count elements of")
    head = paramsList[0]
    
    if not validateList(head):
        raise Exception('Tried to get element count of non-list')
    
    def countHelper(head):
        if head == None:
            return 0

        if type(head) == float:
            return 1
        elif (validateList(head)):
            acum = 0
            for e in head:
                acum += countHelper(e)
            return acum
        return 0

    size = countHelper(head)
    return [float(size)]

def length(memoryManager, paramsList):
    handleEmpty(paramsList, "cannot get length of")
    head = paramsList[0]

    if not validateList(head):
        raise Exception('Tried to get length  of non-list')
    # if type(head) == float:
    #     return [1.0]

    return [float(len(head))]


def printList(memoryManager, paramsList):
    if isEmptyList(paramsList):
        print(paramsList)
        return paramsList

    A = paramsList[0]
    
    print("> ", A)
    return A
    # if type(A) is not tuple:
    #     print("> ", A)
    #     return A
    # else:
    #     print(">", end =" ")
    #     for e in A:
    #         print(e, end =" ")
    #     print("")
    #     return A