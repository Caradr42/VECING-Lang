from compiler.VECING_Lexer import LanguageLexer

#"(1 2 3 4.5)"
#"(2 3.4)"
def parseFile():
    """ lets the user input a fileName. The contents of the file are passed to the Lexer for a 
        quick test. The resulting tokenization is then printed
    """
    lexer = LanguageLexer()
    data = input('Enter a string: ')
    try:
        result = lexer.tokenize(data)

        for tok in result:
            print('type=%r, value=%r' % (tok.type, tok.value))

    except Exception as e:
        print(e)
    print('\n')

parseFile()
