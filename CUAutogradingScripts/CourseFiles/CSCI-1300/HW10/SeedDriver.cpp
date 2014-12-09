
//Leave line 1 blank so the grader can append in the users library.cpp class name

int main (int argv, char* argc[] )
{
	// -------------------------------------------------------------
	// PART 3
	// 	Purpose: Create the library
	//			 read in books and users files 
	//			 & store data into lists
	// -------------------------------------------------------------
	string bookListFilename = argc[1];
	string userRatingsFilename = argc[2];
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
