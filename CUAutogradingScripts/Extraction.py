import os
import subprocess

def ExtractSubmissions(submission_directory = os.getcwd()):
   
    files = os.listdir(submission_directory) #make list of folders in the directory
    
    for file in files:
        if (".zip" in file):
            ziploc = submission_directory + '/' + file
            
            nameOfStudent = file.split('_')[0]
            prompt_cmd = '7z e ' + '"' + ziploc + '"' + ' -o' + '"' + submission_directory + '/' + nameOfStudent + '" -y > NUL'
            subprocess.Popen(prompt_cmd, shell=True)

#submission_directory = 'Submissions'

#ExtractSubmissions(submission_directory)
