from compiler.VECING_Lexer import LanguageLexer

#"(1 2 3 4.5)"
#"(2 3.4)"
def parseFile():
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
