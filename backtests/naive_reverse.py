from cointk.backtest import backtest
from cointk.strategies import NaiveStrategyReverse

strategy = NaiveStrategyReverse(n_prices=1000, threshold=0.8)

backtest(strategy, data_fnm='data/coinbaseUSD.npz',
         plot_name='plots/NaiveReverse-full-threshhold-0.8.html')
