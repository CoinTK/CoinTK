## CoinTK -- Smart Bitcoin Analyzing & Trading Toolkit




```cointk/``` contains most of the algorithmic work
* ```strategies/``` contain different buying/selling strategies, which is just a decision framework based on the given state of price/quantity and past histories



```backtests/``` tests strategies running on historical data, so you can evaluate performance had you ran this strategy since the beginning



Test dataset (10k) in data/
* [full dataset 2015/09-2016/12](http://api.bitcoincharts.com/v1/csv/coinbaseUSD.csv.gz)
* use ```csv_to_npz() in cointk/data.py``` to convert csv to npz; 
  * e.g. ```csv_to_npz('data/coinbaseUSD.csv', 'data/coinbaseUSD.npz')```