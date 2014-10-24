import subprocess
import sys

def compileCPPFile(sourceFileName,outputFileName,displayName):
    try:
        print("--------------Compiling " + displayName + "--------------",sys.stderr)
        subprocess.check_call("g++ "+sourceFileName+" -std=c++11 -o " + outputFileName,shell=True) 
        return True
    except Exception:
        print("-------------ERROR WHILE COMPILING!------------",file=sys.stderr)
        return False