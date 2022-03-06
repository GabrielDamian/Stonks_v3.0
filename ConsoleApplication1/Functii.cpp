#include"Header.h"
#include<iomanip>
#include<cmath>


void narutoMain(double candleSize, double filter_candles_1, double filter_candles_2, int size_seg_unic, int abatere)
{
	//config area

	//PY MODULE:
	//double candleSize = 3;
	//double filter_candles_1 = 0.1;
	//double filter_candles_2 = 0.5;
	//int size_seg_unic = 40;
	//int abatere = 1500;


	std::string command = "python main.py " + std::to_string(candleSize) + " " + std::to_string(filter_candles_1) + " " + std::to_string(filter_candles_2);
	cout << endl << "comanda:" << command << endl;
	int py_return_code = system(command.c_str());
	cout << "py return code:" << py_return_code << endl;


	int min_max_streching = 1;


	int future_price = 10;
	bool yScalerEnabler = true;
	bool powerSumCrossCor = true;

	vector<point> inputData = readFromFile(1);
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
	for (auto& a : variatii)
	{
		segmentareVariatii_with_future_price(a.second, inputData, a.first, future_price);
	}
	cout << endl << "------------Variatii default:" << endl;
	//printVariatii(variatii);


	//comprimare X
	for (auto& a : variatii)
	{
		for (auto& b : a.second)
		{
			comprimaSegment_X(b.values, size_seg_unic);
		}
	}

	cout << endl << "------------Variatii comprimate : " << endl;
	//printVariatii(variatii);

	for (auto& a : variatii)
	{
		for (auto& b : a.second)
		{
			interpoleazaSegment(b.values, size_seg_unic);
		}
	}
	cout << endl << "------------Variatii comprimate si interpolate:" << endl;
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
						if (variatie.future_price != NULL && variatie.future_price > variatie.last_price) positives++;
					}
				}
			}
		}
		pattern_ref.scor = scor_cadinal;
		pattern_ref.positives = positives;
		pattern_ref.index = index_cout;
	}

	std::sort(posibile_patterns.begin(), posibile_patterns.end(), [](patterns const& a, patterns const& b)->bool //descending
		{
			return a.scor > b.scor;
		});

	cout << endl << endl << "==== Pattern finale desc ========";
	//printPatterns(posibile_patterns);

	//supreme test naruto run
	supremeTest(posibile_patterns,  size_seg_unic,  future_price);

	//cin.ignore();
}
vector<point> readFromFile(int howMany)
{
	//howMany == 1 (read all)
	vector<point> fileData;

	floatType a;
	floatType b;
	std::ifstream infile("data.txt");

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
				temp_struct.future_price = NULL;
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
	cout << setprecision(2);
	cout << fixed;

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
		cout << a.y << ", ";
	}
}
void printSegmenteBaza(vector<vector<point>>& segmente_baza)
{
	std::cout << std::fixed;
	std::cout << std::setprecision(1);
	cout <<endl<< "Testare segmente de baza:" << endl;
	int how_many = 10;
	int now = 0;
	for (auto a : segmente_baza)
	{
		if (now > how_many) break;
		now++;
		for (auto b : a)
		{
			//cout << "[" << b.x << "," << b.y << "], ";
			cout << b.y << ",";
		}
		cout << endl;
	}
}
void printVariatii(map<int, vector<twin>>& variatii)
{
	cout << setprecision(2);
	cout << fixed;

	for (auto& a : variatii)
	{
		cout << endl << endl << "-->key:" << a.first << " size arr variatii:" << a.second.size();
		
		int how_many = 5;
		int now = 0;
		
		for (auto& b : a.second)
		{
			if (now > how_many) break;
			now++;
			cout << endl << "Len=" << b.values.size() << " ";
			for (auto& c : b.values)
			{
				//cout << "[" << c.x << "," << c.y << "], ";
				cout << c.y << ", ";
			}
			cout << endl <<endl<<"Future price:" << b.future_price;
			cout << endl << "Last price:" << b.last_price;
			cout << endl << "index:" << b.index << endl;
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

		cout << endl << endl << "----Patten: " << endl;
		printInputData(a.seg_baza);
		
		cout << endl << "score:" << a.scor;
		cout << endl << "positives:" << a.positives;
		cout << endl << "index:" << a.index << endl;

		cout << endl << "Variatii filtrate:";
		printVariatii(a.variatii_filtrate);

		

	}

}

//SUPREME TEST
void supremeTest(vector<patterns> patterns, int size_seg_unic, int future_price)
{
	int how_many = 1; //10k = 1 week
	int abatere_hard = 3000;	//?? formula based on size_seg_unic
	floatType succes_ratio = 0.9; //x%

	int total_buyed = 0;
	int succes_buyes = 0;

	//segmenteaza input_data in segmente consecutive de len = len_pattern
	vector<point> inputData = readFromFile(how_many); //10k = 1 week
	//printInputData(inputData); //TEST RAW DATA

	vector<vector<point>> segmente_baza;
	segmentareArray(segmente_baza, inputData, size_seg_unic);
	cout << endl << "S-au generat:" << segmente_baza.size() << " segment de baza pentru simulare";

	//----TODO---- = shrink pattern to keep only the first 10% of the data
	int how_many_represents_first_10_percentage = int(0.2 * patterns.size());
	
	cout << "how manu 10 %" << how_many_represents_first_10_percentage << endl;
	patterns.resize(how_many_represents_first_10_percentage);
	patterns.shrink_to_fit();

	cout << endl << "final size:" << patterns.size() << endl;
	//itereaza segmentele obtinute
	int index_global_input_data = -1;

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
		//daca cel mai mic cross corelation < maxim_abatere & succes_ratio ok:(maxim_abatere extrem de mic in cazul acesta)

		floatType procent_scor = 0.0;
		if (patterns[index_min_cross_cor].positives == 0)
		{
			//evita impartirea la 0
			procent_scor = 0.0;
		}
		else
		{
			procent_scor = floatType(patterns[index_min_cross_cor].positives) / floatType(patterns[index_min_cross_cor].scor);
		}
		//cout << "procent scor" << procent_scor << endl;
		if (min_cross_cor <= abatere_hard && procent_scor > succes_ratio)
		{
			//simuleaza o cumparare
			total_buyed++;

			//check (index + size_seg_unic + future_price) > seg_now[last_index]
			floatType last_price_live = inputData[index_global_input_data+size_seg_unic].y;
			
			//TODO = check out of range case
			floatType future_price_live = inputData[index_global_input_data + size_seg_unic + future_price].y;
			
			//true ? increment succes_buyes
			if (last_price_live < future_price_live)
			{
				succes_buyes++;
			}
			
		}


	}

	cout << endl << "Final:" << endl;
	cout << "Succes:" << succes_buyes << endl;
	cout << "Total:" << total_buyed << endl;
	cout << "%" << (succes_buyes * 100) / total_buyed;
	//cout succes_buyes / total_buyes

}
