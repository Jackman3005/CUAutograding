#include <iostream>
#include <fstream>  //allows istream/ostream
#include <stdlib.h> //allows atoi

using namespace std;


struct lookingFor{
    //Five categories: bicycle, microwave, dresser, truck, or chicken
    string type;
    //For sale = true; wanted = false
    bool status;
    int price;
};

void printBoard(lookingFor sarray[], int asize){
    //cout << "The virtual yard sale currently contains: " << endl;
    string item;
    string wanted;
    int checkme;
    for(int i = 0; i < asize; i++){

        if(sarray[i].status){
            wanted = "For sale";
        }
        else{
            wanted = "Wanted";
        }
        cout << sarray[i].type << ", " << wanted  << ", " << sarray[i].price << endl;
    }

}

int main(int argc, char **argv){

    int opcount = 0;

    //Open files
    ifstream in_stream;
    ofstream out_stream;

    in_stream.open(argv[1]);
    opcount++;
    out_stream.open("sold.txt");
    opcount++;
    //Figure out how big the array needs to be
    int count1 = 0;
    string line;
    while (!in_stream.eof()){
        getline(in_stream, line);
        count1++;
        opcount++;
    }
    in_stream.close();
    in_stream.clear();//allows for reopening

    //Create an array of size = number of lines and populate with structs
    lookingFor sArray[count1];

    in_stream.open(argv[1]);
    opcount++;
    int count2 = 0;

    string obj;
    string stats;
    bool stat;
    string costS;
    int cost;
    bool alreadysold = false;
    while(!in_stream.eof()){
        //finds delimiter and puts preceding information into string
        getline(in_stream, obj, ',');
        getline(in_stream, stats, ',');
        getline(in_stream, costS); // "\n" is the default delimiter
        opcount++;
        if(obj == ""){ //catches that last line
            break;
        }
        cost = atoi(costS.c_str()); //convert to integer


        if((stats == " wanted")||(stats == " Wanted")||(stats == "wanted")){
            stat = false;
        }
        else{
            stat = true;
        }

        if(count2 >= 0){
        alreadysold = false;
        opcount++;
            for(int j = 0; j < count2; j++){
                if((sArray[j].type == obj) && (sArray[j].status != stat)){
                    if(sArray[j].status){
                    //for sale = true
                        if(cost >= sArray[j].price){
                            out_stream << obj << " sold for " << cost << ".\n";
                            //replace old struct and decrement the used size of array
                            opcount++;
                            sArray[j] = sArray[(count2-1)];

                            count2--;
                            alreadysold = true; //we can only sell once
                        }
                    }
                    else{
                    //wanted = false
                        if(cost <= sArray[j].price){
                            out_stream << obj << " sold for " << cost << ".\n";
                            //replace old struct and decrement the used size of array
                            opcount++;
                            sArray[j] = sArray[(count2-1)];

                            count2--;
                            alreadysold = true; //we can only sell once
                        }
                    }
                }
            if(alreadysold){
                break;
            }
            }
        }
        if (!alreadysold){
            //Now that we're done checking for matches, add to the array
            sArray[count2].price = cost;
            sArray[count2].status = stat;
            sArray[count2].type = obj;
            count2++;
        }


    }

    printBoard(sArray, count2);

    //cout << "\nThis used " << opcount << " operations." << endl;
    //Close files now that we're done with them
    in_stream.close();
    out_stream.close();
    return 0;
}


