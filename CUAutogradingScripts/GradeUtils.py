import re
#from pypeg2 import * #parser
#import pypeg2
#from antlr4 import * #possibly use this for python3 parsing
import CppHeaderParser #sudo pip3 install cppheaderparser, also: sudo pip3 install install ply

def funCppHeaderParser(cppSourceFileName):
    with open (cppSourceFileName, "r") as myfile:
        data=myfile.read()
        
    try:
        cppHeader = CppHeaderParser.CppHeader(cppSourceFileName)
        
    except CppHeaderParser.CppParseError as e:
        print(e)
        exit(1)
        
    return cppHeader

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
    
def CppFunctionFinder (cppSourceFileName, full = False):
    cppHeader = funCppHeaderParser(cppSourceFileName)

    nameFunctions = []
    for i in range(0, len(cppHeader.functions)):
        nameFunctions.append(cppHeader.functions[i]['name'])
    
    if not full:
        return nameFunctions
    else:
        return cppHeader.functions

def cppClassFinder(cppSourceFileName,full = False):
    cppHeader = funCppHeaderParser(cppSourceFileName)

    nameClasses = []
    for i in cppHeader.classes.keys():
        nameClasses.append(cppHeader.classes[i]['name'])
    
    if not full:
        return nameClasses
    else:
        return cppHeader.classes

def cppParser(cppSourceFileName):
    cppHeader = funCppHeaderParser(cppSourceFileName)
    
    return cppHeader
    
    
