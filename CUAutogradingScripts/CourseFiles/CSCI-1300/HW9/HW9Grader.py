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
    
    
    
    
    compiledFileName = "/tmp/hw9"
    successfullyCompiled = CPPCompiler.compileCPPFile(folderNameContainingSubmission + "/" + submissionFileName, compiledFileName, "Crypto")
    if (not successfullyCompiled):
        deductions.append((-100,"Submission did not compile!"))
        return deductions
        
    seedLoader = SeedFileLoader()
    seeds = seedLoader.loadSeedsFromFile(folderContainingScripts + "/HW9Seeds.txt")
    
    for seed in seeds:
        
        #copy the input file to the tmp directory so user can read from it and then write a new file to the same directory
        shutil.copyfile(folderContainingScripts + "/" + seed.commandLineInputs()[2], "/tmp/" + seed.commandLineInputs()[2])
        seed.commandLineInputs()[2] ="/tmp/" + seed.commandLineInputs()[2]
        
        
        programRunner = CPPProgramRunner()
        successfullyRan,output = programRunner.run(compiledFileName, seed.commandLineInputs(), seed.consoleInputs())
        if (not successfullyRan):
            deductions.append((-100,output))
            return deductions
        
        with open(seed.commandLineInputs()[2],"r") as seededInputFile:
            contentsOfSeedFile = seededInputFile.read()
        
        expectedOutput = seed.expectedOutputs()[0]
        userOutput = output.lstrip().rstrip()
        print("OUTPUT: " +output)
        
        if (expectedOutput not in userOutput):
            deductions.append((-100/len(seeds),"Console output was incorrect. The provided file had the string \"" + contentsOfSeedFile + "\" the expected output was \"" + expectedOutput + "\" what was actually received was \"" +userOutput + "\""  ))
            
        
        if ('e' in seed.commandLineInputs()[0].lower()):
            extension = ".enc"
        else:
            extension = ".dec"
        userOutputFileName = seed.commandLineInputs()[2] + extension
        print ("Expected user output file name: " + userOutputFileName)
        try:
            
            userOutputFile = open(userOutputFileName,"r")
            contentsOfFile = userOutputFile.read()
            userOutputFile.close()
            
            if (contentsOfFile.lstrip().rstrip() != expectedOutput):
                deductions.append((-100/len(seeds),"Output file was incorrect. The provided file had the string \"" + contentsOfSeedFile + "\" the expected output was \"" + expectedOutput + "\" what was actually received was \"" +contentsOfFile + "\""  ))
        except Exception as e:
            print (e.strerror)
            studentFeedback("There was an issue reading your output file!!", "Expected to find an output file of name \"" + os.path.split(userOutputFileName)[1] + "\"")             
            
            
    
    return deductions

def deductionsToGradeAndComments(deductions):
    grade = 100
    comments = ""    
    for gradeDeduction, comment in deductions:
        grade += gradeDeduction
        comments += ("[%.1f] " % gradeDeduction) + comment + ", "
    if (len(deductions)==0):
        comments = "Great work!"
    else:
        comments = comments.rstrip(", ")
    grade = max(round(grade),0)
    
    return (grade,comments)

if __name__ == "__main__":
    submissionFolder = sys.argv[1]
    folderContainingScripts = sys.argv[2]
    deductions = gradeSubmission(submissionFolder,folderContainingScripts)
    
    grade, comments = deductionsToGradeAndComments(deductions)
    
    studentFeedback(comments)
    
    print(max(grade,0))
