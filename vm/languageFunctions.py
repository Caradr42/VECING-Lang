import operator
import math

def binaryFunctionGenerator(op, operationName):
    def binaryFunction(memoryManager, paramsList):
        def binaryOperation(a , b):
            if a is None or b is None:
                return None
            if type(a) is not float or type(b) is not float:
                raise Exception("Cannot {} anidated lists".format(operationName))
            return op(a, b)

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
    if len(pythonList) == 0:
        return []
    if pythonList == None or (len(pythonList) == 1 and pythonList[0] == None):
        return [None]

    def flattenHelper(lista):
        left = lista[0]
        right = lista[1]

        if type(left) == float:
            return [left]

        if not(type(left[0]) == float and left[1] == None):
            raise Exception("Cannot flatten list of depth grater than 1")

        if right is None:
            return [left[0]] 

        return [left[0]] + flattenHelper(right)
    
    elems = []
    for tupleList in pythonList:
        elems.append(tuple(flattenHelper(tupleList)))
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
andOp = binaryFunctionGenerator(lambda x, y: 1.0 if x != 0.0 and y != 0.0 else 0.0, 'evaluate >= of')
orOp = binaryFunctionGenerator(lambda x, y: 1.0 if x != 0.0 or y != 0.0 else 0.0, 'evaluate <= of')

notOp = unaryFunctionGenerator(lambda x: 1.0 if x == 0.0 else 0.0, 'cannot evaluate NOT of')

#Relational operators
biggerequal = binaryFunctionGenerator(lambda x, y: 1.0 if x >= y else 0.0, 'evaluate >= of')
lessrequal = binaryFunctionGenerator(lambda x, y: 1.0 if x <= y else 0.0, 'evaluate <= of')
bigger = binaryFunctionGenerator(lambda x, y: 1.0 if x > y else 0.0, 'evaluate >= of')
less = binaryFunctionGenerator(lambda x, y: 1.0 if x < y else 0.0, 'evaluate < of')
notqueal = binaryFunctionGenerator(lambda x, y: 1.0 if x != y else 0.0, 'evaluate != of')
equal = binaryFunctionGenerator(lambda x, y: 1.0 if x == y else 0.0, 'evaluate == of')


def printList(memoryManager, paramsList):
    A = paramsList[0]
    
    if type(A) is not tuple:
        print("> ", A)
    else:
        print("> ", end =" ")
        for e in A:
            print(e, end =" ")
        print("")