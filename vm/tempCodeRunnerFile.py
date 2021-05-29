def flatListToFunctionalList(flatList):
    if len(flatList) == 0:
        return flatList
    if len(flatList) == 1:
        return (flatList[0], None)
        
    flatList.reverse()
    funcList = ((flatList[0], None), None)
    
    for e in flatList[1:]:
        funcList = ((e, None), funcList)
    return funcList

print(flatListToFunctionalList([]))