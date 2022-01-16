#include"Header.h"


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

	double ratio = comprimed_size / result.size();
	transform(result.begin(), result.end(), result.begin(), [ratio](point el) {
		point new_el;
		new_el.x = el.x * ratio;
		new_el.y = el.y;
		return new_el;
		});

}
void interpoleazaSegment(vector<point>& result, int comprimed_size)
{
	
}


