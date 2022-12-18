import sys
from Functions import *

if __name__ == '__main__':
    argParser = ArgParser()
    arguments = argParser.parse_args(sys.argv[1:])

    data = Parse(arguments.startDate, arguments.currency)
    SaveData(data, arguments.outputFile, arguments.format)
