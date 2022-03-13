#include "Header.h"
#include "ThreadPool.h"

int main()
{
	//future price - hardcoded
	double candleSize = 3;
	double filter_candles_1 = 0.5;
	double filter_candles_2 = 0.5;

	int size_seg_unic = 65;
	int min_max_streching = 1;

	int abatere = 5000; //1k-10k
	int abatere_hard = 4000;//1k-10k, but with intern for loop

	floatType succes_ratio = 80;
	vector<vector<floatType>> main_combination = giveMeCombinations("main_combination.txt");

	ThreadPool threadPool;

	std::mutex mutex;

	for (auto& a : main_combination)

	for (int i = 8; i; i--)
	{
		threadPool.submitJob(std::bind(demoNaruto, std::ref(mutex), i, i));
	}

	while (threadPool.isWorking())
	{
		std::cout << "Waiting!";
		std::this_thread::sleep_for(std::chrono::milliseconds(50));
	}

	std::cout << "Out!";
	narutoMain(candleSize, filter_candles_1, filter_candles_2, size_seg_unic, abatere, min_max_streching, abatere_hard, succes_ratio);

	/*for (auto& a : main_combination)
	{
		cout << endl<<"apleare main cu:";
		for (auto& b : a)
		{
			cout << b << " ";
		}

	}*/

	return 0;
}

