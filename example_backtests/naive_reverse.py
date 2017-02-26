from cointk.backtest import backtest
from cointk.strategies import NaiveReverseStrategy

strategy = NaiveReverseStrategy(n_prices=1000, threshold=0.8)

backtest(strategy)
