from cointk.backtest import backtest
from cointk.strategies import NaiveStrategy

strategy = NaiveStrategy(n_prices=1000, threshold=0.8)
backtest(strategy, plot_name='plots/Naive-full-threshhold-0.8.html', verbose=1)
