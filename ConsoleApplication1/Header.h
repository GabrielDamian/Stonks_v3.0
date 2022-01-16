#pragma once
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>

#define abatere  10

using namespace std;

struct point {
	double x;
	double y;

	bool operator==(const point& right) const {
		return x == right.x && y == right.y;
	};
};

struct twin {
	vector<point> values;
	double future_price;
};

struct patterns { //cate un 'patterns' pentru fiecare segment din 'segmente_baza
	vector<point> seg_baza;
	map<int, vector<twin>> variatii_filtrate; //doar variatiile filtrare
	//rezultate finale = suma cardinalului variatiilor
};


vector<point> readFromFile( );
void segmentareArray(vector<vector<point>>& result,vector<point>& inputData, int size_seg_unic);
void normalizeazaSegment(vector<point>& segment);
void seteazaKeyVariatii(map<int, vector<twin>>& variatii, int size_seg_baza, int min_max_streching);
void segmentareVariatii_with_future_price(vector<twin>& result, vector<point>& inputData, int size_variatie, int future_price);

void printVariatii(map<int, vector<twin>>& variatii);
void comprimaSegment(vector<point>& result, int comprimed_size);
void interpoleazaSegment(vector<point>& seg_factorizat, int comprimed_size);
double yEcuatieDreapta(point a, point b, double x);

double crosssCorelation(const vector<point>& seg_1, const vector<point>& seg_2);



