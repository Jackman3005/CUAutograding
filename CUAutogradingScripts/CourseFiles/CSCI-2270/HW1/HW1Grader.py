#!/usr/bin/env python3
 
#CSCI 1300 - Assignment 6 Grader
#THESE LINES ARE NEEDED TO ADD THE GradingScriptLibrary path to the system path so they can be imported!!!
import os,sys,inspect
from numpy import nan

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../../")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
#DO NOT DELETE THE LINES ABOVE

import subprocess
import re
import shutil
import codecs
from GradingScriptLibrary.GradeUtils import studentFeedback,\
    getAllNumbersFromString,remove_control_chars,stringContainsCorrectWords_WillHandleMispellings
from GradingScriptLibrary.GradeUtils import appendToBeginningOfFile
from GradingScriptLibrary.CPPHelpers import CPPCompiler
from GradingScriptLibrary.CPPHelpers.CPPProgramRunner import CPPProgramRunner
from GradingScriptLibrary.SeedFileLoader import SeedFileLoader
from GradingScriptLibrary import GradeUtils
from GradingScriptLibrary import SubmissionFinder
anyNumberRE =  re.compile("([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)")

def gradeSubmission(folderNameContainingSubmission,folderContainingScripts):
    deductions = []
    studentFeedback("\n--------------------------------------------------------------")
    studentFeedback("Grading:",folderNameContainingSubmission)
    
    #Find the submission in the folder - sometimes it isn't named exactly
    submissionFinder = SubmissionFinder.SubmissionFinder()
    
    expectedFileName = "Assignment1Solution.cpp"
    submissionFileName = submissionFinder.findSubmission(folderNameContainingSubmission, expectedFileName.strip(".cpp"))
    if (not submissionFileName):
        submissionFileName = submissionFinder.findSubmission(folderNameContainingSubmission, "1")
        if (not submissionFileName):    
            deductions.append((-100,"Could not find a file to run! Make sure you are using the correct file name and you are submitting the .cpp source code file"))
            return deductions
    if(submissionFileName != expectedFileName):
        deductions.append((-10,"Incorrect file name! Expected \" " + expectedFileName + "\" but was \"" + submissionFileName +"\""))  
    
    locationOfFile = folderNameContainingSubmission + "/" + submissionFileName
    
    #Now compile the file        
    compiledFileName = 	folderNameContainingSubmission + "/hw1"
    successfullyCompiled = CPPCompiler.compileCPPFile(locationOfFile, compiledFileName, "Homework File")
    if (not successfullyCompiled):
        deductions.append((-100,"Submission did not compile!"))
        return deductions
         
    #Now run the program
    programRunner = CPPProgramRunner()
    commandlineargs = ["messageBoard.txt"]
    successfullyRan,studentOutput = programRunner.run(compiledFileName, commandlineargs, '')
    
    #Check the output
    ans = open("./tests/output.txt").read() in studentOutput
    
    if ans != True:
        deductions.append((-100,"Incorrect output"))
        
    
    #Return the grade/comments
    return deductions


def deductionsToGradeAndComments(deductions):
    grade = 100
    comments = "" 
    for gradeDeduction, comment in deductions:
        grade += gradeDeduction
        comments += ("[%.1f] " % gradeDeduction) + comment + "\n"
    if (len(deductions)==0):
        comments = "Great work!"
    else:
        comments = comments.strip("\r").strip("\n")
    grade = max(round(grade),0)
    
    return (grade,comments)

if __name__ == "__main__":
    #Assign all output to the stderr stream as a catch all
    stdoutStream = sys.stdout
    sys.stdout = sys.stderr
    
    submissionFolder = sys.argv[1]
    #folderContainingScripts = sys.argv[2]
    deductions = gradeSubmission(submissionFolder,"/CourseFiles/CSCI-2700/HW1")
    
    grade, comments = deductionsToGradeAndComments(deductions)
    
    studentFeedback(comments)
    
    #Return the Stdout to stdoutstream so that the grade can be printed.
    sys.stdout = stdoutStream
    print(max(grade,0))
