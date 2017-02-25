from cointk.backtest import backtest
from cointk.strategies import NaiveStrategy

strategy = NaiveStrategy(n_prices=1000, threshold=0.5)
backtest(strategy, plot_name='Naive-full-threshhold-0.95.html', verbose=1)
