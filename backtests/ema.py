from cointk.backtest import backtest
from cointk.strategies import EMAPriceCrossover

strategy = EMAPriceCrossover(ma_length=10000, qty=-1, decision='increasing', verbose=1)

backtest(strategy, data_fnm='data/coinbaseUSD.npz',
        plot_name='plots/EMA-full.html', plot_ema=True)


#backtest(strategy, data_fnm='data/coinbaseUSD_30k_sample.npz',
#         plot_name='plots/EMA-30k.html', train_prop=0.01, val_prop=0.9)
