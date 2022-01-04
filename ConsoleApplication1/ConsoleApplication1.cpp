
#include <iostream>
#include <vector>
using namespace std;

int main()
{

	vector<int> test_vector;

	test_vector.push_back(10);
	test_vector.push_back(11);

	for (int el : test_vector)
	{
		cout << el << " ";
	}

}
