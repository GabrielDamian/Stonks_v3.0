#include"Header.h"

int main()
{
	int size_seg_unic = 60;
	int min_max_streching = 0;
	int future_price = 10;

	vector<point> inputData = readFromFile(); 
	//printInputData(inputData); //TEST RAW DATA
	
	vector<vector<point>> segmente_baza;
	segmentareArray(segmente_baza, inputData, size_seg_unic);
	cout << endl << "S-au generat:" << segmente_baza.size() << " segment de baza.";
	//printSegmenteBaza(segmente_baza);

	

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
	//printVariatii(variatii);
	
	
	for (auto& a : variatii)
	{
		for (auto& b : a.second)
		{
			comprimaSegment(b.values, size_seg_unic);
		}
	}
	cout << endl << "----Variatii comprimate:" << endl;
	//printVariatii(variatii);


	for (auto& a : variatii)
	{
		for (auto& b : a.second)
		{
			interpoleazaSegment(b.values, size_seg_unic);
		}
	}
	cout << endl << "----Variatii comprimate si interpolate:" << endl;
	//printVariatii(variatii);


	cout << endl << "Start filtrare patterns:" << endl;
	vector<patterns> posibile_patterns;
	posibile_patterns.reserve(segmente_baza.size());
	int index_cout = 0;

	int decade = int(segmente_baza.size() / 100);
	int one_percent = 0;
	int mycounter = 0;
	for (auto& a : segmente_baza)
	{
		if (decade == mycounter)
		{
			mycounter = 0;
			one_percent++;
			cout << one_percent << "%" << endl;

		}
		mycounter++;
		
		index_cout++;

		if (checkIfStraightLine(a)) continue;
		
		//TODO - skip thi base segment if it is a straight line (function to check it)
		int scor_cadinal = 0;
		int positives = 0;


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
				if (crosssCorelation(base_copy_normalized,variatie.values) < abatere && abs(variatie.index - index_cout) > size_seg_unic )
				{
					//verifica daca in vector twin nu exista deja o variatie cu index apropiat de al tau inainte de a da push
					if (checkSimilarIndex(vector_twin, variatie,20))
					{
						//true, daca exista un index apropiat deja existen in vecto_twin
						//cout << endl << "skip";
					}
					else
					{
						//false daca indexul curent de la variatie este departat de oricare alt index
						//push in vector_twin
						vector_twin.push_back(variatie);
						scor_cadinal++;
						if (variatie.future_price != NULL && variatie.future_price > variatie.last_price) positives++;
					}
					
					
				}
			}
		}
		pattern_ref.scor = scor_cadinal;
		pattern_ref.positives = positives;
		pattern_ref.index = index_cout;
	}
	//SORT VARIATIONS - if in the x' variation laready exists an items with index close to yours, skip this one (in this case
	//only the firt variation will be keept in the variations.


	std::sort(posibile_patterns.begin(), posibile_patterns.end(), [](patterns const& a, patterns const& b)->bool //descending
		{
			return a.scor > b.scor;
		});
	cout << endl << endl << "==== Pattern finale desc ========";
	printPatterns(posibile_patterns);


	//TODO - add index value to the base segment and variations

	return 0;
}