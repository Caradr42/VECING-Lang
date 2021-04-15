import copy
import pprint
varTable = 'varTable'


class SymbolTable:
    def __init__(self):
        self.dict = {}
        self.context = None

    def addSymbol(self, name, symbolType):
        if(self.context == None):
            if(symbolType == "func" or symbolType == "lambda"):
                newTable = SymbolTable()
                self.dict[name] = {"type": symbolType, varTable: newTable}
                self.context = newTable
            else:
                self.dict[name] = {"type": symbolType}
        else:
            self.context.addSymbol(name, symbolType)

    def pop(self):
        if(self.context != None and self.context.context == None):
            self.context = None
        else:
            self.context.pop()

    def getFullDict(self):
        temp = copy.copy(self)

        for key in temp.dict:
            if temp.dict[key]['type'] == 'func' or temp.dict[key]['type'] == 'lambda':
                childDict = temp.dict[key][varTable].getFullDict()
                temp.dict[key][varTable] = childDict

        return temp.dict

    def __str__(self):
        dictt = self.getFullDict()
        return "SymbolTable(\n{}\n)".format(pprint.pformat(dictt))

# myTable = SymbolTable()
# myTable.addSymbol("vect", "vector")
# myTable.addSymbol("obtain", "func")
# myTable.addSymbol("param1", "argument")
# myTable.addSymbol("param2", "argument")
# myTable.addSymbol("lambda1", "lambda")
# myTable.addSymbol("lambda2", "lambda")
# myTable.addSymbol("row", "argumento")
# myTable.pop()
# myTable.addSymbol("mat", "argumento")
# print(myTable)
