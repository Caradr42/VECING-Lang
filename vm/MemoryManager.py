import consts

class MemoryManager():
    def __init__(self):
        self.memory = {
            'global': {},
            'local': {},
            'temporal': {},
            'pointers': {}
        }



    def setValue(self, address, value):
        pass