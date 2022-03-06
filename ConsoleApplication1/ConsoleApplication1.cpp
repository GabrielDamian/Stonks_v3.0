#include"Header.h"

int main()
{
	double candleSize = 1;
	double filter_candles_1 = 0.3;
	double filter_candles_2 = 0.5;

	int size_seg_unic = 65;
	int abatere = 5000;

	narutoMain(candleSize, filter_candles_1, filter_candles_2, size_seg_unic, abatere);
	
	return 0;
}

