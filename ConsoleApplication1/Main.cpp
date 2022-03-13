#include "Header.h"
#include "ThreadPool.h"

int main()
{
	//future price - hardcoded
	double candleSize = 3;
	double filter_candles_1 = 0.5;
	double filter_candles_2 = 0.5;

	int size_seg_unic = 35;
	int min_max_streching = 1;

	int abatere = 5000; //1k-10k
	int abatere_hard = 4000;//1k-10k, but with intern for loop

	floatType succes_ratio = 80;
	vector<vector<floatType>> main_combination = giveMeCombinations("main_combination.txt");

	ThreadPool threadPool;

	std::mutex mutex;

	//for (auto& a : main_combination)
	//{
	//	threadPool.submitJob(
	//		[&]()
	//		{
	//			//narutoMain(a[0], a[2], a[3], a[1], a[6], a[5],5000,0.8,std::ref(mutex));
	//		}
	//	);
	//}

	/*narutoMain(candleSize, filter_candles_1, filter_candles_2, size_seg_unic, min_max_streching, abatere, succes_ratio, std::ref(mutex));
	narutoMain(candleSize, filter_candles_1, filter_candles_2, size_seg_unic, min_max_streching, abatere, succes_ratio, std::ref(mutex));*/

	for (int i = 0; i < 30; i++)
	{
		//narutoMain(candleSize, filter_candles_1, filter_candles_2, size_seg_unic, min_max_streching, abatere, succes_ratio, std::ref(mutex));
		std::cout << "A" << std::endl;
		threadPool.submitJob(
			[&]()
			{
				narutoMain(candleSize, filter_candles_1, filter_candles_2, size_seg_unic, min_max_streching, abatere, succes_ratio, std::ref(mutex));
			}
		);
	}

	//for (int i = 8; i; i--)
	//{
	//	threadPool.submitJob(std::bind(demoNaruto, std::ref(mutex), i, i));
	//}

	while (threadPool.isWorking())
	{
		std::this_thread::sleep_for(std::chrono::milliseconds(50));
	}

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

