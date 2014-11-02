import re
#from pypeg2 import * #parser
#import pypeg2
#from antlr4 import * #possibly use this for python3 parsing
import CppHeaderParser #sudo pip3 install cppheaderparser, also: sudo pip3 install ply
import os
import sys

shouldPrint =True

def studentFeedback(*strToPrint):
    if (shouldPrint):
        print (*strToPrint,file=sys.stderr)

def funCppHeaderParser(cppSourceFileName):
    #with open (cppSourceFileName, "r") as myfile:
        #data=myfile.read()
        
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
    
def CppFunctionFinder (cppSourceFileName):
    cppHeader = funCppHeaderParser(cppSourceFileName)

    Functions = []
    for i in range(0, len(cppHeader.functions)):
        fn = Function(cppHeader.functions[i])
        Functions.append(fn)
    
    return Functions

def cppClassFinder(cppSourceFileName):
    cppHeader = funCppHeaderParser(cppSourceFileName)

    nameClasses = []
    for i in cppHeader.classes.keys():
        nameClasses.append(Classes(i,cppHeader.classes[i]))
        
    return nameClasses

def cppParser(cppSourceFileName):
    cppHeader = funCppHeaderParser(cppSourceFileName)
    
    return cppHeader

def gccxmlstuff():
    
    # Find out the file location within the sources tree
    this_module_dir_path = os.path.abspath(
        os.path.dirname(sys.modules[__name__].__file__))
    # Find out gccxml location
    gccxml_09_path = os.path.join(
        this_module_dir_path, '..', '..', '..',
        'gccxml_bin', 'v09', sys.platform, 'bin')
    # Add pygccxml package to Python path
    sys.path.append(os.path.join(this_module_dir_path, '..', '..'))
    
    from pygccxml import parser #sudo pip3 install pygccxml and sudo apt-get install gccxml, sudo apt-get install g++-multilib
    from pygccxml import declarations
    
    # Configure GCC-XML parser
    config = parser.gccxml_configuration_t(
        gccxml_path=gccxml_09_path,cflags = '',compiler='g++')
    
    decls = parser.parse([this_module_dir_path + '/Lab9.cpp'],config)  
    
class Function:
    def __init__(self,FDict):
        self._functionInfo = FDict
                
    def getName(self):
        return self._functionInfo['name']
    
    def getReturnType(self):
        return self._functionInfo['rtnType']
    
    def getParameters(self):
        paramList = []
        for x in self._functionInfo['parameters']:
            paramList.append(Parameter(x))
            
        return paramList
class Parameter:
    def __init__(self,PDict):
        self._parameterInfo = PDict
                
    def getName(self):
        return self._parameterInfo['name']
    
    def getType(self):
        return self._parameterInfo['type']

class Classes:
    def __init__(self,CName,CDict):
        self._classInfo = CDict
        self._className = CName       
    def getName(self):
        return self._className
