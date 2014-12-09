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
    getAllNumbersFromString,remove_control_chars
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
    
    submissionFinder = SubmissionFinder.SubmissionFinder()
    
    driverFileName = "SeedDriver.cpp"
    
    expectedFileName = "Library.cpp"
    submissionFileName = submissionFinder.findSubmission(folderNameContainingSubmission, expectedFileName.strip(".cpp"))
    if (not submissionFileName):
        submissionFileName = submissionFinder.findSubmission(folderNameContainingSubmission, "10")
        if (not submissionFileName):    
            deductions.append((-100,"Could not find a file to run! Make sure you are using the correct file name and you are submitting the .cpp source code file"))
            return deductions
    if(submissionFileName != expectedFileName):
        deductions.append((-10,"Incorrect file name! Expected \" " + expectedFileName + "\" but was \"" + submissionFileName +"\""))  
    
    locationOfSeedDriverFile = folderNameContainingSubmission + "/" + driverFileName
    #copy seed driver to student submission folder
    shutil.copyfile(folderContainingScripts +"/" + driverFileName,locationOfSeedDriverFile)
    #edit the driver file to import the student library.cpp
    appendToBeginningOfFile(locationOfSeedDriverFile,"#include \"" + submissionFileName + "\"")
    
    deductions.extend(verifyClassesExist())
    
    #Now compile the file        
    compiledFileName = folderNameContainingSubmission + "/hw10"
    successfullyCompiled = CPPCompiler.compileCPPFile(locationOfSeedDriverFile, compiledFileName, "Seeded Driver")
    if (not successfullyCompiled):
        deductions.append((-100,"Submission did not compile!"))
        return deductions
         
    seeds = SeedFileLoader().loadSeedsFromFile(folderContainingScripts + "/HW10Seeds.txt")
    for seed in seeds:
        #copy the input file to the student submission directory so user can read from it and then write a new file to the same directory
        shutil.copyfile(folderContainingScripts + "/" + seed.commandLineInputs()[0], folderNameContainingSubmission + "/" +  seed.commandLineInputs()[0])
        shutil.copyfile(folderContainingScripts + "/" + seed.commandLineInputs()[1], folderNameContainingSubmission + "/" +  seed.commandLineInputs()[1])   
        seed.commandLineInputs()[0] =folderNameContainingSubmission + "/" +  seed.commandLineInputs()[0]
        seed.commandLineInputs()[1] =folderNameContainingSubmission + "/" +  seed.commandLineInputs()[1]
        
        programRunner = CPPProgramRunner()
        successfullyRan,output = programRunner.run(compiledFileName, seed.commandLineInputs(), seed.consoleInputs())
        if (not successfullyRan):
            deductions.append((-100/len(seeds),output))
            return deductions
        fileContainingExpectedOutput = open(folderContainingScripts + "/" + seed.expectedOutputs()[0],"r")
        
        missingOutput = ""
        outputMatches = True
        for line in fileContainingExpectedOutput:
            cleanedOutput = re.subn('[\ \t]+',' ',output)[0]
            if line not in cleanedOutput:
                lineFound = False
                allNumbersInExpectedLine = getAllNumbersFromString(line)
                if (len(allNumbersInExpectedLine) > 0):
                    expectedNumber = allNumbersInExpectedLine[0]
                    lineTextSansNumbers = anyNumberRE.sub('',line).strip()
                    for l in cleanedOutput.split('\n'):
                        l = re.subn("\s+", ' ', l)[0]
                        lineTextSansNumbers = re.subn("\s+", ' ', lineTextSansNumbers)[0]
                        if lineTextSansNumbers in l:
                            allNumbersInActualLine = getAllNumbersFromString(l)
                            if (len(allNumbersInActualLine) > 0):
                                actualNumber = allNumbersInActualLine[0]
                                if (abs(expectedNumber - actualNumber) <= .02):
                                    lineFound = True
                            elif(expectedNumber == 0):
                                    lineFound = True
                if (not lineFound):
                    outputMatches = False
                    missingOutput += line + "\n"
        if (not outputMatches):
            deductions.append((-80/len(seeds),"Output did not match, the following lines were missing: \n" + missingOutput))
        
        
    return deductions

def verifyClassesExist():
    '''
    #Look at classes
    classes = []        
    for i in range(0,len(submissionFileNames)):
        if submissionFileNames[i] != "":
            succeeded, cls = GradeUtils.cppClassFinder(folderNameContainingSubmission + "/" + submissionFileNames[i])
            if succeeded:
                classes.append(cls)
            else:
                classes.append('FAILED')
    #this will loop through all classes and print methods of each, not needed but shows how to access the methods
    for i in range(0,len(classes)):
        for j in range(0,len(classes[i])):
            methods = classes[i][j].getMethods()
            print(classes[i][j].getName())
            for k in range(0,len(methods)):
                print('name ' + methods[k].getName())
                print('scope ' + methods[k].getScope())
                print('rtn ' + methods[k].getReturnType())
    '''
    return [] #Fill this in later
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
    folderContainingScripts = sys.argv[2]
    deductions = gradeSubmission(submissionFolder,folderContainingScripts + "/CourseFiles/CSCI-1300/HW10")
    
    grade, comments = deductionsToGradeAndComments(deductions)
    
    studentFeedback(comments)
    
    #Return the Stdout to stdoutstream so that the grade can be printed.
    sys.stdout = stdoutStream
    print(max(grade,0))
