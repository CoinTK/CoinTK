from cointk.backtest import backtest
from cointk.strategies import NaiveStrategy

strategy = NaiveStrategy(n_prices=1000, threshold=0.99)
backtest(strategy, plot_name='Naive-full-threshhold-0.99', verbose=2)


strategyReverse = NaiveStrategyReverse(n_prices=1000, threshold=0.99)
backtest(strategy, plot_name='NaiveReverse-full-threshhold-0.99', verbose=2)
