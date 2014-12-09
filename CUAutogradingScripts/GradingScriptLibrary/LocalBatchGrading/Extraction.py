import os
import subprocess
import sys

def ExtractSubmissions(submission_directory = os.getcwd()):
   
    files = os.listdir(submission_directory) #make list of folders in the directory
    
    for file in files:
        if (".zip" in file):
            ziploc = submission_directory + '/' + file
            
            nameOfStudent = file.split('_')[0]
            prompt_cmd = '7z e ' + '"' + ziploc + '"' + ' -o' + '"' + submission_directory + '/' + nameOfStudent + "\" -y >/dev/null"
            subprocess.Popen(prompt_cmd, stdout=sys.stderr,stderr=sys.stderr,shell=True)
        
    
    possibleIssuesWithUnizipping = subprocess.check_output("find \""+submission_directory+"\" -mindepth 2 -name *.zip*",shell=True).decode()
    if (len(possibleIssuesWithUnizipping) > 0):
        print("\n\nWARNING: The following files were not fully unzipped! Most likely a zip inside a zip!\n",possibleIssuesWithUnizipping)

#submission_directory = 'Submissions'

#ExtractSubmissions(submission_directory)

#brett was here