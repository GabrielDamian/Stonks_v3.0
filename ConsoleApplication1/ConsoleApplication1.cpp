#include"Header.h"
//-->!!!!!<-- MANDATORY -> File data needs to be consecutive by x and start with index 0

int main()
{
	vector<point> inputData = readFromFile(); 
	//printInputData(inputData); //TEST RAW DATA
	
	int size_seg_unic = 50;
	int min_max_streching = 2;

	vector<vector<point>> segmente_baza;
	segmentareArray(segmente_baza, inputData, size_seg_unic);
	printSegmenteBaza(segmente_baza);
	

	cout <<endl<< "S-au generat:" << segmente_baza.size() << " segment de baza.(+ segmente normalizate)";

	int future_price = 10;
	map<int, vector<twin>> variatii;
	/*{
		35: [{future_price: x, values:[point, point...]}, {}, {}]
		36: [{}, {}, {}]
		37: [{}, {}, {}]
		38: [{}, {}, {}]
	}*/
	
	seteazaKeyVariatii(variatii, size_seg_unic, min_max_streching);
	
	for (auto &a : variatii)
	{
		segmentareVariatii_with_future_price(a.second, inputData, a.first, future_price);
	}
	
	for (auto& a : variatii)
	{
		for (auto& b : a.second)
		{
			comprimaSegment(b.values, size_seg_unic);
		}
	}


	for (auto& a : variatii)
	{
		for (auto& b : a.second)
		{
			interpoleazaSegment(b.values, size_seg_unic);
		}
	}
	
	vector<patterns> posibile_patterns;
	posibile_patterns.reserve(segmente_baza.size());
	int index_cout = 0;
	for (auto& a : segmente_baza)
	{
		int scor_cadinal = 0;

		index_cout++;

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
					scor_cadinal++;
				}
			}
		}
		pattern_ref.scor = scor_cadinal;
	}
	
	//descending
	std::sort(posibile_patterns.begin(), posibile_patterns.end(), [](patterns const& a, patterns const& b)->bool
		{
			return a.scor > b.scor;
		});

	return 0;
}