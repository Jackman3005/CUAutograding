import re
#from pypeg2 import * #parser
#import pypeg2
#from antlr4 import * #possibly use this for python3 parsing
import CppHeaderParser #sudo pip3 install cppheaderparser, also: sudo pip3 install install ply
import os
import sys

# Find out the file location within the sources tree
this_module_dir_path = os.path.abspath(
    os.path.dirname(sys.modules[__name__].__file__))
# Find out gccxml location
gccxml_09_path = os.path.join(
    this_module_dir_path, '..', '..', '..',
    'gccxml_bin', 'v09', sys.platform, 'bin')
# Add pygccxml package to Python path
sys.path.append(os.path.join(this_module_dir_path, '..', '..'))

from pygccxml import parser #sudo pip3 install pygccxml and sudo apt-get install gccxml
from pygccxml import declarations

# Configure GCC-XML parser
config = parser.gccxml_configuration_t(
    gccxml_path=gccxml_09_path,working_directory= this_module_dir_path,cflags = '-std=c++11 -Wall', compiler='g++',ignore_gccxml_output = True)

decls = parser.parse([this_module_dir_path + '/example.hpp'])

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
    
    
