import sys
import subprocess

class ProgramRunner:
    
    def __init__(self,timeout=5):
        self._timeout = timeout
        
        
    def run (self,fileName, commandLineArguments, consoleInputs):
        print("Running "+fileName+" with command line arguments: " + " ".join(commandLineArguments), file=sys.stderr)
        print("and console inputs of: " + ", ".join(consoleInputs))
        
        if (fileName[0] != "/"): #Check if it is a relative path or not
            fileName = "./" + fileName
        
        try:
            commandLineArgsToPass = [fileName]
            if (len(commandLineArguments) > 0):
                commandLineArgsToPass.extend(commandLineArguments)
            
            process = subprocess.Popen(commandLineArgsToPass,stdout=subprocess.PIPE, stdin=subprocess.PIPE,shell=True)
            out,err = process.communicate(("\n".join(consoleInputs)).encode(),timeout=self._timeout)
            return (True,out.decode())
        except subprocess.CalledProcessError as err:
            print("Error running submission: {!s}".format(err), file=sys.stderr)
            return (False,"Runtime Error occurred when running " + fileName)
        except subprocess.TimeoutExpired:
            errMessage = fileName + " took longer than "+self._timeout+" seconds to run. Most likely an infinite loop or prompt for input!"
            print (errMessage,file=sys.stderr)
            return (False, errMessage)