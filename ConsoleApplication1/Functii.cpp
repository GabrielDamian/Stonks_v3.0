#include"Header.h"


vector<double> readFromFile()
{
	vector<double> fileData;

	std::ifstream file("data.txt");
	std::string str;
	int contor = 0;
	while (std::getline(file, str)) {
		//std::cout << str << "\n";
		fileData.push_back(stof(str));  //stof converts str to double, stoi to int
	}

	return fileData;
}