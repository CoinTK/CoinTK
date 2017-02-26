from cointk.backtest import backtest
from cointk.strategies import EMAPriceCrossover

strategy = EMAPriceCrossover(ma_length=10000, qty=-1, decision='increasing',
                             verbose=1)
backtest(strategy, plot_fnm='plots/EMA-full.html',
         plot_ema=True)
