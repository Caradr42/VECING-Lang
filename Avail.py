class Avail:
    def __init__(self):
        self.dict = {}
        self.nextCount = 0

    def addNext(self, value):
        self.dict[self.nextCount] = value
        self.nextCount +=1

    def getValue(self, dir=self.nextCount - 1):
        return self.dict[dir]