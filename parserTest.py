import os
from VECING_Parser import LanguageParser
from VECING_Lexer import LanguageLexer


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
        parser.parse(LanguageLexer().tokenize(data))
        print("Apropiado")
        print("No errors found in file {}".format(fileName))
        if showSymbols:
            print('\n{}\n'.format(parser.symbols))
        if showProgramTree:
            print(parser.programTree, '\n')
        if showCuads:
            cuads = parser.getCuads()
            print('\n'.join('{}: {}'.format(k[0] + 1, k[1]) for k in enumerate(cuads)))
    except Exception as e:
        print("File {} has error".format(fileName))
        print(e)
    print('\n')


print('\n')
parseFile('tests/test3.vg', showTokens=False, showSymbols=True, showProgramTree=True, showCuads=True)
