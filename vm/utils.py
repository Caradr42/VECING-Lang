""" This class basically provides a switch for printing in console.

    attributes
    ----------
    debugMode: Boolean value that states whether or not a print must happen

    methods
    -------
    print(*args)
    """
class Debugger:
    def __init__(self, debugMode):
        self.debugMode = debugMode

    def print(self, *args):
        """ Prints all the arguments if debugMode is true. This class is used in
            Instructions and MemoryManager.

        parameters
        ----------
        *args: a python list of arbitrary length where all the parameters sent to this function go

        returns
        -------
        None
        """
        if self.debugMode:
            print(*args)