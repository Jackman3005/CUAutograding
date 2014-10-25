import re
from pypeg2 import * #parser
import pypeg2
import CppHeaderParser #sudo pip3 install cppheaderparser, also: sudo pip3 install install ply

def getAllNumbersFromString(stringToParse):
    listOfNumbersAsStrings = re.findall("([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)",stringToParse)
    
    listOfNumbers = []
    for string in listOfNumbersAsStrings:
        if(not isinstance(string, str)):
            string = string[0]
        try:
            if (len(string) > 1 and string[0] != '0' and string[1] != '.'):
                string = string.lstrip('0')
            listOfNumbers.append(eval(string))
        except ValueError:
            None
    return listOfNumbers
    
def CppFunctionFinder (cppSourceFileName):
    with open (cppSourceFileName, "r") as myfile:
        data=myfile.read()
        
    try:
        cppHeader = CppHeaderParser.CppHeader(cppSourceFileName)
    except CppHeaderParser.CppParseError as e:
        print(e)
        sys.exit(1)

    numFunctions = len(cppHeader.functions)
    print('Number of functions :', numFunctions)
    
    nameFunctions = []
    for i in range(0, len(cppHeader.functions)):
        nameFunctions.append(cppHeader.functions[i]['name'])
    
    print('The names of the functions: ', nameFunctions) 

