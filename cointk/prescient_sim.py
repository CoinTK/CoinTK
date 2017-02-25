from .backtest import resolve_data
from .data import save_data
import numpy as np


def compute_prescient(strategy, fee=0.0025, data=None,
                      data_fnm='data/coinbaseUSD.npz', data_name='data',
                      datapart='train',
                      history_fnm='prescient_histories/naive.npz',
                      history_name='data'):
    data = resolve_data(data, data_fnm, data_name, datapart)
    order_history = []
    strategy.init_pretest(fee)
    strategy.read_data(tss=data[:, 0], prices=data[:, 1], qtys=data[:, 2])
    for i, (ts, price, qty) in enumerate(data):
        order = strategy.prevaluate(i, ts, price, qty)
        order_history.append(order)
    strategy.read_order_history(order_history)
    order_arr = np.asarray([order.to_tuple() for order in order_history])
    save_data(order_arr, history_fnm, history_name)
    return order_history
