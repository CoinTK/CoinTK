from cointk.backtest import backtest
from cointk.strategies import NaiveStrategy
import random

random.seed(1)
strategy = NaiveStrategy(n_prices=1000, threshold=0.8)

backtest(strategy)
