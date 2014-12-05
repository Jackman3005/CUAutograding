#include "Library.cpp"


int main ()
{
	// -------------------------------------------------------------
	// PART 3
	// 	Purpose: Create the library
	//			 read in books and users files 
	//			 & store data into lists
	// -------------------------------------------------------------
	string bookListFilename = "books.txt";
	string userRatingsFilename = "ratings.txt";
	Library library(bookListFilename, userRatingsFilename);

	//print out the users for the library
	// USE FOR DEBUGGING PURPOSES
	//cout << "Library users: " << endl;
	//library.printUsers();
		
		
	// -------------------------------------------------------------
	// PART 4
	//		Purpose: Print the average ratings for each book
	// -------------------------------------------------------------
	cout << "\n\nBooks and average ratings: " << endl;
	library.printAverageBookRatings();
}
