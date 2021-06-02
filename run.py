import sys
import re
import os

if __name__ == '__main__':
    """ Gets a name of a file along some optional flags for the compiler,
        it calls the compiler in the given fileName, and calls the virtual machine
        to run the intermediate code generated.
        This section of the code is used can be used manually in the terminal,
        and it is also use in our bash script run.sh.
    """
    argumentsInString = ' '.join(sys.argv[1:])
    regex = r'(.*[\\\/])*'
    fileName = sys.argv[1]
    fileNameShort = re.sub(regex, '',fileName)

    os.system('python compile.py {}'.format(argumentsInString)) 
    os.chdir('vm')
    os.system('python VENCING_VM.py ../{}'.format(fileNameShort[0 : -2] + 'o')) 
    os.chdir('..')
