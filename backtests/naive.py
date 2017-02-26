from cointk.backtest import backtest
from cointk.strategies import NaiveStrategy

strategy = NaiveStrategy(n_prices=1000, threshold=0.8)

backtest(strategy, data_fnm='data/coinbaseUSD_100k_sample.npz', plot_name='plots/Naive-full-threshhold-0.8.html', verbose=1, train_prop=0.01, val_prop=0.9)

# test with full data
#backtest(strategy, plot_name='plots/Naive-full-threshhold-0.8.html', verbose=1)
