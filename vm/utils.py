class Debugger:
    def __init__(self, debugMode):
        self.debugMode = debugMode

    def print(self, *args):
        if self.debugMode:
            print(*args)