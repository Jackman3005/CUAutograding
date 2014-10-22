#!/bin/python3
import Extraction
import StudentGradingDictionary
import StudentCSV
import sys
import hw6Autograder


zipFilesFolderLocation = sys.argv[1]
outputFileLocation = sys.argv[2]

print ("extracting zip files from",zipFilesFolderLocation)
Extraction.ExtractSubmissions(zipFilesFolderLocation)
print ("Finished extracting")
Students = StudentGradingDictionary.ReturnStudentGradingDictionary('MoodleRosterOct20.csv','RosterOct12.csv',zipFilesFolderLocation)


studentIdKeys = Students.keys()
numOfStudents = len(studentIdKeys)
studentCount = 1
for studentId in studentIdKeys:
    #if (studentCount >= 10):
        #break
    print("Grading student " + str(studentCount)+"/" + str(numOfStudents) + " " + Students[studentId]["FN"] + " " + Students[studentId]["LN"] )
    if (Students[studentId]['Directory'] != None):
        Students[studentId]['Grade'], Students[studentId]['Comments'] = hw6Autograder.gradeSubmission(zipFilesFolderLocation + "/" + Students[studentId]['Directory'])
    else:
        Students[studentId]['Grade'], Students[studentId]['Comments'] = (0,"[-100] Could not find a valid submission")
    studentCount +=1
    
print ("Writing csv file",outputFileLocation)
StudentCSV.makeCSV(Students,outputFileLocation)    
    
    

