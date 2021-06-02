import copy
import pprint
varTable = 'varTable'


class SymbolTable:
    """ This Class is a structure with the purpose of storing the symbols of the language 
        and those created by the user while keeping track of the contexts were those symbols 
        can be used from. The implementation of the structure works as a tree like graph with 
        biderectional connections between the nodes of the graph such that top down and botton 
        up traverse is posible. 
        This whole class is only used by VECING_Parser.py

    attributes
    ----------
    dict: the dictionary acting as root of the graph
    child: a reference to the child node for the current context we are traversing
    parent: a reference to parent node. If root this is None
    currentContext: A static variable containing the node for the current context 
        we are traversing

    methods
    -------
    addSymbol(name, symbolType, funcExtras=None)
    isSymbolInContext(symbol)
    getFunctionSymbol(symbol)
    pop()
    pop()
    getFullDict()
    __str__()
    """
    currentContext = None

    def __init__(self):
        self.dict = {}
        self.child = None
        self.parent = None
        SymbolTable.currentContext = self

    def addSymbol(self, name, symbolType, funcExtras=None):
        """ adds a symbol to the symbol table at the current context
            This also means that the graph/tree goes down one level to the context of the 
            newly created symbol
            used by VECING_Parser.py

        parameters
        ----------
        name: the name of the symbol
        symbolTypeL: the type of symbol, either function, or lambda
        funcExtras:  dictionary of extra parameters only necessary for function symbols
        """
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
        """ Check if a symbol exists in the current context
            used by VECING_Parser.py

        parameters
        ----------
        symbol: the name of the symbol to check

        returns
        -------
        True or False depending if symbol exists in the current context
        """
        if ( symbol in list(self.dict.keys()) ):
            return True
        elif self.parent:
            return self.parent.isSymbolInContext(symbol)
        return False    
    
    def getFunctionSymbol(self, symbol):
        """ Returns the whole dictionary of a symbol if that symbol is of type function
            used by VECING_Parser.py

        parameters
        ----------
        symbol: the name of the symbol fetch

        returns
        -------
        the whole dictionary of a symbol fetched
        """
        if ( symbol in list(self.dict.keys()) and self.dict[symbol]["type"] == "func"):
            return self.dict[symbol]
        return None

    def pop(self):
        """ pops the context. This means that the graph/tree goes up one level to the context above
            used by VECING_Parser.py

        """
        if (self.child == None):
            return 
        SymbolTable.currentContext = SymbolTable.currentContext.parent
        SymbolTable.currentContext.child = None

    def getFullDict(self):
        """ Returns the whole dictionary of this SymbolTable
            used by VECING_Parser.py

        returns
        -------
        the whole dictionary of this object
        """
        temp = copy.copy(self)

        for key in temp.dict:
            if temp.dict[key]['type'] == 'func' or temp.dict[key]['type'] == 'lambda':
                childDict = temp.dict[key][varTable].getFullDict()
                temp.dict[key][varTable] = childDict

        return temp.dict

    def __str__(self):
        """ prints the Symbol table contents in a more beautiful and understandable way
            used when calling print passing this object.

        """
        dictt = self.getFullDict()
        return "SymbolTable(\n{}\n)".format(pprint.pformat(dictt))
