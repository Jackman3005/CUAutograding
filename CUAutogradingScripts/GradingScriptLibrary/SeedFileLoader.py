import sys
import shlex

class SeedFileLoader:
    
    def __init__(self, separator = ";"):
        self.separator = separator
        
    def loadSeedsFromFile(self,fileName):
        try:
            seedFile = open(fileName, "r")
        except Exception as e:
            print ("Exception was thrown when trying to open seed file: ", seedFile,"Error:\n",e.strerror)
            sys.exit(1)
        else:
            seeds = []
            for line in seedFile:
                if (line.lstrip()[0] == "#"): #Skip lines with a comment indicator at the start
                    continue;
                ioTokens = line.split(self.separator)
                if (len(ioTokens) < 3):
                    self.printSeedFileError(fileName)
                    sys.exit(1)
                commandLineArguments = self.cleanStrings(shlex.split(ioTokens[0]))  #Shlex splitting will keep strings within quotes as one input/output
                consoleInputs = self.cleanStrings(shlex.split(ioTokens[1]))
                expectedOutputs = self.cleanAndEvalStrings(shlex.split(ioTokens[2]))
                    
                seed = Seed(commandLineArguments,consoleInputs,expectedOutputs)
                seeds.append(seed)
            return seeds
                
    def cleanStrings(self,strings):
        returnStrings = []
        for string in strings:
            returnStrings.append(string.lstrip().rstrip())
        return returnStrings
    def cleanAndEvalStrings(self,strings):
        returnValues = []
        
        for string in self.cleanStrings(strings):
            value = string
            try:
                value = eval(string)
            except Exception:
                None
            returnValues.append(value)
        return returnValues
    
    
    def printSeedFileError(self,fileName):
        print ("Could not find CLA, Console Inputs, or Expected outputs for seed file:",fileName)
        print ("Expected to see seed file in the following format:\n")
        print ("CLA1 CLA2 CLA3..."+self.separator +" ConsoleIn1 ConsoleIn2 ConsoleIn3..."+self.separator +" ExpectedOut1 ExpectedOut2...")
        print ("You must put the '" + self.separator + "' separator in even if there are no inputs of that type")
            

class Seed:
    def __init__(self,commandLineInputs,consoleInputs,expectedOutputs):
        self._commandLineInputs = commandLineInputs
        self._consoleInputs = consoleInputs
        self._expectedOutputs = expectedOutputs
        
    def consoleInputs(self):
        return self._consoleInputs
    
    def commandLineInputs(self):
        return self._commandLineInputs
    
    def expectedOutputs(self):
        return self._expectedOutputs