#!/usr/bin/env python3
 
#CSCI 1300 - Assignment 3 Grader
#Make sure this file is in the same folder as your assignments
#Your assignments need to be called Problem1.py, Problem2.py, Problem3.py and Problem4.py

#Put Seed1.txt, Seed2.txt, Seed3.txt, and Seed4.txt in the same folder too!

#Run this file to test your code

import subprocess
import sys
import os
import re

shouldPrint = True
'''
Correct answers,
acceptable bounds for student answers,
total points for assignment so far
'''

def myPrint(*strToPrint, file=sys.stderr):
    if (shouldPrint):
        print (strToPrint,file=file)

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
        myPrint("Could not find all 3 files! Only found",len(hwFileNameDictionary),":",foundFiles, file=sys.stderr)
    return (hwFileNameDictionary,deductions)

def sublistIsInListWithCorrectOrder(sublist, list):                                                         
    L = len(sublist) 
    for i in range(len(list)-L +1): 
            if list[i:i+L] == sublist: 
                    return True 
    return False 

def gradeProblemOne(problem1FileName):
    #
    #Test Problem1 file
    #
    #
    deductions = []
    try:
        myPrint("--------------Compiling Problem 1--------------")
        subprocess.check_call("g++ "+problem1FileName+" -std=c++11 -o problem1",shell=True) 
            
    except Exception:
        myPrint("-------------ERROR WHILE COMPILING!------------",file=sys.stderr)
                
        deductions.append((-100/3,"Problem 1 did not compile!"))
        return deductions
        
    
    try:
        seed1 = open("Seed1.txt",'r')
    except IOError:
        myPrint("Seed file for Problem 1 not Found!", file=sys.stderr)
        sys.exit(1)
    
    
    seed_count = 0
    seed_values = []
    for line in seed1:
        seed_count += 1
        temp2 = getAllNumbersFromString(line)
        seed_values.append(temp2)
    
    problemsCorrect = 0
    error_bounds = 0.5
    try:
        for i in range(0,seed_count):
            out=""
            myPrint("Testing Problem1 with inputs of " + str(int(seed_values[i][0])) + " " + str(int(seed_values[i][1])) + " " + str(int(seed_values[i][2])) + " " + str(int(seed_values[i][3])) +" " + str(int(seed_values[i][4])) +"...", file=sys.stderr)
            try:
                p1Process = subprocess.Popen("./problem1",stdout=subprocess.PIPE,stdin=subprocess.PIPE,shell=True)
                out,err = p1Process.communicate((str(int(seed_values[i][0]))+"\n" + str(int(seed_values[i][1])) +"\n" + str(int(seed_values[i][2]))+"\n"+str(int(seed_values[i][3]))+"\n"+str(int(seed_values[i][4]))).encode(),timeout=5)
                
        
            except subprocess.CalledProcessError as err:
                myPrint("Error running submission: {!s}".format(err), file=sys.stderr)
                deductions.append((-100/3,"Error Running Problem 1 Submission"))
                return deductions
        
            outputStr = out.decode()
            responses = getAllNumbersFromString(outputStr)
            expectedPasserRating = seed_values[i][5]
            expectedOutputString = "The passer rating is "+str(expectedPasserRating)
            hadCorrectValuesButIncorrectlyFormattedString = False
            
            
            if (expectedOutputString in outputStr):
                problemsCorrect += 1
            elif (len(responses) > 0):
                previousProblemsCorrect = problemsCorrect;
                for response in responses:
                    #if answer given is within acceptable bounds, marked as correct and points added
                    if( abs(expectedPasserRating - response) < error_bounds):
                        problemsCorrect += 1
                if (previousProblemsCorrect == problemsCorrect):
                    #if not correct, prints the error
                    myPrint("Looking for: {!s}".format(seed_values[i][5]), file=sys.stderr)
                    myPrint("Received: {!s}".format(responses), file=sys.stderr)
                else:
                    hadCorrectValuesButIncorrectlyFormattedString = True
        if problemsCorrect == seed_count:
            if (hadCorrectValuesButIncorrectlyFormattedString):
                myPrint("Problem 1 had correct values, but the format of the string was incorrect")
                deductions.append((-5,"Problem 1 had correct values, but was formatted incorrectly"))
            else:
                myPrint("Problem 1 correct!", file=sys.stderr)
        else:
            myPrint("Problem 1 INCORRECT", file=sys.stderr)
            deductions.append(((-100/3)*((seed_count - problemsCorrect)/seed_count), str(seed_count-problemsCorrect) + " out of " + str(seed_count) + " of the inputs for problem 1 did not produce the correct output."))
        
        
        
    except subprocess.TimeoutExpired:
        deductions.append((-100/3,"Problem 1 took longer than 5 seconds to run. Most likely an infinite loop or prompt for input!"))
    
        
    return deductions

def gradeProblemTwo(problem2FileName):
    compiledCodeName = "problem2"
    deductions = []
    try:
        myPrint("--------------Compiling Problem 2--------------")
        subprocess.check_call("g++ "+problem2FileName+" -std=c++11 -o "+compiledCodeName,shell=True) 
            
    except Exception:
        myPrint("-------------ERROR WHILE COMPILING!------------",file=sys.stderr)
                
        deductions.append((-100/3,"Problem 2 did not compile!"))
        return deductions
    
    #Load problem 2 seed file    
    try:
        seed2 = open("Seed2.txt",'r')
    except IOError:
        myPrint("Seed file for Problem 2 not Found!", file=sys.stderr)
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
            
            myPrint("Testing Problem2 with inputs of " + str(seed_values[i][0]) + "...", file=sys.stderr)
            try:
                output = subprocess.check_output(["./"+compiledCodeName, str(seed_values[i][0])],timeout=5)
            except subprocess.CalledProcessError as err:
                myPrint("Error running submission: {!s}".format(err), file=sys.stderr)
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
                    myPrint("Looking for: {!s}, {!s} and {!s}".format(seed_values[i][1], seed_values[i][2], seed_values[i][3]), file=sys.stderr)
                    myPrint("Received: {!s}, check for spelling errors!".format(response), file=sys.stderr)
            else:
                myPrint("Did not retrieve enough values from output")
        if problemsCorrect == seed_count:
            if (hadCorrectValuesButIncorrectlyFormattedString):
                myPrint("Problem 2 had correct values, but the format of the string was incorrect")
                deductions.append((-5,"Problem 2 had correct values, but was formatted incorrectly"))
            else:
                myPrint("Problem 2 correct!", file=sys.stderr)
        elif i == (seed_count-1):
            myPrint("Problem 2 INCORRECT", file=sys.stderr)
            deductions.append(((-100/3)*((seed_count - problemsCorrect)/seed_count), str(seed_count-problemsCorrect) + " out of " + str(seed_count) + " of the inputs for problem 2 did not produce the correct output."))
    except subprocess.SubprocessError:
        deductions.append((-100/3,"Problem 2 took longer than 5 seconds to run. Most likely an infinite loop or prompt for input!"))
    return deductions


def gradeProblemThree(problem3Filename):
    
    compiledCodeName = "problem3"
    deductions = []
    try:
        myPrint("--------------Compiling Problem 3--------------")
        subprocess.check_call("g++ "+problem3Filename+" -std=c++11 -o "+compiledCodeName,shell=True) 
            
    except Exception:
        myPrint("-------------ERROR WHILE COMPILING!------------",file=sys.stderr)
                
        deductions.append((-100/3,"Problem 3 did not compile!"))
        return deductions
    
    
    try:
        initialStartingPopulation = 307357870
        expectedNewPopulation1 = 310338194
        expectedNewPopulation2 = 310338195
        myPrint("Testing Problem3 with starting population of " + str(initialStartingPopulation) +  "...", file=sys.stderr)
        try:
            output = subprocess.check_output(["./"+compiledCodeName, str(initialStartingPopulation)],timeout=5)
        except subprocess.CalledProcessError as err:
            myPrint("Error running submission: {!s}".format(err), file=sys.stderr)
            deductions.append((-100/3,"Error Running Problem 3 Submission"))
            return deductions
        
        outputStr = output.decode()
        response = getAllNumbersFromString(outputStr)
        
        
        
        expectedOutputString1 = "The population will be " + str(expectedNewPopulation1) + " people"
        expectedOutputString2 = "The population will be " + str(expectedNewPopulation2) + " people"
        if (len(response) > 0):        
            if (response[0] in (expectedNewPopulation1,expectedNewPopulation2)):
                if (expectedOutputString1 in outputStr or expectedOutputString2 in outputStr):
                    myPrint("Problem 3 correct!", file=sys.stderr)    
                else:
                    myPrint("Problem 3 had correct values, but incorrectly formatted output")
                    deductions.append((-5,"Problem 3 had correct values, but incorrectly formatted output"))
            else:
                #if not correct, prints the error
                myPrint("Problem 3 INCORRECT", file=sys.stderr)
                myPrint("Looking for: {!s} or {!s}".format(expectedNewPopulation1,expectedNewPopulation2), file=sys.stderr)
                myPrint("Received: {!s}".format(response[0]), file=sys.stderr)
                deductions.append((-100/3, "Incorrect output from Problem 3"))
        else:
            deductions.append((-100/3, "There was no acceptable output from Problem 3"))
    except subprocess.SubprocessError:
        deductions.append((-100/3,"Problem 3 took longer than 5 seconds to run. Most likely an infinite loop or prompt for input!"))
   
    return deductions

def gradeSubmission(folderNameContainingSubmission):
    myPrint("\n--------------------------------------------------------------")
    myPrint("Grading:",folderNameContainingSubmission)
    
    hwFileNameDictionary, fileNameDeductions = findHomeworkFiles(folderNameContainingSubmission)
    
    if ("problem1" in hwFileNameDictionary):
        problem1Deductions = gradeProblemOne(hwFileNameDictionary["problem1"])
    else:
        problem1Deductions = []
        problem1Deductions.append((-100/3,"Could not find Problem 1 file"))
    if ("problem2" in hwFileNameDictionary):
        problem2Deductions = gradeProblemTwo(hwFileNameDictionary["problem2"])
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
    
