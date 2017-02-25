from cointk.backtest import backtest
from cointk.strategies import NaiveStrategy, NaiveStrategyReverse, RandomStrategy

# testing w/ 10000 data
strategy = NaiveStrategy(n_prices=1000, threshold=0.8)
strategyReverse = NaiveStrategyReverse(n_prices=1000, threshold=0.8)
strategyRandom = RandomStrategy()

#backtest(strategy, data_fnm='data/coinbaseUSD_100k_sample.npz', train_prop=0.01, val_prop=0.9, plot_name='plots/Naive-100k-test.html')
#backtest(strategyReverse, data_fnm='data/coinbaseUSD_100k_sample.npz', train_prop=0.01, val_prop=0.9, plot_name='plots/NaiveReverse-100k-test.html')
backtest(strategyRandom, data_fnm='data/coinbaseUSD_100k_sample.npz', train_prop=0.01, val_prop=0.9, plot_name='plots/NaiveRandom-100k-test.html')
