#include"Header.h"
#include<iomanip>
vector<point> readFromFile()
{
	vector<point> fileData;

	int a;
	double b;
	std::ifstream infile("data.txt");
	while (infile >> a >> b)
	{
		point temp_point;
		temp_point.x = a;
		temp_point.y = b;
		fileData.push_back(temp_point);
	}

	return fileData;
}

void segmentareArray(vector<vector<point>>& result, vector<point> inputData, int size_seg_unic)
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
			normalizeazaSegment(buffer);
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
	int min_x = segment[0].x;
	double min_y = segment[0].y;

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

	int index = 0;
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
			
			//normalizeazaSegment(buffer);
			twin temp_struct;
			normalizeazaSegment(buffer);
			temp_struct.values = buffer;



			//conditie de extragere future_price
			if (index + future_price < inputData.size() - 1)
			{
				temp_struct.future_price = inputData[index].y;
			}
			else
			{
				temp_struct.future_price = NULL;
			}

			result.push_back(temp_struct);
		}
		else
		{
			//nu mai pot incadra inca un segment
		}

	}
}
void printVariatii(map<int, vector<twin>> variatii)
{
	cout << setprecision(2);
	cout << fixed;
	cout << endl << "Test populare variatii:" << endl;
	for (auto& a : variatii)
	{
		cout << endl << "-->key:" << a.first << " size arr variatii:" << a.second.size() << endl;
		for (auto& b : a.second)
		{
			//b = struct twin
			//cout << endl << "Future price:" << b.future_price << " Values:";
			//cout <<a.first<< "== ?"<<b.values.size()<<endl;
			cout << endl << "Len=" << b.values.size() << " ";
			for (auto& c : b.values)
			{
				//cout << "(" << c.x<<","<<c.y<<") ";
				cout << "(" << c.x << "," << c.y << ") ";
			}
			cout << " Future price:" << b.future_price;
		}
	}
}
void comprimaSegment(vector<point>& result, int comprimed_size)
{
	//comprimed_size = 10
	// 
	//from size = 5
	//from size = 15

	double ratio = comprimed_size / (double)(result.size() - 1);
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

	vector<double> x_segment_referinta; //range(0,comprimed_size)
	vector<double> x_segment_factorizat; //doar x's

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
		double x_curent = a;
	
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

double yEcuatieDreapta(point point_a, point point_b, double x_value)
{
	double x0 = point_a.x;
	double y0 = point_a.y;
	double x1 = point_b.x;
	double y1 = point_b.y;

	double x = x_value;

	double y = (y0 * (x1 - x) + y1 * (x - x0)) / (x1 - x0);

	return y;
}
