from cointk.backtest import backtest
from cointk.strategies import NaiveStrategy, NaiveStrategyReverse

# testing w/ 10000 data
strategy = NaiveStrategy(n_prices=1000, threshold=0.7)
strategyReverse = NaiveStrategyReverse(n_prices=1000, threshold=0.7)
backtest(strategy, data_fnm='data/coinbaseUSD_sample.npz', train_prop=0.01, val_prop=0.9, plot_name='Naive-test.html')


backtest(strategyReverse, data_fnm='data/coinbaseUSD_sample.npz', train_prop=0.01, val_prop=0.9, plot_name='NaiveReverse-test.html')
