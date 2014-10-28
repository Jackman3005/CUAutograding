import GradeUtils

def TestGetAllNumbersFromString():
    
    fns = GradeUtils.CppFunctionFinder('test.cpp')
    cls  =GradeUtils.cppClassFinder('test.cpp')
    #fns = GradeUtils.CppFunctionFinder('Lab9.cpp',full=True)
    #cls = GradeUtils.cppClassFinder('Lab9.cpp',full=True)
    
    if len(fns) > 1:
        print('You used too many functions')
    else:
        print('Correct number of functions')
    
    if len(cls) > 0:
        print('You were not supposed to use classes')
    else:
        print('No classes were used')

def CryptographyTest():
    fns = GradeUtils.CppFunctionFinder('Crypto.cpp')
    cls  =GradeUtils.cppClassFinder('Crypto.cpp')
    
    for i in requiredFnNames:
        requiredFns[i] = {}
        #requiredFns[i]['returnType'] =  
    
    if len(fns) >= 7:
        
        print('You used too many functions')
    else:
        print('Used too few functions')
    
    if len(cls) > 0:
        print('You were not supposed to use classes')
    else:
        print('No classes were used')

def RunAllTests():
    TestGetAllNumbersFromString()
    #CryptographyTest()
    
RunAllTests()


