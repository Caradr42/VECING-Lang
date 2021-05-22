import sys
sys.path.append('./libs/graphics')

from graphics import *
from Instructions import instructions
import re

instructionPointer = 1

# def main():
#     # win = GraphWin("Some window", 500, 500)
#     # win.setBackground(color_rgb(255, 0, 0)) 
#     # win.getMouse()
#     # win.close()

def readFile(fileName):
    regex = r'.*\.o$'
    if not re.match(regex, fileName):
        raise Exception("Invalid extension")
    if not os.path.exists(fileName):
        raise Exception("File does not exist")
    try:
        file = open(fileName, 'r')
    except:
        raise Exception('File {} not found'.format(fileName))
    return file

def getQuadsFromFile(file):
    lines = file.readlines()
    file.close()
    lines = list(map(lambda string: string[0:-1], lines))
    quads = list(map(lambda string: string.split(' '), lines))
    return quads

def parseQuads(quads):
    floatRegex  = r'-?\d*\.\d*'
    addressRegex = r'\d*'

    for q in range(0, len(quads)):
        for i in range(1, 4):
            if quads[q][i] == "None":
                quads[q][i] = None
            elif re.fullmatch(floatRegex, quads[q][i]):
                quads[q][i] = float(quads[q][i])
            elif re.fullmatch(addressRegex, quads[q][i]):
                quads[q][i] = int(quads[q][i])
    return quads

def executeQuads(quads):
    global instructionPointer
    while instructionPointer - 1 < len(quads):
        quad = quads[instructionPointer - 1]
        instructionName = quad[0]
        nextLine = instructions[instructionName](quad, instructionPointer)

        if nextLine != None:
            instructionPointer = nextLine
        else:
            instructionPointer += 1

if __name__ == '__main__':
    
    flags = {
        "-v": False
    }

    if(len(sys.argv) < 2):
        raise Exception("Missing file name")
    fileName = sys.argv[1]

    file = readFile(fileName)

    for i in range(2, len(sys.argv)):
        arg = sys.argv[i]
        if arg in list(flags.keys()):
            flags[arg] = True
    
    quads = parseQuads(getQuadsFromFile(file))
    print(quads)
    executeQuads(quads)
