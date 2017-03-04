from cointk.backtest import backtest
from cointk.strategies import EMAPriceCrossover
import random

random.seed(1)
strategy = EMAPriceCrossover(ma_length=10000, qty=-1, trend_threshold=2, decision_logic='order_once',
                             verbose=1)
backtest(strategy, plot_fnm='plots/EMA-full.html', datapart='train', plot_args={'initial_funds': 1000})
