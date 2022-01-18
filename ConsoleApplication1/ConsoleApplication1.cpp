#include"Header.h"
//-->!!!!!<-- MANDATORY -> File data needs to be consecutive by x and start with index 0

int main()
{
	vector<point> inputData = readFromFile(); 
	//printInputData(inputData);
	

	//********** STAGE 2 **********
	cout << "Start stage 2" << endl;
	
	int size_seg_unic = 10;
	int min_max_streching = 2;

	cout << "Start generare segmente de baza..." << endl;
	
	vector<vector<point>> segmente_baza;
	segmentareArray(segmente_baza, inputData, size_seg_unic);
	//printSegmenteBaza(segmente_baza);
	
	cout <<endl<< "Succes.S-au generat:" << segmente_baza.size() << " segment de baza.(+ segmente normalizate)";

	//********** STAGE 3 **********
	cout << endl << "Start stage 3:" << endl;

	int future_price = 10;
	map<int, vector<twin>> variatii;
	/*{
		35: [{future_price: x, values:[point, point...]}, {}, {}]
		36: [{}, {}, {}]
		37: [{}, {}, {}]
		38: [{}, {}, {}]
	}*/
	
	seteazaKeyVariatii(variatii, size_seg_unic, min_max_streching);
	cout << endl << "Key variatii setate cu succes.";
	cout << endl << "Populez variatii...";
	
	for (auto &a : variatii)
	{
		segmentareVariatii_with_future_price(a.second, inputData, a.first, future_price);
	}
	cout << endl << "Succes populare variatii.(Variatii normalizate)";


	//printVariatii(variatii);

	cout << endl << "Start comprimare variatii:" << endl;
	for (auto& a : variatii)
	{
		cout << endl << "current key:" << a.first;
		for (auto& b : a.second)
		{
			comprimaSegment(b.values, size_seg_unic);
		}
	}

	cout << endl << "Start interpolare variatii:" << endl;
	
	for (auto& a : variatii)
	{
		for (auto& b : a.second)
		{
			interpoleazaSegment(b.values, size_seg_unic);
		}
	}

	//printVariatii(variatii);
	// 
	//********** STAGE 4 **********
	
	vector<patterns> posibile_patterns;
	posibile_patterns.reserve(segmente_baza.size());
	int index_cout = 0;
	for (auto& a : segmente_baza)
	{
		posibile_patterns.emplace_back();
		patterns& pattern_ref = posibile_patterns[posibile_patterns.size() - 1];

		pattern_ref.seg_baza = a;
		
		for (auto& b : variatii)
		{
			pattern_ref.variatii_filtrate[b.first] = vector<twin>();
			vector<twin>& vector_twin = pattern_ref.variatii_filtrate.at(b.first);

			for (auto& variatie : variatii.at(b.first))
			{
				if (crosssCorelation(a,variatie.values) < abatere)
				{
					vector_twin.push_back(variatie);
				}
			}
		}
	}
	
	//#TEST posibile patterns;
	/*
	cout << endl<<"DAMN BOYY";
	for (auto& a : posibile_patterns)
	{
		cout << endl << "--posibil nou pattern:" << endl;
		for (auto& b : a.seg_baza)
		{
			cout << "(" << b.x << "," << b.y << "), ";
		}
		cout << endl << "Cu variatiile:" << endl;
		for (auto& c : a.variatii_filtrate)
		{
			cout << c.first << ":";
			for (auto& d : c.second)
			{
				//bad, but just tesing
				cout << endl;
				for (auto& e : d.values)
				{
					cout << "(" << e.x << "," << e.y << "), ";
				}
			}
			cout << endl << endl;
		}
	}

	*/
	cout << "DAMN BOY, it's done in time.!!!";


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