import os
import sys
import re
import traceback
from compiler.VECING_Parser import LanguageParser
from compiler.VECING_Lexer import LanguageLexer

def getRelativePath(relPath):
    currDir = os.path.dirname(__file__)
    return os.path.join(currDir, relPath)


def parseFile(fileName, showTokens=False, showSymbols=False, showProgramTree=False, showCuads=False):
    lexer = LanguageLexer()
    parser = LanguageParser()

    with open(getRelativePath(fileName), 'r') as file:
        data = file.read()
    lexerData = lexer.tokenize(data)

    if showTokens:
        try:
            for tok in lexerData:
                print('type=%r, value=%r' % (tok.type, tok.value))
        except Exception as e:
            print(e)

    try:
        lexed = LanguageLexer().tokenize(data)
        if showSymbols:
            print('\n{}\n'.format(parser.symbols))

        parser.parse(lexed)
        if showProgramTree:
            print(parser.programTree, '\n')
            
        cuads = parser.getCuads()
        if showCuads:
            print('\n'.join('{}: {}'.format(k[0] + 1, k[1]) for k in enumerate(cuads)))
            
        print("No errors found in file {}".format(fileName))

        regex = r'(.*[\\\/])*'

        fileName = re.sub(regex, '',fileName)
        print(fileName)
        path = fileName[0 : -2]
        path += "o"

        if os.path.exists(path):
            os.remove(path)

        output = open(path, 'w')
        for cuad in cuads:
            output.write("{} {} {} {}\r".format(cuad[0], cuad[1], cuad[2], cuad[3]))

    except Exception as e:
        print("File {} has error".format(fileName))
        print(e)
        traceback.print_exc()
    print('\n')

if __name__ == '__main__':
      
    flags = {
        "-v": False,
        "-t": False,
        "-s": False,
        "-e": False,
        "-c": False,
    }

    if(len(sys.argv) < 2):
        raise Exception("Missing file name")

    fileName = sys.argv[1]

    regex = r'.*\.vg$'
    if not re.match(regex, fileName):
        raise Exception("Invalid extension")
    
    if not os.path.exists(fileName):
        raise Exception("File does not exist")

    try:
        file = open(fileName, 'r')
    except:
        raise Exception('File {} not found'.format(fileName))

    for i in range(2, len(sys.argv)):
        arg = sys.argv[i]
        if arg in list(flags.keys()):
            flags[arg] = True
        
    print('\n')
    
    parseFile(fileName, showTokens=flags["-t"], showSymbols=flags["-s"], showProgramTree=flags["-e"], showCuads=flags["-c"])

