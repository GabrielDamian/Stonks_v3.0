#include "Header.h"
#include "ThreadPool.h"

int main()
{
	//future price - hardcoded
	//double candleSize = 3;
	//double filter_candles_1 = 0.5;
	//double filter_candles_2 = 0.5;

	//int size_seg_unic = 35;
	//int min_max_streching = 1;

	//int abatere = 5000; //1k-10k
	//int abatere_hard = 4000;//1k-10k, but with intern for loop


	floatType filter_succes_ratio = 60;
	vector<vector<floatType>> main_combinations = giveMeCombinations("main_combination.txt");

	/* 
	#FORMAT MAIN :
	#  a[0] candles_size /
	#  a[1] size_seg_unic /
	#  a[2] filter_1 /
	#  a[3] filter_2 /
	#  a[4] future_price /
	#  a[5] min_max_streching /
	#  a[6] abatere*/

	ThreadPool threadPool(8);

	std::mutex mutex_file_main;
	std::mutex mutex_file_terraForm;
	std::mutex mutex_file_Apollo;
	std::mutex mutex_console;

	for (auto& a : main_combinations)
	{
		//cout << std::endl <<"da:"<< a[0] << " " << a[1] << " " << a[2] << " " << a[3] << " " << a[4] << " " << a[5];
		threadPool.submitJob(
				[&]()
				{
				//cout << std::endl << a[0] << " " << a[1] << " " << a[3] << " " << a[4] << " " << a[5] << " " << a[6];
				narutoMain(a[0], a[2], a[3], a[1], a[5], a[6], filter_succes_ratio,std::ref(mutex_file_main), std::ref(mutex_file_terraForm), std::ref(mutex_file_Apollo), std::ref(mutex_console));
				}
			);
	}
	//for (int i = 0; i < 30; i++)
	//{
	//	//narutoMain(candleSize, filter_candles_1, filter_candles_2, size_seg_unic, min_max_streching, abatere, succes_ratio, std::ref(mutex));
	//	std::cout << std::endl << "Started a new job !";
	//	threadPool.submitJob(
	//		[&]()
	//		{
	//			narutoMain(candleSize, filter_candles_1, filter_candles_2, size_seg_unic, min_max_streching, abatere, succes_ratio, std::ref(mutex));
	//		}
	//	);
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

