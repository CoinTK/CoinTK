from cointk.backtest import backtest
from cointk.strategies import RandomStrategy

strategy_random = RandomStrategy()

backtest(strategy_random, data_fnm='data/coinbaseUSD.npz',
         plot_name='plots/NaiveRandom-full.html')
