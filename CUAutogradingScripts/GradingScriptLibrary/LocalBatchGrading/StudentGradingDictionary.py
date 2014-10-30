import os
import re

def ReturnStudentGradingDictionary(roster_filename,cross_reference_roster, submission_directory = os.getcwd()):
    files = os.listdir(submission_directory) #make list of folders in the directory
    folderList = []
    for file in files:
        if os.path.isdir(submission_directory + '/' + file):
            folderList.append(file)
    if (cross_reference_roster):
        moodleRoster = {}
        for line in open(cross_reference_roster,"r").readlines()[1:]:
            tokens  = line.split(',')
            firstName = tokens[0]
            lastName = tokens[1]
            email = tokens[2].lower().rstrip().lstrip()
            moodleRoster[email] = {"FN":firstName,"LN":lastName}
    
#parse the roster .csv
    Students = {}
    roster = open(roster_filename, 'r')
    next(roster)
    for studentId in roster:
        info = studentId.split(',')
        email = info[2].lower().strip('"').rstrip().lstrip()
        FN = info[1].lower().strip('"').strip()
        LN = info[0].lower().strip('"').strip()
        Information = {}
        Information['FN'] = ''
        Information['LN'] = ''
        Information['Grade'] = 0
        Information['Comments'] = ''
        Information['Directory'] = None
        Students[email] = Information
        Students[email]['FN'] = FN
        Students[email]['LN'] = LN
        
        
        cleanedFN =  re.sub("[^a-zA-Z0-9_-]","",FN)
        cleanedLN =  re.sub("[^a-zA-Z0-9_-]","",LN)
        
        for x in folderList:
            folderName = x.lower()
            
            if cross_reference_roster and email in moodleRoster: #some have a nickname in moodle. check to see if that name is listed
                cleanedMoodleFN = re.sub("[^ a-zA-Z0-9_-]","",moodleRoster[email]["FN"].lower())
                cleanedMoodleLN = re.sub("[^ a-zA-Z0-9_-]","",moodleRoster[email]["LN"].lower())
                firstNameInFolderName = (cleanedMoodleFN in folderName or cleanedFN in folderName)
                lastNameInFolderName = (cleanedMoodleLN in folderName or cleanedLN in folderName)
            else:
                firstNameInFolderName = cleanedFN in folderName
                lastNameInFolderName = cleanedLN in folderName
            if firstNameInFolderName and lastNameInFolderName:
                Students.get(email)['Directory'] = x
                
    return Students


