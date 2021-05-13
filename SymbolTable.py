import copy
import pprint
varTable = 'varTable'


class SymbolTable:
    currentContext = None

    def __init__(self):
        self.dict = {}
        self.child = None
        self.parent = None
        SymbolTable.currentContext = self

    def addSymbol(self, name, symbolType, funcExtras=None):
        if(self.child == None):
            if(symbolType == "func" or symbolType == "lambda"):
                newTable = SymbolTable()
                newTable.parent = self
                self.child = newTable
                self.dict[name] = {"type": symbolType, "funcExtras": funcExtras, varTable: newTable,}
            else:
                self.dict[name] = {"type": symbolType}
        else:
            self.child.addSymbol(name, symbolType)

    def isSymbolInContext(self, symbol):
        if ( symbol in list(self.dict.keys()) ):
            return True
        elif self.parent:
            return self.parent.isSymbolInContext(symbol)
        return False    
    
    def getFunctionSymbol(self, symbol):
        if ( symbol in list(self.dict.keys()) and self.dict[symbol]["type"] == "func"):
            return self.dict[symbol]
        return None

    def pop(self):
        if (self.child == None):
            return 
        SymbolTable.currentContext = SymbolTable.currentContext.parent
        SymbolTable.currentContext.child = None

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
