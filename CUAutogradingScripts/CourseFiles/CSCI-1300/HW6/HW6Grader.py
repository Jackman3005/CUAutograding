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

from GradingScriptLibrary.CPPHelpers import CPPCompiler
from GradingScriptLibrary.CPPHelpers.CPPProgramRunner import CPPProgramRunner
from GradingScriptLibrary.SeedFileLoader import SeedFileLoader
from GradingScriptLibrary.GradeUtils import studentFeedback


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

def fileNameHasAcceptableExtensionAndRoughlyMatchesName(textToLookFor,fileName):
    if (len(fileName) < len(textToLookFor)):
        return False
    containsText = textToLookFor.lower() in fileName.lower()
    isCPlusPlusFile = (".cpp" in fileName.lower() or ".cc" in fileName.lower() or ".c++" in fileName.lower())
    isNotHiddenOrBackupFile = fileName[0] != '.' and fileName[0] != '~'
    
    return containsText and isCPlusPlusFile and isNotHiddenOrBackupFile

def findHomeworkFiles(folderNameContainingSubmission):
    files = os.listdir(folderNameContainingSubmission)
    deductions = []
    hwFileNameDictionary = {}
    problem1Name = "Hw6Problem1.cpp"
    problem2Name = "Hw6Problem2.cpp"
    problem3Name = "Hw6Problem3.cpp"
    
    for file in files:
        if fileNameHasAcceptableExtensionAndRoughlyMatchesName("problem1",file):
            hwFileNameDictionary["problem1"] = '"' + folderNameContainingSubmission + "/" +file +'"'
            if (file != problem1Name):
                deductions.append((-5, problem1Name+ " had the wrong name ('"+file +"')"))
        elif fileNameHasAcceptableExtensionAndRoughlyMatchesName("problem2",file):
            hwFileNameDictionary["problem2"] = '"' + folderNameContainingSubmission + "/" +file+ '"'
            if (file != problem2Name):
                deductions.append((-5,problem2Name+ " had the wrong name ('"+file +"')"))
        elif fileNameHasAcceptableExtensionAndRoughlyMatchesName("problem3",file):
            hwFileNameDictionary["problem3"] = '"' + folderNameContainingSubmission + "/" +file+ '"'
            if (file != problem3Name):
                deductions.append((-5,problem3Name+ " had the wrong name ('"+file +"')"))
    if len(hwFileNameDictionary) < 3:
        foundFiles =""
        for fileName in hwFileNameDictionary.values():
                foundFiles += fileName + "\t"
        studentFeedback("Could not find all 3 files! Only found",len(hwFileNameDictionary),":",foundFiles)
    return (hwFileNameDictionary,deductions)

def sublistIsInListWithCorrectOrder(sublist, bigList):                                                         
    L = len(sublist) 
    for i in range(len(bigList)-L +1): 
            if bigList[i:i+L] == sublist: 
                    return True 
    return False 

def gradeProblemOne(problem1FileName,seedFileLocation):
    #
    #Test Problem1 file
    #
    #
    deductions = []
    compiledFileName = "/tmp/problem1"
    successfullyCompiled = CPPCompiler.compileCPPFile(problem1FileName, compiledFileName, "Problem 1")
    if (not successfullyCompiled):
        deductions.append((-100/3,"Problem 1 did not compile!"))
        return deductions
        
    seedLoader = SeedFileLoader()
    seeds = seedLoader.loadSeedsFromFile(seedFileLocation)
    
    
    problemsCorrect = 0
    error_bounds = 0.5

    for seed in seeds:
        
        programRunner = CPPProgramRunner()
        successfullyRan,output = programRunner.run(compiledFileName, seed.commandLineInputs(), seed.consoleInputs())
        if (not successfullyRan):
            deductions.append((-100/3,output))
            return deductions
        
        responses = getAllNumbersFromString(output)
        expectedPasserRating = seed.expectedOutputs()[0]
        expectedOutputString = "The passer rating is "+str(expectedPasserRating)
        hadCorrectValuesButIncorrectlyFormattedString = False
        
        
        if (expectedOutputString in output):
            problemsCorrect += 1
        elif (len(responses) > 0):
            previousProblemsCorrect = problemsCorrect;
            for response in responses:
                #if answer given is within acceptable bounds, marked as correct and points added
                if( abs(expectedPasserRating - response) < error_bounds):
                    problemsCorrect += 1
            if (previousProblemsCorrect == problemsCorrect):
                #if not correct, prints the error
                studentFeedback("Looking for: {!s}".format(seed.expectedOutputs()[0]))
                studentFeedback("Received: {!s}".format(responses))
            else:
                hadCorrectValuesButIncorrectlyFormattedString = True
    if problemsCorrect == len(seeds):
        if (hadCorrectValuesButIncorrectlyFormattedString):
            studentFeedback("Problem 1 had correct values, but the format of the string was incorrect")
            deductions.append((-5,"Problem 1 had correct values, but was formatted incorrectly"))
        else:
            studentFeedback("Problem 1 correct!")
    else:
        studentFeedback("Problem 1 INCORRECT")
        deductions.append(((-100/3)*((len(seeds) - problemsCorrect)/len(seeds)), str(len(seeds)-problemsCorrect) + " out of " + str(len(seeds)) + " of the inputs for problem 1 did not produce the correct output."))
    
    
   
        
    return deductions

def gradeProblemTwo(problem2FileName,seedFileLocation):
    compiledCodeName = "/tmp/problem2"
    deductions = []
    try:
        studentFeedback("--------------Compiling Problem 2--------------")
        subprocess.check_call("g++ "+problem2FileName+" -std=c++11 -o "+compiledCodeName,shell=True) 
            
    except Exception:
        studentFeedback("-------------ERROR WHILE COMPILING!------------")
                
        deductions.append((-100/3,"Problem 2 did not compile!"))
        return deductions
    
    #Load problem 2 seed file    
    try:
        seed2 = open(seedFileLocation,'r')
    except IOError:
        studentFeedback("Seed file for Problem 2 not Found!")
        sys.exit(1)
       
    #
    # Problem 2 grading code here
    #
    try:
        seed_count = 0
        seed_values = []
        for line in seed2:
            seed_count += 1
            seed_values.append(getAllNumbersFromString(line))
        problemsCorrect = 0
        for i in range(0,seed_count):
        
            response = []
            
            studentFeedback("Testing Problem2 with inputs of " + str(seed_values[i][0]) + "...")
            try:
                output = subprocess.check_output([compiledCodeName, str(seed_values[i][0])],timeout=5)
            except subprocess.CalledProcessError as err:
                studentFeedback("Error running submission: {!s}".format(err))
                deductions.append((-100/3,"Error Running Problem 2 Submission"))
                return deductions
        
            outputStr = output.decode()
            response = getAllNumbersFromString(outputStr)
            
            expectedOutputValues = [seed_values[i][1],seed_values[i][2],seed_values[i][3]]
            expectedOutputString = "The time is " + str(seed_values[i][1]) + " hours, " + str(seed_values[i][2]) + " minutes, and " + str(seed_values[i][3]) + " seconds"
            hadCorrectValuesButIncorrectlyFormattedString = False
            #response.append(splitted[-1].rstrip('.'))
            if (len(response) >= 3):
                
                if(sublistIsInListWithCorrectOrder(expectedOutputValues,response)):
                    problemsCorrect += 1
                    if (not expectedOutputString in outputStr):
                        hadCorrectValuesButIncorrectlyFormattedString = True
                else:
                    #if not correct, prints the error
                    studentFeedback("Looking for: {!s}, {!s} and {!s}".format(seed_values[i][1], seed_values[i][2], seed_values[i][3]))
                    studentFeedback("Received: {!s}, check for spelling errors!".format(response))
            else:
                studentFeedback("Did not retrieve enough values from output")
        if problemsCorrect == seed_count:
            if (hadCorrectValuesButIncorrectlyFormattedString):
                studentFeedback("Problem 2 had correct values, but the format of the string was incorrect")
                deductions.append((-5,"Problem 2 had correct values, but was formatted incorrectly"))
            else:
                studentFeedback("Problem 2 correct!")
        elif i == (seed_count-1):
            studentFeedback("Problem 2 INCORRECT")
            deductions.append(((-100/3)*((seed_count - problemsCorrect)/seed_count), str(seed_count-problemsCorrect) + " out of " + str(seed_count) + " of the inputs for problem 2 did not produce the correct output."))
    except subprocess.SubprocessError:
        deductions.append((-100/3,"Problem 2 took longer than 5 seconds to run. Most likely an infinite loop or prompt for input!"))
    return deductions


def gradeProblemThree(problem3Filename):
    
    compiledCodeName = "/tmp/problem3"
    deductions = []
    try:
        studentFeedback("--------------Compiling Problem 3--------------")
        subprocess.check_call("g++ "+problem3Filename+" -std=c++11 -o "+compiledCodeName,shell=True) 
            
    except Exception:
        studentFeedback("-------------ERROR WHILE COMPILING!------------")
                
        deductions.append((-100/3,"Problem 3 did not compile!"))
        return deductions
    
    
    try:
        initialStartingPopulation = 307357870
        expectedNewPopulation1 = 310338194
        expectedNewPopulation2 = 310338195
        studentFeedback("Testing Problem3 with starting population of " + str(initialStartingPopulation) +  "...")
        try:
            output = subprocess.check_output([compiledCodeName, str(initialStartingPopulation)],timeout=5)
        except subprocess.CalledProcessError as err:
            studentFeedback("Error running submission: {!s}".format(err))
            deductions.append((-100/3,"Error Running Problem 3 Submission"))
            return deductions
        
        outputStr = output.decode()
        response = getAllNumbersFromString(outputStr)
        
        
        
        expectedOutputString1 = "The population will be " + str(expectedNewPopulation1) + " people"
        expectedOutputString2 = "The population will be " + str(expectedNewPopulation2) + " people"
        if (len(response) > 0):        
            if (response[0] in (expectedNewPopulation1,expectedNewPopulation2)):
                if (expectedOutputString1 in outputStr or expectedOutputString2 in outputStr):
                    studentFeedback("Problem 3 correct!")    
                else:
                    studentFeedback("Problem 3 had correct values, but incorrectly formatted output")
                    deductions.append((-5,"Problem 3 had correct values, but incorrectly formatted output"))
            else:
                #if not correct, prints the error
                studentFeedback("Problem 3 INCORRECT")
                studentFeedback("Looking for: {!s} or {!s}".format(expectedNewPopulation1,expectedNewPopulation2))
                studentFeedback("Received: {!s}".format(response[0]))
                deductions.append((-100/3, "Incorrect output from Problem 3"))
        else:
            deductions.append((-100/3, "There was no acceptable output from Problem 3"))
    except subprocess.SubprocessError:
        deductions.append((-100/3,"Problem 3 took longer than 5 seconds to run. Most likely an infinite loop or prompt for input!"))
   
    return deductions

def gradeSubmission(folderContainingSubmission,folderContainingScripts):
    studentFeedback("\n--------------------------------------------------------------")
    studentFeedback("Grading:",folderContainingSubmission)
    
    hwFileNameDictionary, fileNameDeductions = findHomeworkFiles(folderContainingSubmission)
    
    if ("problem1" in hwFileNameDictionary):
        problem1Deductions = gradeProblemOne(hwFileNameDictionary["problem1"],folderContainingScripts+"/HW6Problem1Seed.txt")
    else:
        problem1Deductions = []
        problem1Deductions.append((-100/3,"Could not find Problem 1 file"))
    if ("problem2" in hwFileNameDictionary):
        problem2Deductions = gradeProblemTwo(hwFileNameDictionary["problem2"],folderContainingScripts+"/HW6Problem2Seed.txt")
    else:
        problem2Deductions = []
        problem2Deductions.append((-100/3,"Could not find Problem 2 file"))
    if ("problem3" in hwFileNameDictionary):
        problem3Deductions = gradeProblemThree(hwFileNameDictionary["problem3"])
    else:
        problem3Deductions = []
        problem3Deductions.append((-100/3,"Could not find Problem 3 file"))
        
    
    grade = 100
    comments = ""
    deductions = []
    deductions.extend(fileNameDeductions)
    deductions.extend(problem1Deductions)
    deductions.extend(problem2Deductions)
    deductions.extend(problem3Deductions)
    
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
    grade,comments = gradeSubmission(submissionFolder,folderContainingScripts)
    
    print(grade)
