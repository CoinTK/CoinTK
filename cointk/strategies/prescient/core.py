import numpy as np
from ..core import Strategy
from ...order import Order, OrderSpec


class PrescientStrategy(Strategy):
    def __init__(self, order_history=None):
        super().__init__()
        self.tss = []
        self.prices = []
        self.qtys = []
        self.order_history = order_history
        self.idx = 0

    def init_pretest(self, fee):
        self.fee = fee

    def init_backtest(self, funds, balance, worth):
        super().init_backtest(funds, balance, worth)
        self.idx = 0

    def read_order_history(self, order_history):
        self.order_history = order_history

    def load_order_history(self, history_fnm, history_name='data'):
        order_arr = np.load(history_fnm)[history_name]
        self.order_history = [OrderSpec(src_tuple=row) for row in order_arr]

    def read_data(self, tss, prices, qtys):
        self.tss = tss
        self.prices = prices
        self.qtys = qtys

    def gen_order(self, ts, price, qty, funds, balance):
        order = Order(spec=self.order_history[self.idx])
        self.idx += 1
        return order
