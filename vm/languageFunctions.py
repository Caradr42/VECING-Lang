
def add(memoryManager, paramsList):
    def addPair(a , b):
        if a is None or b is None:
            return None
        if type(a) is not float or type(b) is not float:
            raise Exception("Cannot add anidated lists")
        return a + b

    A = paramsList[0]
    B = paramsList[1]

    if type(A) != type(B):
        raise Exception("Cannot add elements of different types")
    
    if type(A) == float:
        return addPair(A, B)

    lenghtA = len(A)
    lengthB = len(B)
    if lenghtA != lengthB:
        raise Exception("cannot add list of different dimensions: {} <> {}".format(lenghtA, lengthB))

    result = []
    for i in range(lenghtA):
        result.append(addPair(A[i], B[i]))
    return result
    

def sub(memoryManager, paramsList):
    def subPair(a , b):
        if a is None or b is None:
            return None
        if type(a) is not float or type(b) is not float:
            raise Exception("Cannot subtract anidated lists")
        return a - b

    A = paramsList[0]
    B = paramsList[1]

    if type(A) != type(B):
        raise Exception("Cannot add elements of different types")
    
    if type(A) == float:
        return subPair(A, B)

    lenghtA = len(A)
    lengthB = len(B)
    if lenghtA != lengthB:
        raise Exception("cannot subtract lists of different dimensions: {} <> {}".format(lenghtA, lengthB))

    result = []
    
    for i in range(lenghtA):
        result.append(subPair(A[i], B[i]))
    return result

def printList(memoryManager, paramsList):
    A = paramsList[0]
    
    if type(A) is not tuple:
        print(A)
    else:
        for e in A:
            print(e, end =" ")
        print("")