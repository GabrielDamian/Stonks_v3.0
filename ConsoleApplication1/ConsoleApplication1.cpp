#include"Header.h"

int main()
{
	int size_seg_unic = 30;
	int min_max_streching = 2;
	int future_price = 10;

	vector<point> inputData = readFromFile(); 
	printInputData(inputData); //TEST RAW DATA
	
	vector<vector<point>> segmente_baza;
	segmentareArray(segmente_baza, inputData, size_seg_unic);
	cout << endl << "S-au generat:" << segmente_baza.size() << " segment de baza.";
	printSegmenteBaza(segmente_baza);

	

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
	cout << endl << "---Variatii default:" << endl;
	printVariatii(variatii);
	
	
	for (auto& a : variatii)
	{
		for (auto& b : a.second)
		{
			comprimaSegment(b.values, size_seg_unic);
		}
	}
	cout << endl << "----Variatii comprimate:" << endl;
	printVariatii(variatii);


	for (auto& a : variatii)
	{
		for (auto& b : a.second)
		{
			interpoleazaSegment(b.values, size_seg_unic);
		}
	}
	cout << endl << "----Variatii comprimate si interpolate:" << endl;
	printVariatii(variatii);


	vector<patterns> posibile_patterns;
	posibile_patterns.reserve(segmente_baza.size());
	int index_cout = 0;
	for (auto& a : segmente_baza)
	{
		int scor_cadinal = 0;

		index_cout++;

		posibile_patterns.emplace_back();
		patterns& pattern_ref = posibile_patterns[posibile_patterns.size() - 1];

		vector<point> base_copy_normalized = a;
		normalizeazaSegment(base_copy_normalized);
		pattern_ref.seg_baza = base_copy_normalized;
		
		for (auto& b : variatii)
		{
			pattern_ref.variatii_filtrate[b.first] = vector<twin>();
			vector<twin>& vector_twin = pattern_ref.variatii_filtrate.at(b.first);

			for (auto& variatie : variatii.at(b.first))
			{
				if (crosssCorelation(base_copy_normalized,variatie.values) < abatere)
				{
					vector_twin.push_back(variatie);
					scor_cadinal++;
				}
			}
		}
		pattern_ref.scor = scor_cadinal;
	}
	std::sort(posibile_patterns.begin(), posibile_patterns.end(), [](patterns const& a, patterns const& b)->bool //descending
		{
			return a.scor > b.scor;
		});
	//TODO - cout variatii filtrate si sortate desc
	cout << endl << endl << "==== Pattern finale desc ========";
	printPatterns(posibile_patterns);


	//TODO - add index value to the base segment and variations
	//TODO - fix future price value
	//TODO - add succes ratio to each final base filtered patter (positive_future_price / variations.size())

	return 0;
}