import subprocess
import sys

def compileCPPFile(sourceFileName,outputFileName,displayName):
    try:
        print("--------------Compiling " + displayName + " source code--------------",file=sys.stderr)
        subprocess.check_call("g++ \""+sourceFileName+"\" -std=c++11 -o \"" + outputFileName + "\"",stdout=sys.stderr,stderr=sys.stderr,shell=True) 
        return True
    except Exception:
        print("-------------ERROR WHILE COMPILING!------------",file=sys.stderr)
        return False