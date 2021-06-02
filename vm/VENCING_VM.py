import sys
sys.path.append('../libs/graphics')
from Instructions import instructions
import re
from graphics import *

instructionPointer = 1


def readFile(fileName):
    """ Checks if the given fileName has the required extension of the intermediate code
        and opens the file, else it raises an error. It is only used in this same file when
        it gets called from the command line.

    parameters
    ----------
    fileName: the name of the file to open

    returns
    -------
    file: The opened file
    """
    regex = r'.*\.o$'
    if not re.match(regex, fileName):
        raise Exception("Invalid extension")
    if not os.path.exists(fileName):
        raise Exception("File does not exist")
    try:
        file = open(fileName, 'r')
    except:
        raise Exception('Can not open file {}'.format(fileName))
    return file


def getQuadsFromFile(file):
    """ Gets the content of a file that must containt quads. It is only used in this same file when
        it gets called from the command line.

    parameters
    ----------
    file: An opened file with content

    returns
    -------
    quads: The formatted quads gotten from the file
    """
    lines = file.readlines()
    file.close()
    lines = list(map(lambda string: string[0:-1], lines))
    quads = list(map(lambda string: string.split(' '), lines))
    return quads


def parseQuads(quads):
    """ Modifies the quads to provide an easy use later on, it casts evert float value to a 
        real float instead of having a string that appears to be a float, and also casts every virtual address
        number to an integer value. It is only used in this same file when
        it gets called from the command line.

    parameters
    ----------
    quads: the quads before being modified

    returns
    -------
    quads: the quads after being modified

    """
    floatRegex = r'-?\d*\.\d*'
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
    """ Each iteration of the while a quad is obtained from the quads parameter
        and executed used the instruction dictionary of functions. It also updates
        the instructionPointer if needed. It is only used in this same file when
        it gets called from the command line.

    parameters
    ----------
    quads: a list of all the quads to execute
    """
    global instructionPointer
    while instructionPointer - 1 < len(quads):
        quad = quads[instructionPointer - 1]
        instructionName = quad[0]
        nextLine = instructions[instructionName](quad, instructionPointer)

        if nextLine != None:
            instructionPointer = nextLine
        else:
            instructionPointer += 1

# def setInstructionPointer(value):
#     global instructionPointer
#     instructionPointer = value

if __name__ == '__main__':
    """ Gets a name of a file, obtains the quads from the file, and executes them.
    This section of the code can be called from the command line and is not used anywhere else.
    """

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
  
    executeQuads(quads)

