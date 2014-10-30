#THESE LINES ARE NEEDED TO ADD THE GradingScriptLibrary path to the system path so they can be imported!!!
import os,sys,inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
#DO NOT DELETE THE LINES ABOVE


import configparser
import importlib.machinery
from GradingScriptLibrary.LocalBatchGrading import Extraction
from GradingScriptLibrary.LocalBatchGrading import StudentGradingDictionary
from GradingScriptLibrary.LocalBatchGrading import StudentCSV

try:
    configFileLocation = sys.argv[1]
    config = configparser.ConfigParser()
    config.read(configFileLocation)
    zipFilesFolderLocation = config['Paths']['zip_submissions_folder']
    outputCsvFileLocation = config['Paths']['grade_output_file']
    outputLogFileLocation = config['Paths']['output_log_file'] 
    universityRosterLocation = config['Paths']['university_roster']
    crossReferenceRosterLocation = config['Paths'].get('cross_reference_roster',fallback=False)
    gradingScriptFileLocation = config['Paths']['grading_script_file']
    
except Exception as e:
    print("Problem Reading config file! make sure you pass one in when you call this script!")
    print(e.strerror)
else:
    #import the grading script file dynamically
    loader = importlib.machinery.SourceFileLoader("module.name", gradingScriptFileLocation)
    autogradingScript = loader.load_module()
    
    gradingScriptFolder = os.path.split(gradingScriptFileLocation)[0]
    
    #redirect the stderr to the log file
    sys.stderr = open(outputLogFileLocation,"w")
    
    
    print ("extracting zip files from",zipFilesFolderLocation)
    Extraction.ExtractSubmissions(zipFilesFolderLocation)
    print ("Finished extracting")
    Students = StudentGradingDictionary.ReturnStudentGradingDictionary(universityRosterLocation,crossReferenceRosterLocation,zipFilesFolderLocation)
    
    
    studentIdKeys = Students.keys()
    numOfStudents = len(studentIdKeys)
    studentCount = 1
    for studentId in studentIdKeys:
        if (studentCount >= 30):
            break
        print("Grading student " + str(studentCount) + "/" + str(numOfStudents) + " " + Students[studentId]["FN"] + " " + Students[studentId]["LN"])
        
        if (Students[studentId]['Directory'] != None):
            Students[studentId]['Grade'], Students[studentId]['Comments'] = autogradingScript.gradeSubmission(zipFilesFolderLocation + "/" + Students[studentId]['Directory'],gradingScriptFolder)
        else:
            Students[studentId]['Grade'], Students[studentId]['Comments'] = (0,"[-100] Could not find a valid submission")
        studentCount +=1
        
    print ("Writing csv file",outputCsvFileLocation)
    StudentCSV.makeCSV(Students,outputCsvFileLocation)    
    
    

