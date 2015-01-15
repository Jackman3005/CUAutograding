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
        return cppHeader
        
    except CppHeaderParser.CppParseError as e:
        studentFeedback ("There was a problem parsing the \""+cppSourceFileName + "\" C++ source code file for functions! See Error Below:\n",e)
        return None
        
    

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

#This function could take some time with larger Files.
def appendToBeginningOfFile(file_name, text):
    with open(file_name, "r+") as f:
     old = f.read() # read everything in the file
     f.seek(0) # rewind
     f.write(text + "\n" + old)
     
     
#This function will leniently look for words within a string. The words must be in the order
#that they are expected. The words may be mispelled or have the wrong case and it will still be
#counted as acceptable. Also if there are extra words in between the expected words they are essentially
#ignored. As long as all of the expected words are found in order within the text then this will return true
#In order to install the "enchant" module run "sudo pip3 install pyenchant"
def stringContainsCorrectWords_WillHandleMispellings(expectedText,studentOutput):
    import enchant
    d = enchant.Dict("en_us")
    expectedWords = expectedText.strip().lower().split()
    actualWords = studentOutput.strip().lower().split()
    wordsCorrect = 0
    for wordToCheck in actualWords:
        if (wordToCheck == expectedWords[wordsCorrect]):
            wordsCorrect += 1
        else:
            possibleCorrectSpellings = d.suggest(wordToCheck)
            if (expectedWords[wordsCorrect] in possibleCorrectSpellings):
                wordsCorrect += 1
    return wordsCorrect == len(expectedWords)
 
 
#This next section is for removing non-printable characters from students strings.
#This is really helpful because the strings will appear completely identical but will not
#equal eachother when evaluated. So. we can remove all the nonprintable characters and then compare them.           
import unicodedata, re
control_chars = ''.join(map(chr, list(range(0,32)) + list(range(127,160))))

control_char_re = re.compile('[%s]' % re.escape(control_chars))

def remove_control_chars(s):
    return control_char_re.sub('', s)
    
    
def CppFunctionFinder (cppSourceFileName):
    cppHeader = funCppHeaderParser(cppSourceFileName)

    if (cppHeader != None):
        Functions = []
        for i in range(0, len(cppHeader.functions)):
            fn = Function(cppHeader.functions[i])
            Functions.append(fn)
        
        return (True,Functions)
    return (False,None)

def cppClassFinder(cppSourceFileName):
    cppHeader = funCppHeaderParser(cppSourceFileName)
    
    if (cppHeader != None):
        
        nameClasses = []
        for i in cppHeader.classes.keys():
            nameClasses.append(Classes(i,cppHeader.classes[i]))
            
        return (True,nameClasses)
    return(False,None)

def cppParser(cppSourceFileName):
    cppHeader = funCppHeaderParser(cppSourceFileName)
    
    return cppHeader
'''
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
'''  
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
    
class Method:
    def __init__(self,MDict,scope):
        self._methodInfo = MDict
        self._scope = scope        
    def getName(self):
        return self._methodInfo['name']
    def getScope(self):
        return self._scope
    def getReturnType(self):
        return self._methodInfo['rtnType']
    
    def getParameters(self):
        paramList = []
        for x in self._methodInfo['parameters']:
            paramList.append(Parameter(x))

class Classes:
    def __init__(self,CName,CDict):
        self._classInfo = CDict
        self._className = CName       
    def getName(self):
        return self._className
    def getMethods(self):
        methodList =[]
        for x in self._classInfo['methods']:
            if len(self._classInfo['methods'][x]) != 0:
                for y in range(0,len(self._classInfo['methods'][x])):
                    methodList.append(Method(self._classInfo['methods'][x][y],x))
        return methodList
                

            
