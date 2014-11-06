#!/usr/bin/env python3
 
#CSCI 1300 - Assignment 6 Grader
#THESE LINES ARE NEEDED TO ADD THE GradingScriptLibrary path to the system path so they can be imported!!!
import os,sys,inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../../")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
#DO NOT DELETE THE LINES ABOVE

import subprocess
import re
import shutil
from GradingScriptLibrary.GradeUtils import studentFeedback
from GradingScriptLibrary.CPPHelpers import CPPCompiler
from GradingScriptLibrary.CPPHelpers.CPPProgramRunner import CPPProgramRunner
from GradingScriptLibrary.SeedFileLoader import SeedFileLoader
from GradingScriptLibrary import GradeUtils
from GradingScriptLibrary import SubmissionFinder


def gradeSubmission(folderNameContainingSubmission,folderContainingScripts):
    deductions = []
    studentFeedback("\n--------------------------------------------------------------")
    studentFeedback("Grading:",folderNameContainingSubmission)
    
    submissionFinder = SubmissionFinder.SubmissionFinder()
    
    submissionFileName = submissionFinder.findSubmission(folderNameContainingSubmission, "crypt")
    if (not submissionFileName):
        deductions.append((-100,"Could not find a file to run! Make sure you are using the correct file name and you are submitting the .cpp source code file"))
        return deductions
    elif(submissionFileName != "Crypto.cpp"):
        deductions.append((-10,"Incorrect file name! Expected \"Crypto.cpp\" but was \"" + submissionFileName +"\""))
    
    
    
    
    compiledFileName = folderNameContainingSubmission + "/hw9"
    locationOfStudentSourceCode = folderNameContainingSubmission + "/" + submissionFileName
    successfullyCompiled = CPPCompiler.compileCPPFile(locationOfStudentSourceCode, compiledFileName, "Crypto")
    if (not successfullyCompiled):
        deductions.append((-100,"Submission did not compile!"))
        return deductions
    
    
    #Check for correct functions
    functions = GradeUtils.CppFunctionFinder(locationOfStudentSourceCode)
    
    
    requiredFunctions = {}
    requiredFunctions["readFile"] = {"params":["string"],"returns":"string"}
    requiredFunctions["encryptChar"] = {"params":["char","int"],"returns":"char"}
    requiredFunctions["decryptChar"] = {"params":["char","int"],"returns":"char"}
    requiredFunctions["encryptMessage"] = {"params":["string","int"],"returns":"string"}
    requiredFunctions["decryptMessage"] = {"params":["string","int"],"returns":"string"}
    requiredFunctions["writeToFile"] = {"params":["string","string","string"],"returns":"void"}
    requiredFunctions["main"] = {}
    for function in functions:
        if (function.getName() in requiredFunctions):
            hadCorrectParameters = True
            hadCorrectReturnType = True
            requiredFunction = requiredFunctions[function.getName()]
            if ("params" in requiredFunction):
                studentParameters = function.getParameters()
                expectedParameters = requiredFunction["params"]
                if(len(studentParameters) != len(expectedParameters)):
                    hadCorrectParameters = False
                else:
                    for i in range(len(studentParameters)):
                        if (studentParameters[i].getType() != expectedParameters[i]):
                            hadCorrectParameters = False
            if ("returns" in requiredFunction):
                hadCorrectReturnType = function.getReturnType() == requiredFunction["returns"] 
            del requiredFunctions[function.getName()]
            
            comment = "The \"" + function.getName() + "\" function was incorrectly defined\n"
            if (not hadCorrectParameters):
                comment += "Expected " + str(len(requiredFunction['params'])) + " parameters of type " + ", ".join(requiredFunction['params']) + "\n"
                comment += "Received " + str(len(function.getParameters())) + " parameters of type " + ", ".join([x.getType() for x in function.getParameters()])  + "\n"
            if (not hadCorrectReturnType):
                comment += "Expected return type of " + requiredFunction['returns'] + "\n"
                comment += "Received return type of " + function.getReturnType() + "\n"
            
            if (not hadCorrectParameters or not hadCorrectReturnType):
                deductions.append((-10, comment))
    
    
    for missingFunction in requiredFunctions.keys():
        deductions.append((-10, "Function \"" + missingFunction + "\" was missing from your source code file."))
        
        
    seedLoader = SeedFileLoader()
    seeds = seedLoader.loadSeedsFromFile(folderContainingScripts + "/HW9Seeds.txt")
    
    for seed in seeds:
        
        #copy the input file to the student submission directory so user can read from it and then write a new file to the same directory
        shutil.copyfile(folderContainingScripts + "/" + seed.commandLineInputs()[2], folderNameContainingSubmission + "/" +  seed.commandLineInputs()[2])
        seed.commandLineInputs()[2] =folderNameContainingSubmission + "/" +  seed.commandLineInputs()[2]
        
        
        programRunner = CPPProgramRunner()
        successfullyRan,output = programRunner.run(compiledFileName, seed.commandLineInputs(), seed.consoleInputs())
        if (not successfullyRan):
            deductions.append((-100,output))
            return deductions
        
        with open(seed.commandLineInputs()[2],"r") as seededInputFile:
            contentsOfSeedFile = seededInputFile.read()
        
        expectedEncodedOrDecodedOutput = seed.expectedOutputs()[0]
        userOutput = output.lstrip().rstrip()
        
        expectedExactConsoleOutputLine1 = ""
        if ('e' in seed.commandLineInputs()[0].lower()):
            extension = ".enc"
            expectedExactConsoleOutputLine1 += "Encrypting file: " + seed.commandLineInputs()[2]
        else:
            extension = ".dec"
            expectedExactConsoleOutputLine1 += "Decrypting file: " + seed.commandLineInputs()[2]
        
        expectedExactConsoleOutputLine2 = contentsOfSeedFile
        expectedExactConsoleOutputLine3 = expectedEncodedOrDecodedOutput
        
        
        
        
        
        #Make sure they have all three lines of correct output P.S. Gnarly ass string
        if (expectedExactConsoleOutputLine1 not in userOutput or expectedExactConsoleOutputLine2 not in userOutput or expectedExactConsoleOutputLine3 not in userOutput):
            deductions.append((-100/len(seeds),"Console output was incorrect. Given Parameters: " + " ".join(seed.commandLineInputs()) + "\n" + 
                                               "-------------------------------------------------------\n" +
                                               "The provided file contained the text:\n" + 
                                               contentsOfSeedFile + "\n\n" +
                                               "The expected output was: \n" + 
                                               expectedExactConsoleOutputLine1 + "\n" + 
                                               expectedExactConsoleOutputLine2 +"\n" + 
                                               expectedExactConsoleOutputLine3  + "\n\n" +
                                               "What was actually received was:\n" +
                                               userOutput + "\n" +
                                               "-------------------------------------------------------\n"  ))
            continue;
        
        
        userOutputFileName = seed.commandLineInputs()[2] + extension
        
        try:
            
            userOutputFile = open(userOutputFileName,"r")
            contentsOfFile = userOutputFile.read()
            userOutputFile.close()
            
            if (contentsOfFile.lstrip().rstrip() != expectedEncodedOrDecodedOutput):
                deductions.append((-100/len(seeds),"Output file was incorrect. Given Parameters: " + " ".join(seed.commandLineInputs()) + "\n" + 
                                                   "-------------------------------------------------------\n" +
                                                   "The provided file contained the text:\n" + 
                                                   contentsOfSeedFile + "\n\n" +
                                                   "The expected output was: \n" + 
                                                   expectedEncodedOrDecodedOutput  + "\n\n" +
                                                   "What was actually received was:\n" +
                                                   contentsOfFile + "\n" +
                                                   "-------------------------------------------------------\n"  ))
        except Exception as e:
            studentFeedback("There was an issue reading your output file!!", "Expected to find an output file of name \"" + os.path.split(userOutputFileName)[1] + "\"\n",e)             
            
            
    
    return deductions

def deductionsToGradeAndComments(deductions):
    grade = 100
    comments = ""    
    for gradeDeduction, comment in deductions:
        grade += gradeDeduction
        comments += ("\n[%.1f] " % gradeDeduction) + comment + ", "
    if (len(deductions)==0):
        comments = "Great work!"
    else:
        comments = comments.rstrip(", ")
    grade = max(round(grade),0)
    
    return (grade,comments)

if __name__ == "__main__":
    #Assign all output to the stderr stream as a catch all
    stdoutStream = sys.stdout
    sys.stdout = sys.stderr
    
    submissionFolder = sys.argv[1]
    folderContainingScripts = sys.argv[2]
    deductions = gradeSubmission(submissionFolder,folderContainingScripts + "/CourseFiles/CSCI-1300/HW9")
    
    grade, comments = deductionsToGradeAndComments(deductions)
    
    studentFeedback(comments)
    
    #Return the Stdout to stdoutstream so that the grade can be printed.
    sys.stdout = stdoutStream
    print(max(grade,0))
