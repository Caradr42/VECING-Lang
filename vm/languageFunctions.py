
def add(memoryManager, paramsList):
    def addPair(a , b):
        if type(a) is not float or type(b) is not float:
            raise Exception("Cannot add anidated lists")
        return a + b

    A = paramsList[0]
    B = paramsList[1]

    lenghtA = len(A)
    lengthB = len(B)
    if lenghtA != lengthB:
        raise Exception("cannot add list of different dimensions: {} <> {}".format(lenghtA, lengthB))

    result = []
    for i in range(lenghtA):
        result.append(addPair(A[i], B[i])
    return result
    

def sub(memoryManager, paramsList):
    def addPair(a , b):
        if type(a) is not float or type(b) is not float:
            raise Exception("Cannot add anidated lists")
        return a - b

    A = paramsList[0]
    B = paramsList[1]

    lenghtA = len(A)
    lengthB = len(B)
    if lenghtA != lengthB:
        raise Exception("cannot add list of different dimensions: {} <> {}".format(lenghtA, lengthB))

    result = []
    for i in range(lenghtA):
        result.append(addPair(A[i], B[i])
    return result