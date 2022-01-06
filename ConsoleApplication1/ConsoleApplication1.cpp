#include"Header.h"

int main()
{
	vector<double> ceva = readFromFile();
	for (double c : ceva)
	{
		cout << c << " ";
	}
	return 0;
}