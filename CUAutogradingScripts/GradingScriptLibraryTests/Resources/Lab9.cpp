// Don't forget to compile using the c++11 std

#include<iostream>
#include<fstream>
using namespace std;

int main (){

    string nameOfPercentagesFile = "gradePercentages.txt";
    string nameOfGradesFile = "gradeScores.txt";
    
    ifstream inputFileStream1;
    ifstream inputFileStream2;
    
    inputFileStream1.open(nameOfPercentagesFile,ios::in);
    
    double gradePercentages[50]; //Arbitrarily large array
    string line;
    
    int numCategories = 0;
    //For loop is has three parts for(INITIALIZATION; CONDITION; INCREMENT/DECREMNT)
    //Because I have initialized numCategories before the loop I do not need to do it in the
    //Definition. Also note my conditional is not dependent on my numCategories variable
    //Read line from inputFileStream and store it in "line" variable. Will return false when the inputFileStream is empty
    for( ; getline(inputFileStream1,line); numCategories++) 
    {
        int indexOfSpace = line.find(" ");  //Because there is no split function we must search for the first occurance of a space 
        string percentageString = line.substr(indexOfSpace+1,3); //Now we will extract the part of the string after the space up to 3 in length
        double percentage = stoi(percentageString);
        gradePercentages[numCategories] = percentage;
    }
    inputFileStream1.close();  //Don't forget to close your file Streams!
    
    inputFileStream2.open(nameOfGradesFile,ios::in);
    double averageGradeForCategory[50]; //Arbitrarily large array
    
    for(int i = 0 ; getline(inputFileStream2,line); i++) 
    {
        double gradesForThisCategory[50]; //Hold onto an array of each grade in the category in order to do an average
        int currentIndex = 0;
        int indexOfNextSpace;
        int countOfGrades = 0;
        //line.find(SEPARATOR,INDEX_TO_START_LOOKING_FROM)
        while ((indexOfNextSpace = line.find(" ",currentIndex)) != -1) //This will loop until there is no longer a space found
        {
            int lengthOfToken = indexOfNextSpace - currentIndex;
            string token = line.substr(currentIndex,lengthOfToken);
            double grade = stoi(token);
            gradesForThisCategory[countOfGrades] = grade;
            countOfGrades++;
            currentIndex = indexOfNextSpace+1; //We add one to make sure we skip the space we've already found
        }
        // This 'if' is necessary to get the last number in a line. Since the \n is not found when looking for the space
        if (currentIndex < line.size()-1) //If our current index is not already at the end of the line
        {
            int lengthOfToken = line.size() - currentIndex ;
            string token = line.substr(currentIndex,lengthOfToken);
            double grade = stoi(token);
            gradesForThisCategory[countOfGrades] = grade;
            countOfGrades++;
        }
        //Add up all the grades for the category
        double sumOfGrades = 0;
        for (int i = 0; i < countOfGrades; i++)
        {
            sumOfGrades += gradesForThisCategory[i];
        }
        
        averageGradeForCategory[i] = sumOfGrades/countOfGrades; //Store the average grade for the category
    }
    inputFileStream2.close();  //Don't forget to close your file Streams!
    
    double finalGrade = 0;
    for (int i = 0; i < numCategories; i++)
    {
        finalGrade += averageGradeForCategory[i] * (gradePercentages[i] /100);
    }
    
    cout.precision(1);
    cout << fixed << "Final Grade: " << finalGrade << "%" << endl;


}
