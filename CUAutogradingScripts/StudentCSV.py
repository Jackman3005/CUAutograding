import csv

def makeCSV(Students,outputFileLocation):
    
    with open(outputFileLocation, 'w',newline='') as csvfile:
        HWGradeWriter = csv.writer(csvfile, delimiter=',')
        
        HWGradeWriter.writerow(['email','FirstName','LastName' , 'Grade','Comments'])
        for studentId in Students:    
            l = [studentId,str(Students[studentId]['FN']),str(Students[studentId]['LN']),str(Students[studentId]['Grade']),Students[studentId]['Comments']]
            HWGradeWriter.writerow(l)