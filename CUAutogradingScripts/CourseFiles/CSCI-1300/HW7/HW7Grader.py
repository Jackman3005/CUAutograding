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
    
    submissionFileName = submissionFinder.findSubmission(folderNameContainingSubmission, "dna")
    if (not submissionFileName):
        submissionFileName = submissionFinder.findSubmission(folderNameContainingSubmission, "7")
        if not (submissionFileName):
            deductions.append((-100,"Could not find a file to run! Make sure you are using the correct file name and you are submitting the .cpp source code file"))
            return deductions
    if(submissionFileName != "DNA.cpp"):
        deductions.append((-10,"Incorrect file name! Expected \"DNA.cpp\" but was \"" + submissionFileName +"\""))
    
    
    
    
    compiledFileName = folderNameContainingSubmission + "/dna"
    locationOfStudentSourceCode = folderNameContainingSubmission + "/" + submissionFileName
    
    successfullyCompiled = CPPCompiler.compileCPPFile(locationOfStudentSourceCode, compiledFileName, "DNA")
    if (not successfullyCompiled):
        deductions.append((-100,"Submission did not compile!"))
        return deductions
    
    
    #Check for correct functions
    functions = GradeUtils.CppFunctionFinder(locationOfStudentSourceCode)
    nonMainFunctions = [x for x in functions if x.getName() != "main"]
    if (len(nonMainFunctions) > 0):
        deductions.append((-40,"Used additional functions besides main, this was not allowed."))
    
    
        
    seedLoader = SeedFileLoader()
    seeds = seedLoader.loadSeedsFromFile(folderContainingScripts + "/HW7Seeds.txt")
    
    for seed in seeds:
        
        for i in range(0,len(seed.commandLineInputs())):
            source = folderContainingScripts + "/" + seed.commandLineInputs()[i]
            seed.commandLineInputs()[i] = source
        
        
        programRunner = CPPProgramRunner()
        successfullyRan,output = programRunner.run(compiledFileName, seed.commandLineInputs(), seed.consoleInputs())
        if (not successfullyRan):
            deductions.append((-100,output))
            return deductions
        
        
        
        expectedMousePercentage = seed.expectedOutputs()[0]
        expectedHumanPercentage = seed.expectedOutputs()[1]
        expectedAnswer = seed.expectedOutputs()[2]
        userOutputNumbers = GradeUtils.getAllNumbersFromString(output)
        
        
        tolerance = .00001
        outputLines = output.splitlines();
        
        
        hadIncorrectOutput = False
        comment = ""
        if (len(userOutputNumbers)>1):
            
            if (abs(userOutputNumbers[0] - expectedMousePercentage) > tolerance):
                hadIncorrectOutput = True
                comment+= " Expected Mouse Percentage was: " + str(expectedMousePercentage) + ", received: " + str(userOutputNumbers[0]) + " "
            if (abs(userOutputNumbers[1] - expectedHumanPercentage) > tolerance):
                hadIncorrectOutput = True
                comment+= "Expected Human Percentage was: " + str(expectedHumanPercentage) + ", received: " + str(userOutputNumbers[1]) + " "
            
            cleanedStudentAnswer = re.sub("\s+"," ", outputLines[len(outputLines)-1].strip())
            jackIsVeryLenientStudentAnswer = re.sub("can not", "cannot",cleanedStudentAnswer)
            if (not GradeUtils.stringContainsCorrectWords_WillHandleMispellings(expectedAnswer,jackIsVeryLenientStudentAnswer)):
                hadIncorrectOutput = True
                comment+= " Expected answer to be: "+ expectedAnswer + ", received: " +  cleanedStudentAnswer
        else:
            hadIncorrectOutput = True
            comment = "Could not find the human and/or mouse percentages!"
        if (hadIncorrectOutput):
            deductions.append((-100/len(seeds), comment))
       
    
    return deductions

def deductionsToGradeAndComments(deductions):
    grade = 100
    comments = ""    
    for gradeDeduction, comment in deductions:
        grade += gradeDeduction
        comments += ("\n[%.1f] " % gradeDeduction) + comment + " "
    if (len(deductions)==0):
        comments = "Great work!"
    else:
        comments = comments.rstrip(", ")
    grade = max(round(grade),0)
    
    return (grade,comments)

if __name__ == "__main__":
    submissionFolder = sys.argv[1]
    folderContainingScripts = sys.argv[2]
    deductions = gradeSubmission(submissionFolder,folderContainingScripts + "/CourseFiles/CSCI-1300/HW9")
    
    grade, comments = deductionsToGradeAndComments(deductions)
    
    studentFeedback(comments)
    
    print(max(grade,0))
