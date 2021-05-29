import sys
import re
import os

if __name__ == '__main__':

    argumentsInString = ' '.join(sys.argv[1:])
    regex = r'(.*[\\\/])*'
    fileName = sys.argv[1]
    fileNameShort = re.sub(regex, '',fileName)

    os.system('python compile.py {}'.format(argumentsInString)) 
    os.chdir('vm')
    os.system('python VENCING_VM.py ../{}'.format(fileNameShort[0 : -2] + 'o')) 
    os.chdir('..')
