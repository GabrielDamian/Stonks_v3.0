#include "Header.h"
#include <iomanip>
#include <cmath>
#include <mutex>
#include <sstream>


void narutoMain(int candles_size, int size_seg_unic, floatType filter_1, floatType filter_2, int future_price, int min_max_streching, int abatere, std::mutex& mutex_file_main, std::mutex& mutex_file_terraForm, std::mutex& mutex_file_Apollo, std::mutex& mutex_console)
{

	//params checked

	{
		std::unique_lock<std::mutex> lock(mutex_console);
		std::cout << endl << "candle size :" << candles_size;
		std::cout << endl << "size_seg_unic :" << size_seg_unic;
		std::cout << endl << "filter_1 :" << filter_1;
		std::cout << endl << "filter_2 :" << filter_2;
		std::cout << endl << "future_price :" << future_price;
		std::cout << endl << "min_max_streching :" << min_max_streching;
		std::cout << endl << "abatere :" << abatere;
	}

	vector<point> inputData;

	{
		std::unique_lock<std::mutex> lock(mutex_file_main);
		inputData = pythonHandler("AAPL.csv", "main_data.txt", candles_size, filter_1, filter_2);
	}
	
	bool yScalerEnabler = true;
	bool powerSumCrossCor = true;

	//printInputData
	/*{
		std::unique_lock<std::mutex> lock(mutex_console);
		printInputData(inputData);
	}*/

	vector<vector<point>> segmente_baza;
	segmentareArray(segmente_baza, inputData, size_seg_unic);
	/*{
		std::unique_lock<std::mutex> lock(mutex_console);
		std::cout << endl << "S-au generat:" << segmente_baza.size() << " segment de baza.";
	}*/

	/*{
		std::unique_lock<std::mutex> lock(mutex_console);
		printSegmenteBaza(segmente_baza);
	}*/

	map<int, vector<twin>> variatii;
	
	std::cout << endl << "step 2";

	seteazaKeyVariatii(variatii, size_seg_unic, min_max_streching);
	for (auto& a : variatii)
	{
		segmentareVariatii_with_future_price(a.second, inputData, a.first, future_price);
	}
	//std::cout << endl << "------------Variatii default:" << endl;
	//printVariatii(variatii);

	//comprimare X
	for (auto& a : variatii)
	{
		for (auto& b : a.second)
		{
			comprimaSegment_X(b.values, size_seg_unic);
		}
	}

	//std::cout << endl << "------------Variatii comprimate : " << endl;
	//printVariatii(variatii);

	for (auto& a : variatii)
	{
		for (auto& b : a.second)
		{
			interpoleazaSegment(b.values, size_seg_unic);
		}
	}
	//std::cout << endl << "------------Variatii comprimate si interpolate:" << endl;
	//printVariatii(variatii);
	
	std::cout << endl << "step 3";
	
	//std::cout << endl << "Start filtrare patterns:" << endl;

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
			std::cout << one_percent << "%" << endl;
		}
		mycounter++;

		index_cout++;

		if (checkIfStraightLine(a)) continue;

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
				if (crosssCorelation(base_copy_normalized, variatie.values, yScalerEnabler, powerSumCrossCor) < abatere && abs(variatie.index - index_cout) > int(size_seg_unic / 2))
				{
					//verifica daca in vector twin nu exista deja o variatie cu index apropiat de al tau inainte de a da push
					if (checkSimilarIndex(vector_twin, variatie, 20)) //20 - nu vr sa am indexes mai apropiate intre ele
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
						if (variatie.future_price != 0 && variatie.future_price > variatie.last_price) positives++;
					}
				}
			}
		}
		pattern_ref.scor = scor_cadinal;
		pattern_ref.positives = positives;
		pattern_ref.index = index_cout;
	}
	//cout << endl << "step 4";
	//!!! CHECK POINT

	/*{
		std::unique_lock<std::mutex> lock(mutex_console);
		std::cout << endl << "before sort length:" << posibile_patterns.size() << endl;
	}*/

	std::sort(posibile_patterns.begin(), posibile_patterns.end(), [](patterns const& a, patterns const& b)->bool //descending
	{
		return a.scor > b.scor;
	});

	//printPatterns(posibile_patterns);
	//!!! CHECK POINT

	/*{
		std::unique_lock<std::mutex> lock(mutex_console);
		std::cout << endl << "after sort:" << posibile_patterns.size() << endl;
	}*/

	//vector<floatType> possible_succes_ratios = {50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0};

	vector<floatType> possible_succes_ratios = {70.0};
	
	for (auto a : possible_succes_ratios)
	{
		
		vector<patterns> current_filtered_patterns = filterBySuccesRatio(a, posibile_patterns);
		std::cout << endl << "au intrat:" << posibile_patterns.size();
		std::cout << endl << "au iesit:" << current_filtered_patterns.size();

		{
			std::unique_lock<std::mutex> lock(mutex_console);
			std::cout << endl << "current_filtered_patterns.size():" << current_filtered_patterns.size() << " succ_ratio:" << a;
			//printPatterns(current_filtered_patterns);
		}

		if (current_filtered_patterns.size() > 0)//if there are not patterns, supremeTest will throw a error bcs of crossCorelation
		{
			supremeTestMaster(current_filtered_patterns, a, candles_size, size_seg_unic, filter_1, filter_2, future_price, min_max_streching, abatere, mutex_file_terraForm, mutex_file_Apollo, mutex_console);
		}
	}
	std::cout << endl << "end of possible succes ratios";
	
	//cin.ignore();
}
vector<patterns> filterBySuccesRatio(int filter_succes_ratio, vector<patterns> posibile_patterns)
{
	vector<patterns> patterns_filtrate;

	for (auto& a : posibile_patterns)
	{
		floatType current_succes_ratio;
		if (a.positives == 0)
		{
			current_succes_ratio = 0;
		}
		else
		{
			current_succes_ratio = (floatType)(a.positives * 100) / a.scor;
		}
		/*{
			std::unique_lock<std::mutex> lock(mutex_console);
			cout << endl << "current_succes_ratio" << current_succes_ratio << " -> comparat cu ->" << filter_succes_ratio << " positive:" << a.positives;
		}*/
		if (current_succes_ratio > filter_succes_ratio)
		{
			//std::cout << "ratio:" << current_succes_ratio << " " << a.scor << endl;
			patterns_filtrate.push_back(a);
		}
	}
	return patterns_filtrate;
}
vector<point> readFromFile(int howMany, string source)
{
	//howMany == 1 (read all)
	vector<point> fileData;

	floatType a;
	floatType b;
	std::ifstream infile(source);

	if (howMany == 1)
	{
		while (infile >> a >> b)
		{
			point temp_point;
			temp_point.x = a;
			temp_point.y = b;
			fileData.push_back(temp_point);
		}
	}
	else
	{
		int counter = 0;
		while (counter <= howMany && infile >> a >> b)
		{
			point temp_point;
			temp_point.x = a;
			temp_point.y = b;
			fileData.push_back(temp_point);
			counter++;
		}
	}
	return fileData;
}
void segmentareArray(vector<vector<point>>& result, vector<point>& inputData, int size_seg_unic)
{
	int index = 0;
	int size_arr = inputData.size();

	for (auto el = inputData.begin(); el != inputData.end(); ++el)
	{
		int index = distance(inputData.begin(), el);
		//cout << index << " " << (*el).x << " " << (*el).y << endl;

		if (index < size_arr - size_seg_unic - 1)
		{
			vector<point> buffer;
			int index_buffer = index;
			while (buffer.size() < size_seg_unic)
			{
				buffer.push_back(inputData[index_buffer]);
				index_buffer++;
			}
			/*cout << endl << "Before normalizare:" << endl;
			for (auto a : buffer)
			{
				cout << a.x<<"," <<a.y<<" ";
			}
			cout << endl << "After normalization:" << endl;*/
			
			normalizeazaSegment(buffer);
			
			/*for (auto a : buffer)
			{
				cout << a.x << "," << a.y << " ";
			}
			*/
			result.push_back(buffer);
		}
		else
		{
			//nu mai pot incadra inca un segment
		}

	}
}
void normalizeazaSegment(vector<point>& segment)
{
	floatType min_x = segment[0].x;
	floatType min_y = segment[0].y;

	for (auto a : segment)
	{
		if (a.x < min_x)
		{
			min_x = a.x;
		}
		if (a.y < min_y)
		{
			min_y = a.y;
		}
	}

	for (int i = 0; i < segment.size(); ++i)
	{
		segment[i].x = segment[i].x - min_x;
		segment[i].y = segment[i].y - min_y;
	}
}
void seteazaKeyVariatii(map<int, vector<twin>>& variatii, int size_seg_baza, int min_max_streching)
{
	for (int i = size_seg_baza - min_max_streching; i <= size_seg_baza + min_max_streching; ++i)
	{
		vector<twin> temp_vector_twin;
		variatii.insert(make_pair(i, temp_vector_twin));
	}
}
void segmentareVariatii_with_future_price(vector<twin>& result, vector<point>& inputData, int size_variatie,int future_price)
{
	//toate segmentele pentru o cheie de variatie (ex:35,36..)
	vector<twin> result_data;

	//int index = 0;
	int size_arr = inputData.size();

	for (auto el = inputData.begin(); el != inputData.end(); ++el)
	{
		int index = distance(inputData.begin(), el);
		//cout << index << " " << (*el).x << " " << (*el).y << endl;

		if (index < size_arr - size_variatie - 1)
		{
			vector<point> buffer;
			int index_buffer = index;
			while (buffer.size() < size_variatie)
			{
				buffer.push_back(inputData[index_buffer]);
				index_buffer++;
			}
			//salveaza aici intr-o prop la fel ca future_price, un last_value_before_normalization
			//necesara pentru a compara daca pretul a crescut sau a scazut cu valoarea dinainte normalizare
			
			floatType last_price_default = buffer[buffer.size() - 1].y;
			normalizeazaSegment(buffer);
			twin temp_struct;
			temp_struct.values = buffer;



			//conditie de extragere future_price
			if (index + future_price < inputData.size() - 1)
			{
				temp_struct.future_price = inputData[index].y;
				temp_struct.last_price = last_price_default;
			}
			else
			{
				temp_struct.future_price = 0;
			}
			temp_struct.index = index;
			result.push_back(temp_struct);
		}
		else
		{
			//nu mai pot incadra inca un segment
		}

	}
}

void comprimaSegment_X(vector<point>& result, int comprimed_size)
{
	//comprimed_size = 10
	// 
	//from size = 5
	//from size = 15

	floatType ratio = comprimed_size / (floatType)(result.size() - 1);
	transform(result.begin(), result.end(), result.begin(), [ratio](point el) {
		el.x *= ratio;
		return el;
		});

}
void interpoleazaSegment(vector<point>& segment_factorizat, int comprimed_size)
{
	std::cout << setprecision(2);
	std::cout << fixed;

	vector<point> segment_rezultat;

	vector<floatType> x_segment_referinta; //range(0,comprimed_size)
	vector<floatType> x_segment_factorizat; //doar x's

	int temp_index = 0;
	while (temp_index < comprimed_size)
	{
		x_segment_referinta.push_back(temp_index);
		temp_index++;
	}

	for (auto a : segment_factorizat)
	{
		x_segment_factorizat.push_back(a.x);
	}

	for (auto a : x_segment_referinta)
	{
		floatType x_curent = a;
	
		auto it = find(x_segment_factorizat.begin(), x_segment_factorizat.end(), x_curent);
		if (it != x_segment_factorizat.end())
		{
			point x_y_factorizat_aferent;

			auto temp_it = find_if(segment_factorizat.begin(), segment_factorizat.end(), [=](point i) { return x_curent == i.x; });

			if (temp_it != segment_factorizat.end()) {
				point pereche_noua = {};
				pereche_noua.x = x_curent;
				pereche_noua.y = temp_it->y;
				segment_rezultat.push_back(pereche_noua);
			}
		}
		else
		{
			point prev_index = segment_factorizat[0];
			point next_index;
			int index = 1;
			while (index < segment_factorizat.size())
			{
				next_index = segment_factorizat[index];
				if (prev_index.x < x_curent && x_curent < next_index.x)
				{
					point pereche_noua = {};
					pereche_noua.x = x_curent;
					pereche_noua.y = yEcuatieDreapta(prev_index, next_index, x_curent);
					segment_rezultat.push_back(pereche_noua);
					break;
				}
				else
				{
					index += 1;
					prev_index = next_index;
				}
			}
		}
	}


	if (segment_rezultat.size() < segment_rezultat.size())
	{
		point last_item;
		last_item.x = x_segment_referinta[x_segment_referinta.size() - 1];
		last_item.y = segment_factorizat[segment_factorizat.size() - 1].y;

		segment_rezultat.push_back(last_item);
	}

	segment_factorizat = segment_rezultat;
}

floatType yEcuatieDreapta(point point_a, point point_b, floatType x_value)
{
	floatType x0 = point_a.x;
	floatType y0 = point_a.y;
	floatType x1 = point_b.x;
	floatType y1 = point_b.y;

	floatType x = x_value;

	floatType y = (y0 * (x1 - x) + y1 * (x - x0)) / (x1 - x0);

	return y;
}

floatType crosssCorelation(const vector<point>& base, const vector<point>& seg_2, bool yScalerEnabler, bool powerSum)
{
	//!! seg_1.size() == seg_2.size();
	
	if (yScalerEnabler)
	{
		floatType max_y_var = seg_2[0].y;
		for (auto& a : seg_2)
		{
			if (a.y > max_y_var) max_y_var = a.y;
		}

		floatType max_y_base = base[0].y;
		for (auto& a : base)
		{
			if (a.y > max_y_base) max_y_base = a.y;
		}

		floatType y_ratio = max_y_base / max_y_var;
		
		/*vector<point> scaled_variation;
		scaled_variation.reserve(seg_2.size());
		for (auto& a : seg_2)
		{
			point new_point;
			new_point.x = a.x;
			new_point.y = a.y * y_ratio;
			scaled_variation.push_back(new_point);
		}*/

		//cross cor with scaled y variation
		floatType suma_scaled = 0;
		int i = 0;
		while (i < base.size())
		{
			floatType var = base[i].y - seg_2[i].y * y_ratio;

			if (powerSum)
			{
				suma_scaled += var * var;
			}
			else
			{
				suma_scaled += abs(var);
			}
			i++;
		}
		//cout << "suma cross:" << suma_scaled << endl;
		return suma_scaled;
	}
	else
	{
		floatType suma = 0;
		int i = 0;
		while (i < base.size())
		{
			floatType var = abs(base[i].y - seg_2[i].y);
			suma += var;
			if (powerSum)
			{
				suma += var * var;
			}
			else
			{
				suma += var;
			}
			i++;
		}
		//cout << "suma cross:" << suma << endl;
		return suma;
	}
}
bool checkIfStraightLine(vector<point> segment)
{
	floatType sample = abs(segment[0].y - segment[1].y);
	floatType neighborhood_range = 0.5; //use case-ul in care punctele sunt pe o dreapta este caracterizat de faptul ca y's sunt incrementati cu acelasi offset
	
	for (int i = 0; i < segment.size() - 2; i++)
	{
		if (abs(segment[i].y - segment[i + 1].y) > sample + neighborhood_range)
		{
			return false;
		}
	}
	return true;
}
bool checkSimilarIndex(vector<twin>& vector_twin, twin variatie, int how_far)
{
	//cout << "verifica index:" << variatie.index << " in vector twin";
	for (auto& a : vector_twin)
	{
		if (abs(a.index - variatie.index) < how_far)
		{
			return true;
		}
	}
	return false;
}
//Test functions:
void printInputData(vector<point>& inputData)
{
	int how_many = 1000;
	int now = 0;
	for (auto a : inputData)
	{
		if (now > how_many) break;
		now++;
		//cout << "[" << a.x << " " << a.y << "], ";
		std::cout << a.y << ", ";
	}
}
void printSegmenteBaza(vector<vector<point>>& segmente_baza)
{
	std::cout << std::fixed;
	std::cout << std::setprecision(1);

	std::cout <<endl<< "Testare segmente de baza:" << endl;
	int how_many = 10;
	int now = 0;
	for (auto a : segmente_baza)
	{
		std::cout << endl << " NEW:" << endl;

		if (now > how_many) break;
		now++;
		for (auto b : a)
		{
			//cout << "[" << b.x << "," << b.y << "], ";
			std::cout << b.y << ",";
		}
	}
}
void printVariatii(map<int, vector<twin>>& variatii)
{
	std::cout << setprecision(2);
	std::cout << fixed;

	for (auto& a : variatii)
	{
		std::cout << endl << endl << "-->key:" << a.first << " size arr variatii:" << a.second.size();
		
		int how_many = 5;
		int now = 0;
		
		for (auto& b : a.second)
		{
			if (now > how_many) break;
			now++;
			std::cout << endl << "Len=" << b.values.size() << " ";
			for (auto& c : b.values)
			{
				//cout << "[" << c.x << "," << c.y << "], ";
				std::cout << c.y << ", ";
			}
			std::cout << endl <<endl<<"Future price:" << b.future_price;
			std::cout << endl << "Last price:" << b.last_price;
			std::cout << endl << "index:" << b.index << endl;
		}
	}
}
void printPatterns(vector<patterns> posibile_patterns)
{
	int how_many = 100;
	int now = 0;
	for (auto& a : posibile_patterns)
	{
		if (now > how_many) break;
		now++;

		std::cout << endl << endl << "----Patten: " << endl;
		printInputData(a.seg_baza);
		
		std::cout << endl << "score:" << a.scor;
		std::cout << endl << "positives:" << a.positives;
		std::cout << endl << "index:" << a.index << endl;

		std::cout << endl << "Variatii filtrate:";
		printVariatii(a.variatii_filtrate);

	}
}

//SUPREME TEST
void supremeTestMaster(vector<patterns> patternsParam, floatType succes_ratio_filter, int candles_size, int size_seg_unic, floatType filter_1, floatType filter_2, int future_price, int min_max_streching, int abatere, std::mutex& mutex_file_terraForm, std::mutex& mutex_file_Apollo, std::mutex& mutex_console)
{
	string farm_locations[] = { 
		/*"FarmLand/Test_3_0.csv",
		"FarmLand/Test_3_1.csv",
		"FarmLand/Test_3_2.csv",
		"FarmLand/Test_3_3.csv",
		"FarmLand/Test_3_4.csv",
		"FarmLand/Test_3_5.csv",
		"FarmLand/Test_3_6.csv",
		"FarmLand/Test_3_7.csv",
		"FarmLand/Test_3_8.csv",
		"FarmLand/Test_3_9.csv",*/

		"FarmLand/Test_4_0.csv",

		"FarmLand/LastWeek.csv",
		"FarmLand/LastWeek2.csv",
		"FarmLand/LastWeek3.csv",
		"FarmLand/LastWeek4.csv",
		"FarmLand/LastWeek5.csv",
		"FarmLand/Latest_1.csv",
		"FarmLand/Latest_2.csv",
		"FarmLand/Latest_3.csv",
		"FarmLand/Latest_4.csv",
		
		"FarmLand/Last_data_2022.csv"
	};
	
	//vector<int> foamShrink = { 10,20,30,50,100,200,300,500,800,1000,1500,2000 };
	vector<int> foamShrink = {1500};
	//vector<int> abatereHard = { 200,500,1000,2000,3000,4000,5000/*,6000,7000,8000,9000,10000*/ };
	vector<int> abatereHard = {1000};

	vector<point> testData;
	/*{
		std::unique_lock<std::mutex> lock(mutex_file_terraForm);
		testData = pythonHandler("FarmLand/LastWeek1.csv", "FarmLand/portal_gun.txt", candles_size, filter_1, filter_2);
	}*/

	for (auto &farm_location_el : farm_locations)
	{
		{
			std::unique_lock<std::mutex> lock(mutex_file_terraForm);
			testData = pythonHandler(farm_location_el, "FarmLand/portal_gun.txt", candles_size, filter_1, filter_2);
		}

		/*cout << endl << "TEST 1:, raw data from csv:"<<farm_location_el << endl;
		for (auto& a : testData)
		{
			cout << endl << a.x << "," << a.y;
		}*/

		//1,3,5,10,20,[30],50,100 //realSize = 33
		int currentSize = patternsParam.size();
		std::cout << endl << "current size:" << currentSize;
		for (auto& a : foamShrink)
		{
			cout << "before break" << endl;
			if (a > currentSize) //maybe currentSize - 1 
				break;

			cout << "after break" << endl;
			vector<patterns> shrinked_patterns;

			for (int i = 0; i < a; i++)
			{ 
				shrinked_patterns.push_back(patternsParam[i]);
			}
			std::cout << endl << "check point";
			for (auto& c : abatereHard)
			{
				cout << endl << "HERE BITCH" << endl;
				writePatternsIntoFile(shrinked_patterns);
				supremeTest(c, a, testData, shrinked_patterns, succes_ratio_filter, candles_size, size_seg_unic, filter_1, filter_2, future_price, min_max_streching, abatere, mutex_file_Apollo, mutex_console, farm_location_el);
			}
		}
	}
}

vector<point> pythonHandler(string source, string destination,int candleSize, floatType filter_candles_1, floatType filter_candles_2)
{
	vector<point> inputData;
	
	std::string command = "python main.py " +
		std::to_string(candleSize) + " " +
		std::to_string(filter_candles_1) + " " +
		std::to_string(filter_candles_2) + " " +
		source + " " +
		destination;

	//std::cout << endl << "check comanda:" << command << endl;
	int py_return_code = system(command.c_str());
	//std::cout << "py return code:" << py_return_code << endl;

	inputData = readFromFile(1, destination);

	return inputData;
}
void supremeTest(int abatere_hard, int how_many_for_foam, vector<point> testData, vector<patterns> patterns, floatType succes_ratio_filter, int candles_size, int size_seg_unic, floatType filter_1, floatType filter_2, int future_price, int min_max_streching, int abatere, std::mutex& mutex_file_Apollo, std::mutex& mutex_console, string test_farm)
{
	//test
	//cout << endl << "entry point supremeTest:" << endl;


	int total_buyed = 0;
	int succes_buyes = 0;

	vector<point> inputData = testData; //wtf man

	//printInputData(inputData); //TEST RAW DATA

	vector<vector<point>> segmente_baza;
	segmentareArray(segmente_baza, inputData, size_seg_unic);
	//test
	//cout << endl << "segmente array:" << endl;
	//int index_time_stamp = 0;
	/*for(auto & a:segmente_baza)
	{
		cout << endl << "time stamp:" << index_time_stamp << endl;
		index_time_stamp++;
		for (auto& b : a)
		{
			cout << b.x << "," << b.y << "/";
		}
		cout << endl;
	}*/

	/*cout << endl << "patterns:" << endl;
	for (auto& a : patterns)
	{
		for (auto& b : a.seg_baza)
		{
			cout << b.x << "," << b.y << "/";
		}
		cout << endl;
	}*/

	//std::cout << endl << "S-au generat:" << segmente_baza.size() << " segment de baza pentru simulare";
	
	int index_global_input_data = -1;
	int last_index_added = 0;
	int offset_to_ignore = 20; //20 min
	for (auto& a : segmente_baza)
	{
		//cout << "index_global" << index_global_input_data << endl;
		index_global_input_data++;

		//afla cel mai mic cross corelation dintre toate patterns posibile
		floatType min_cross_cor = crosssCorelation(a, patterns[0].seg_baza, true, true);
		//cout << "min cross:" << min_cross_cor << endl;
		int index_min_cross_cor = 0;
		int index_iterator = -1;

		for (auto& b : patterns)
		{
			index_iterator++;
			if (crosssCorelation(a, b.seg_baza, true, true) < min_cross_cor)
			{
				min_cross_cor = crosssCorelation(a, b.seg_baza, true, true);
				index_min_cross_cor = index_iterator;
			}
		}
		//daca cel mai mic cross corelation < abatere_hard

		if (min_cross_cor <= abatere_hard )
		{
			if (last_index_added == 0 || index_global_input_data - last_index_added > offset_to_ignore)
			{
				last_index_added = index_global_input_data;
				//cout << endl << "Add new :" << index_global_input_data;
				//test with python
				//cout << endl<< "new patt at:" << index_global_input_data << endl;

				//simuleaza o cumparare
				total_buyed++;

				//check (index + size_seg_unic + future_price) > seg_now[last_index]
				floatType last_price_live = inputData[index_global_input_data + size_seg_unic].y; //possible index out of range

				//TODO = check out of range case
				floatType future_price_live = inputData[index_global_input_data + size_seg_unic + future_price].y; //possible index out of range

				//true ? increment succes_buyes
				if (last_price_live < future_price_live)
				{
					succes_buyes++;
				}
			}
		}
	}
	
	if (total_buyed == 0)
		return;
	floatType succes_percent = (succes_buyes * 100) / total_buyed;

	std::stringstream stream;

	stream << succes_percent << "/" << succes_buyes << "/" << total_buyed << "/" << abatere_hard << "/";
	stream << how_many_for_foam << "/"<<succes_ratio_filter << "/"<< candles_size << "/" << size_seg_unic << "/" << filter_1 << "/";
	stream << filter_2 << "/" << future_price << "/" << min_max_streching << "/" << abatere << "/";
	stream << test_farm << "/";

	writeResultIntoFile(mutex_file_Apollo, stream.str(), "apollo.txt");
	if (succes_percent > 50)
	{
		writeResultIntoFile(mutex_file_Apollo, stream.str(), "apolloGold.txt");
	}
}

vector<vector<floatType>> giveMeCombinations(const string file_name) {

	vector<vector<floatType>> result;

	std::ifstream infile(file_name);
	string row;
	while (infile >> row)
	{
		//std::cout << row << std::endl;
		vector<floatType> temp_arr;

		//cout << "Row: " << row << endl;

		std::string delimiter = "/";

		size_t pos = 0;
		std::string token;
		while ((pos = row.find(delimiter)) != std::string::npos) {
			token = row.substr(0, pos);
			
			//std::cout << token << std::endl;

			temp_arr.push_back(::atof(token.c_str()));
			row.erase(0, pos + delimiter.length());
		}
		/*for (auto a : temp_arr)
		{
			std::cout << a << " ";
		}
		std::cout << endl;*/
		result.push_back(temp_arr);
	}

	//print test
	/*for (auto& a : result)
	{
		for (auto& b : a)
		{
			cout << b << " ";
		}
		cout << endl;
	}*/

	return result;
}

void writeResultIntoFile(std::mutex& mutex, string a,string destination)
{
	std::unique_lock<std::mutex> lock(mutex);

	auto file = std::ofstream(destination, std::ofstream::app);

	file << a << std::endl;

	file.close();
}


void writePatternsIntoFile(vector<patterns> patternsParam)
{
	cout << endl << "MA-ta mare:" << patternsParam.size() << endl;
	std::stringstream file_stream;
	for (auto& a : patternsParam)
	{
		std::stringstream new_row_stream;
		for (auto& b : a.seg_baza)
		{
			new_row_stream << b.x << "," << b.y << "/";
		}
		file_stream << new_row_stream.str() + "\n";
	}
	file_stream << "\n\n";
	auto file = std::ofstream("outputPatterns.txt", std::ofstream::app);

	file << file_stream.str() << std::endl;

	file.close();
}