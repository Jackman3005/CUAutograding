import GradeUtils

def TestGetAllNumbersFromString():
    
    fns = GradeUtils.CppFunctionFinder('test.cpp',full=True)
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
    
def RunAllTests():
    TestGetAllNumbersFromString()
    
    
RunAllTests()


