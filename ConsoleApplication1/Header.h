#pragma once
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <mutex>
typedef float floatType;

using namespace std;

struct point {
	floatType x;
	floatType y;

	bool operator==(const point& right) const {
		return x == right.x && y == right.y;
	};
};

struct twin {
	vector<point> values;
	floatType future_price;
	floatType last_price;
	int index;
};

struct patterns { 
	vector<point> seg_baza;
	map<int, vector<twin>> variatii_filtrate; 
	int scor;
	int positives;
	int index;
};

//Naruto main
void narutoMain(double candleSize, double filter_candles_1, double filter_candles_2, int size_seg_unic, int min_max_streching, int abatere, floatType filter_succes_ratio, std::mutex& mutex_file_main,std::mutex& mutex_file_terraForm, std::mutex & mutex_file_Apollo, std::mutex& mutex_console);

vector<point> readFromFile(int howMany, string source);
void segmentareArray(vector<vector<point>>& result,vector<point>& inputData, int size_seg_unic);
void normalizeazaSegment(vector<point>& segment);
void seteazaKeyVariatii(map<int, vector<twin>>& variatii, int size_seg_baza, int min_max_streching);
void segmentareVariatii_with_future_price(vector<twin>& result, vector<point>& inputData, int size_variatie, int future_price);

void comprimaSegment_X(vector<point>& result, int comprimed_size);

void interpoleazaSegment(vector<point>& seg_factorizat, int comprimed_size);
floatType yEcuatieDreapta(point a, point b, floatType x);

floatType crosssCorelation(const vector<point>& base, const vector<point>& seg_2, bool yScalerEnabler, bool powerSum);
bool checkIfStraightLine(vector<point> baseSegment);
bool checkSimilarIndex(vector<twin>& vector_twin, twin variatie, int how_far);

//Test functions
void printInputData(vector<point>& inputData);
void printSegmenteBaza(vector<vector<point>>& segmente_baza);
void printVariatii(map<int, vector<twin>>& variatii);
void printPatterns(vector<patterns> posibile_patterns);

//SUPREME TEST

void supremeTestMaster(vector<patterns> patterns, double candleSize, double filter_candles_1, double filter_candles_2,int future_price, int size_seg_unic, int min_max_streching, int abatere, floatType filter_succes_ratio, std::mutex& mutex_file_terraForm, std::mutex& mutex_file_Apollo);

void supremeTest(vector<point> terraFormedInputData,vector<patterns> patterns, int size_seg_unic, int future_price, int abatere_hard, floatType succes_ratio, int procent_how_many, std::mutex& mutex_Apollo);
//Combination translator
vector<vector<floatType>> giveMeCombinations(const string file_name);
vector<point> pythonHandler(string source, string destination, int candleSize, int filter_candles_1, int filter_candles_2);

//Results writer
void writeResultIntoFile(std::mutex& mutex, int a);

