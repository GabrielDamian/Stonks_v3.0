#include "Header.h"
#include "ThreadPool.h"

int main() //main checked
{
	vector<vector<floatType>> main_combinations = giveMeCombinations("main_combination.txt"); //checked

	/* 
	#FORMAT MAIN :
	#  a[0] candles_size /
	#  a[1] size_seg_unic /
	#  a[2] filter_1 /
	#  a[3] filter_2 /
	#  a[4] future_price /
	#  a[5] min_max_streching /
	#  a[6] abatere*/

	ThreadPool threadPool(4);

	std::mutex mutex_file_main;
	std::mutex mutex_file_terraForm;
	std::mutex mutex_file_Apollo;
	std::mutex mutex_console;

	for (auto& a : main_combinations)
	{
		threadPool.submitJob(
				[&]()
				{
				cout << endl << "abatere main:" << a[6] << endl;
				narutoMain(a[0], a[1], a[2], a[3], a[4], a[5], a[6], std::ref(mutex_file_main), std::ref(mutex_file_terraForm), std::ref(mutex_file_Apollo), std::ref(mutex_console));
				}
			);
	}

	while (threadPool.isWorking())
	{
		std::this_thread::sleep_for(std::chrono::milliseconds(50));
	}
	cout << endl << "DONE" << endl;
	return 0;

}

