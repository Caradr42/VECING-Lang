# stack (lifo)
from collections import deque
class Stack():
    def __init__(self):
        self.elems = deque()

    def __str__(self):
         return "stack({})".format(list(self.elems)[::-1])
        
    def push(self, elem):
        self.elems.append(elem)

    def pop(self):
        return self.elems.pop()

    def size(self):
        return len(self.elems)

    def isEmpty(self):
        return len(self.elems) == 0

    def top(self):
        return self.elems[-1]

    def clear(self):
        self.elems.clear()