import re
from pypeg2 import * #parser

#Define 


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
    
    #logic:
    # find 'int','void' 'float',     
    listOfNumbersAsStrings = re.findall("([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)",data)
    
    print (listOfNumbersAsStrings)