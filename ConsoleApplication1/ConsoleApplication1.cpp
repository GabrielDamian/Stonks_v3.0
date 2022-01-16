#include"Header.h"

int main()
{
	vector<point> inputData = readFromFile(); //s-au aplicat deja prelucrari de filtrare candles si candlesToFunction
	/*for (auto a : inputData)
	{
		cout << a.x << " " << a.y << endl;
	}*/
	
	cout << "Start stage 2" << endl;
	
	int size_seg_unic = 10;
	int min_max_streching = 2;

	cout << "Start generare segmente de baza..." << endl;
	vector<vector<point>> segmente_baza;
	segmentareArray(segmente_baza, inputData, size_seg_unic);
	
	//cout << "Testare segmente de baza:" << endl;
	//for (auto a : segmente_baza)
	//{
	//	cout << endl << "arr nou:";
	//	for (auto b : a)
	//	{
	//		cout << " " << b.y << ",";
	//	}
	//}
	cout << "Succes.S-au generat:" << segmente_baza.size() << " segment de baza.(+ segmente normalizate)";
	cout << endl << "Start stage 3:" << endl;

	int future_price = 10;
	map<int, vector<twin>> variatii;
	/*{
		35: [{future_price: x, values:[point, point...]}, {}, {}]
		36: [{}, {}, {}]
		37: [{}, {}, {}]
		38: [{}, {}, {}]
	}*/
	seteazaKeyVariatii(variatii, size_seg_unic, min_max_streching); //populeaza doar keys in obiect (35,36,37..)

	cout << endl << "Populez variatii...";
	for (auto &a : variatii)
	{
		segmentareVariatii_with_future_price(a.second, inputData, a.first, future_price);
	}
	cout << endl << "Succes populare variatii.(Variatii normalizate)";


	//verificare populare variatii
	//CTRL+K+C	 
	//CTRL+K+U

//	printVariatii(variatii);

	/*{
		35: [{future_price: x, values:[point, point...]}, {}, {}]
		36: [{}, {}, {}]
		37: [{}, {}, {}]
		38: [{}, {}, {}]
	}*/
	cout << "Start comprima interpoleaza handler" << endl;
	for (auto& a : variatii)
	{
		cout << endl << "Current key:" << a.first;
		for (auto& b : a.second)
		{
			//comprima si interpoleaza
			comprimaSegment(b.values, size_seg_unic);
			//interpoleazaSegment(b.values, size_seg_unic);
		}
	}

	printVariatii(variatii);


	cout << endl << "Start interpolare variatii:";








	//TRASH TESTING
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