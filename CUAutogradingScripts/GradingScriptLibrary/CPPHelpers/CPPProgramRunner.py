import sys
import subprocess

class CPPProgramRunner:
    
    def __init__(self,timeout=5):
        self._timeout = timeout
        
        
    def run (self,fileName, commandLineArguments, consoleInputs):
        print("Running "+fileName+" with command line arguments: " + " ".join(commandLineArguments), file=sys.stderr)
        if (len(consoleInputs)>0):
            print("and console inputs of: " + ", ".join(consoleInputs),file=sys.stderr)
        
        if (fileName[0] != "/"): #Check if it is a relative path or not
            fileName = "./" + fileName
        
        try:
            commandLineArgsToPass = [fileName]
            if (len(commandLineArguments) > 0):
                commandLineArgsToPass.extend(commandLineArguments)
                
            #Two different ways to run the program. If there are no console inputs then the first way does not seem to work.
            if (len(consoleInputs)>0):
                process = subprocess.Popen(commandLineArgsToPass,stdout=subprocess.PIPE, stdin=subprocess.PIPE,shell=True)
                out,err = process.communicate(("\n".join(consoleInputs)).encode(),timeout=self._timeout)
                return (True,out.decode())
            else:
                output = subprocess.check_output(commandLineArgsToPass,timeout=self._timeout)
                return (True,output.decode())
        except subprocess.CalledProcessError as err:
            print("Error running submission: {!s}".format(err), file=sys.stderr)
            return (False,"Runtime Error occurred when running " + fileName)
        except subprocess.TimeoutExpired:
            errMessage = fileName + " took longer than "+self._timeout+" seconds to run. Most likely an infinite loop or an unexpected prompt for input!"
            print (errMessage,file=sys.stderr)
            return (False, errMessage)