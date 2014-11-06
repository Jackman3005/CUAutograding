import os

class SubmissionFinder:
    
    def __init__(self,acceptableExtensions = [".cpp",".cc",".c++"]):
        self.acceptableExtensions = acceptableExtensions
    
    def fileNameHasAcceptableExtensionAndRoughlyMatchesName(self,textToLookFor,fileName):
        if (len(fileName) < len(textToLookFor)):
            return False
        containsText = textToLookFor.lower() in fileName.lower()
        hasCorrectExtension = False
        for extension in self.acceptableExtensions:
            if (extension.lower() in fileName.lower()):
                hasCorrectExtension = True
                break
        
        isNotHiddenOrBackupFile = fileName[0] != '.' and fileName[0] != '~'
        
        return containsText and hasCorrectExtension and isNotHiddenOrBackupFile

    def findSubmission(self,submissionDirectory, simpleName):
        try:
            files = os.listdir(submissionDirectory)
            for file in files:
                if (self.fileNameHasAcceptableExtensionAndRoughlyMatchesName(simpleName,file)):
                    return file
            return False
                
        except Exception as e:
            print ("Error when looking for submission file...\n",e.strerror,file=sys.stderr)
            return False
