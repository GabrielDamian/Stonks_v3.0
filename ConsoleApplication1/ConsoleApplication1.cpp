#include"Header.h"

int main()
{
	vector<point> inputData = readFromFile();
	/*for (auto a : inputData)
	{
		cout << a.x << " " << a.y << endl;
	}*/
	cout << "Start stage 2" << endl;
	
	int size_seg_unic = 10;
	int min_max_streching = 5;

	cout << "Start generare segmente de baza..." << endl;
	vector<vector<point>> segmente_baza;
	segmentareArray(segmente_baza, inputData, size_seg_unic);
	/*for (auto a : segmente_baza)
	{
		cout << endl << "arr nou:";
		for (auto b : a)
		{
			cout << " " << b.y;
		}
	}*/
	cout << "Succes.S-au generat:" << segmente_baza.size() << " segment de baza.(+ segmente normalizate)";
	cout << endl << "Start stage 3:" << endl;

	int future_price = 10;
	map<int, vector<twin>> variatii;
	seteazaKeyVariatii(variatii, size_seg_unic, min_max_streching);
	cout << endl << "Verificare chei in variatii:" << endl;

	for (auto a : variatii)
	{
		cout << "key:" << a.first << endl;
		segmentareVariatii_with_future_price(a.second, inputData, a.first, future_price);
	}





	/*for (int i = size_seg_unic - min_max_streching; i <= size_seg_unic + min_max_streching; i++)
	{
		cout << "min max:" << i << endl;
	}

	map<int, vector<int>> ceva;
	vector<int> test = { 1,2,3,4,5 };
	vector<int> test_2(test.size());
	transform(test.begin(), test.end(), test.begin(), [](int el) {
		return el * 2;
	});
	int contor = 0;
	std::copy_if(test.begin(), test.end(), test_2.begin(), [&contor](int i) {
		if (i % 2 == 0)
		{
			contor++;
		}
		return (i % 2 == 0); });
	
	test_2.resize(contor);

	for (auto a : test_2)
	{
		cout << a << " ";
	}
	ceva.insert(make_pair(1, test));
	for (auto a : ceva)
	{
		cout << a.first;

	}*/
	return 0;
}