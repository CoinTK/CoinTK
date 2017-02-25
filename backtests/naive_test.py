from cointk.backtest import backtest
from cointk.strategies import OldNaiveStrategy

strategy = OldNaiveStrategy(n_prices=100, threshold=0.8)
# Use the 100k test dataset
backtest(strategy, data_fnm='data/coinbaseUSD_100k_sample.npz', plot_name='Naive-test-100k-threshhold-0.8.html', verbose=1)
