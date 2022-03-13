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

	int myWriterObject;

	std::mutex mutex;
	std::unique_lock<std::mutex> lock(mutex, std::defer_lock);

	threadPool.submitJob(
		[&lock]() {
			int count = 100;

			
		}
	);

	threadPool.submitJob(
		[&lock]() {
			int count = 100;

			while (count--)
			{
				std::cout << "[Bitch" << "bitch" << "bitch" << "bitch]";
			}
		}
	);

	while (threadPool.hasJobs())
	{
		std::this_thread::sleep_for(std::chrono::milliseconds(50));
	}

	return 0;

	for (auto& a : main_combination)
	{
		cout << endl<<"apleare main cu:";
		for (auto& b : a)
		{
			cout << b << " ";
		}
		//narutoMain(candleSize, filter_candles_1, filter_candles_2, size_seg_unic, abatere, min_max_streching, abatere_hard, succes_ratio);

	}


	
	return 0;
}

