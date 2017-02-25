from cointk.backtest import backtest
from cointk.strategies import NaiveStrategy

strategy = NaiveStrategy(n_prices=30, threshold=0.8)
backtest(strategy)
