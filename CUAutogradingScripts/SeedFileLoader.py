import sys

class SeedFileLoader:
    
    def __init__(self, separator = ";"):
        self.separator = separator
        
    def loadSeedsFromFile(self,fileName):
        seedFile = open(fileName, "r")
        seeds = []
        for line in seedFile:
            ioTokens = line.split(self.separator)
            if (ioTokens < 3):
                self.printSeedFileError(fileName)
                sys.exit(1)
            commandLineArguments = ioTokens[0].split()
            consoleInputs = ioTokens[1].split()
            expectedOutputs = ioTokens[2].split()
            seed = Seed(commandLineArguments,consoleInputs,expectedOutputs)
            seeds.append(seed)
        return seeds
            
                
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