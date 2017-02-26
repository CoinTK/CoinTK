from .core import Strategy
from ..order import Order
from collections import deque


class NaiveStrategy(Strategy):
    '''
        Very basic strategy: buy if we're on a rising price trend,
        sell if we've been losing money

        This is just to provide a 'baseline' to test the performance of our
        smarter algorithms

        This is significantly faster than naive.py, since it doesn't
        recalculate uptrend/downtrends from scratch every time. Instead, as we
        encounter new data points, we simply increment/decrement the
        uptrend/downtrend counters by 1
    '''
    def __init__(self, n_prices=1000, qty=0.01, threshold=0.8, price_inc=0.1):
        super().__init__()
        self.n_prices = n_prices
        self.old_prices = deque()
        self.qty = qty
        self.threshold = threshold
        self.price_inc = price_inc
        self.uptrend_count = 0
        self.downtrend_count = 0

    def gen_order(self, ts, price, qty, funds, balance):
        order = None
        if len(self.old_prices) > 1:
            if price >= self.old_prices[-1]:
                self.uptrend_count += 1
            if price <= self.old_prices[-1]:
                self.downtrend_count += 1
            if len(self.old_prices) > self.n_prices + 1:
                if self.old_prices[1] >= self.old_prices[0]:
                    self.uptrend_count -= 1
                if self.old_prices[1] <= self.old_prices[0]:
                    self.downtrend_count -= 1
                self.old_prices.popleft()
            # simply Naive strategy: buy if we're on an uptrend,
            # sell if we're on a downtrend
            if self.uptrend_count / len(self.old_prices) > self.threshold:
                order = Order(buy=True, price=price + self.price_inc,
                              qty=self.qty, identifier=len(self.orders))
            if self.downtrend_count / len(self.old_prices) > self.threshold:
                order = Order(sell=True, price=price - self.price_inc,
                              qty=self.qty, identifier=len(self.orders))
        self.old_prices.append(price)
        return order
