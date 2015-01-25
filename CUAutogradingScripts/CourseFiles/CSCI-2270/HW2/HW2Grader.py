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
from GradingScriptLibrary.GradeUtils import studentFeedback,getAllNumbersFromString,remove_control_chars#,stringContainsCorrecthreerds_WillHandleMispellings
from GradingScriptLibrary.GradeUtils import appendToBeginningOfFile
from GradingScriptLibrary.CPPHelpers import CPPCompiler
from GradingScriptLibrary.CPPHelpers.CPPProgramRunner import CPPProgramRunner
from GradingScriptLibrary.SeedFileLoader import SeedFileLoader
from GradingScriptLibrary import GradeUtils
from GradingScriptLibrary import SubmissionFinder
anyNumberRE =  re.compile("([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)")

def gradeSubmission(folderNameContainingSubmission,folderContainingScripts):
    os.chdir(folderContainingScripts)
    
    deductions = []
    studentFeedback("\n--------------------------------------------------------------")
    studentFeedback("Grading:",folderNameContainingSubmission)
    
    #Find the submission in the folder - sometimes it isn't named exactly
    submissionFinder = SubmissionFinder.SubmissionFinder()
    
    expectedFileName = "Assignment2.cpp"
    submissionFileName = submissionFinder.findSubmission(folderNameContainingSubmission, expectedFileName.strip(".cpp"))
    if (not submissionFileName):
        submissionFileName = submissionFinder.findSubmission(folderNameContainingSubmission, "2")
        if (not submissionFileName):    
            deductions.append((-100,"Could not find a file to run! Make sure you are using the correct file name and you are submitting the .cpp source code file"))
            return deductions
    if(submissionFileName != expectedFileName):
        deductions.append((-75,"Incorrect file name! Expected \" " + expectedFileName + "\" but was \"" + submissionFileName +"\""))  
    
    locationOfFile = folderNameContainingSubmission + "/" + submissionFileName
    
    #Now compile the file        
    compiledFileName = 	folderNameContainingSubmission + "/hw2"
    successfullyCompiled = CPPCompiler.compileCPPFile(locationOfFile, compiledFileName, "Homework File")
    if (not successfullyCompiled):
        deductions.append((-100,"Submission did not compile!"))
        return deductions
         
    #Now run the program with the provided file
    programRunner = CPPProgramRunner(timeout=10)
    commandlineargs = ["Hemmingway_edit.txt", "10"]
    successfullyRan,studentOutput = programRunner.run(compiledFileName, commandlineargs, '')
    solnOutput = open("./outputs/Hemmingway_test.txt").read()
    
    SO_split = studentOutput.split('#')
    SO_split = [x.split('\n') for x in SO_split]
    
    solnOutput = solnOutput.split("#")
    solnOutput = [x.split('\n') for x in solnOutput]
    #Check the output
    
    #warn/deduct if there are not the same number of sections
    if not len(solnOutput) == len(SO_split):
        studentFeedback("Your output does not have the same number of sections as the solution. Check to ensure you have three (and only three) '#' signs")
        deductions.append((-75,"Incorrect number of output sections (separated by '#')"))
        return deductions
    
    sections = {"Top Words":0, "Times Doubled":1, "Unique Words":2}
    
    for x in sections:
        #warn if there are not the same number of sections
        if not len(solnOutput[sections[x]]) == len(SO_split[sections[x]]):
            studentFeedback("Your output for " + x + " does not have the same number of lines as the solution.")
            deductions.append((-20,"Incorrect number of lines in " + x + " section."))
        
        SO_range = range(len(SO_split[sections[x]]))
        soln_range = range(len(solnOutput[sections[x]]))
        
        for i in range(max(len(soln_range),len(SO_range))):
            if i not in SO_range or i not in soln_range:
                if i <= max(soln_range):
                    deductions.append((-10,"You have too few lines for this section"))
                else:
                    deductions.append((-10,"You have too many lines for this section"))
                
                continue
                    
            elif SO_split[sections[x]][i] != solnOutput[sections[x]][i]:
                if x == "Number of Operations":
                    #hint for number of operations
                    studentFeedback("**Operations Counter: If your counter is too low, verify that you are shifting the array when items are removed. If your counter is too high, verify that you are only counting loop operations and that you are not doing unnecessary passes over the data.")
                
                deductions.append((-10,"Expected: " + solnOutput[sections[x]][i] + " got: " + SO_split[sections[x]][i]))
    
    #Now run the program with the provided file
    programRunner = CPPProgramRunner(timeout=10)
    commandlineargs = ["HungerGames_edit.txt", "10"]
    successfullyRan,studentOutput = programRunner.run(compiledFileName, commandlineargs, '')
    solnOutput = open("./outputs/HungerGames_test.txt").read()
    
    SO_split = studentOutput.split('#')
    SO_split = [x.split('\n') for x in SO_split]
    
    solnOutput = solnOutput.split("#")
    solnOutput = [x.split('\n') for x in solnOutput]
    #Check the output
    
    #warn/deduct if there are not the same number of sections
    if not len(solnOutput) == len(SO_split):
        studentFeedback("Your output does not have the same number of sections as the solution. Check to ensure you have three (and only three) '#' signs")
        deductions.append((-75,"Incorrect number of output sections (separated by '#')"))
        return deductions
    
    sections = {"Top Words":0, "Times Doubled":1, "Unique Words":2}
    
    for x in sections:
        #warn if there are not the same number of sections
        if not len(solnOutput[sections[x]]) == len(SO_split[sections[x]]):
            studentFeedback("Your output for " + x + " does not have the same number of lines as the solution.")
            deductions.append((-20,"Incorrect number of lines in " + x + " section."))
        
        SO_range = range(len(SO_split[sections[x]]))
        soln_range = range(len(solnOutput[sections[x]]))
        
        for i in range(max(len(soln_range),len(SO_range))):
            if i not in SO_range or i not in soln_range:
                if i <= max(soln_range):
                    deductions.append((-10,"You have too few lines for this section"))
                else:
                    deductions.append((-10,"You have too many lines for this section"))
                
                continue
                    
            elif SO_split[sections[x]][i] != solnOutput[sections[x]][i]:
                if x == "Number of Operations":
                    #hint for number of operations
                    studentFeedback("**Operations Counter: If your counter is too low, verify that you are shifting the array when items are removed. If your counter is too high, verify that you are only counting loop operations and that you are not doing unnecessary passes over the data.")
                
                deductions.append((-10,"Expected: " + solnOutput[sections[x]][i] + " got: " + SO_split[sections[x]][i]))
                
    #Now run the program with a test file
    programRunner = CPPProgramRunner(timeout=10)
    commandlineargs = ["HungerGames_edit_odd.txt","10"]
    successfullyRan,studentOutput = programRunner.run(compiledFileName, commandlineargs, '')
    solnOutput = open("./outputs/HungerGames_test2.txt").read()
    
    SO_split = studentOutput.split('#')
    SO_split = [x.split('\n') for x in SO_split]
    
    solnOutput = solnOutput.split("#")
    solnOutput = [x.split('\n') for x in solnOutput]
    #Check the output
    
    #warn/deduct if there are not the same number of sections
    if not len(solnOutput) == len(SO_split):
        studentFeedback("Your output does not have the same number of sections as the solution. Check to ensure you have three (and only three) '#' signs")
        deductions.append((-75,"Incorrect number of output sections (separated by '#')"))
        return deductions
    
    for x in sections:
        #warn if there are not the same number of sections
        if not len(solnOutput[sections[x]]) == len(SO_split[sections[x]]):
            studentFeedback("Your output for " + x + " does not have the same number of lines as the solution.")
            deductions.append((-20,"Incorrect number of lines in " + x + " section."))
        
        SO_range = range(len(SO_split[sections[x]]))
        soln_range = range(len(solnOutput[sections[x]]))
        
        for i in range(max(len(soln_range),len(SO_range))):
            if i not in SO_range or i not in soln_range:
                if i <= max(soln_range):
                    deductions.append((-10,"You have too few lines for this section"))
                else:
                    deductions.append((-10,"You have too many lines for this section"))
                
                continue
                    
            elif SO_split[sections[x]][i] != solnOutput[sections[x]][i]:
                if x == "Number of Operations":
                    #hint for number of operations
                    studentFeedback("**Operations Counter: If your counter is too low, verify that you are shifting the array when items are removed. If your counter is too high, verify that you are only counting loop operations and that you are not doing unnecessary passes over the data.")
                
                deductions.append((-10,"Inexact Output"))
    
    #Now run the program with a test file
    programRunner = CPPProgramRunner(timeout=10)
    commandlineargs = ["Hemmingway_edit_odd.txt","10"]
    successfullyRan,studentOutput = programRunner.run(compiledFileName, commandlineargs, '')
    solnOutput = open("./outputs/Hemmingway_test2.txt").read()
    
    SO_split = studentOutput.split('#')
    SO_split = [x.split('\n') for x in SO_split]
    
    solnOutput = solnOutput.split("#")
    solnOutput = [x.split('\n') for x in solnOutput]
    #Check the output
    
    #warn/deduct if there are not the same number of sections
    if not len(solnOutput) == len(SO_split):
        studentFeedback("Your output does not have the same number of sections as the solution. Check to ensure you have three (and only three) '#' signs")
        deductions.append((-75,"Incorrect number of output sections (separated by '#')"))
        return deductions
    
    for x in sections:
        #warn if there are not the same number of sections
        if not len(solnOutput[sections[x]]) == len(SO_split[sections[x]]):
            studentFeedback("Your output for " + x + " does not have the same number of lines as the solution.")
            deductions.append((-20,"Incorrect number of lines in " + x + " section."))
        
        SO_range = range(len(SO_split[sections[x]]))
        soln_range = range(len(solnOutput[sections[x]]))
        
        for i in range(max(len(soln_range),len(SO_range))):
            if i not in SO_range or i not in soln_range:
                if i <= max(soln_range):
                    deductions.append((-10,"You have too few lines for this section"))
                else:
                    deductions.append((-10,"You have too many lines for this section"))
                
                continue
                    
            elif SO_split[sections[x]][i] != solnOutput[sections[x]][i]:
                if x == "Number of Operations":
                    #hint for number of operations
                    studentFeedback("**Operations Counter: If your counter is too low, verify that you are shifting the array when items are removed. If your counter is too high, verify that you are only counting loop operations and that you are not doing unnecessary passes over the data.")
                
                deductions.append((-10,"Inexact Output"))

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
    scriptFolder = os.path.join(sys.argv[2], "CourseFiles/CSCI-2270/HW2")
    deductions = gradeSubmission(submissionFolder, scriptFolder)
    
    grade, comments = deductionsToGradeAndComments(deductions)
    
    studentFeedback(comments)
    
    #Return the Stdout to stdoutstream so that the grade can be printed.
    sys.stdout = stdoutStream
    print(max(grade,0))
