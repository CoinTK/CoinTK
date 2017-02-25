from .core import Strategy
from ..order import Order
from collections import deque


class NaiveStrategy(Strategy):
    '''
        Very basic strategy: buy if we're on a rising price trend, sell if we've been losing money

        This is just to provide a 'baseline' to test the performance of our smarter algorithms
    '''
    def __init__(self, n_prices=10, qty=0.01, threshold=0.8, price_inc=0.1):
        super().__init__()
        self.n_prices = n_prices
        self.old_prices = deque(maxlen=n_prices)
        self.qty = qty
        self.threshold = threshold
        self.price_inc = price_inc

    def gen_order(self, ts, price, qty, funds, balance):
        order = None
        if len(self.old_prices) == self.n_prices:
            # amount of days the price increased
            uptrend = [self.old_prices[i] >= self.old_prices[i-1]
                       for i in range(1, self.n_prices)].count(True)
            uptrend /= (self.n_prices - 1)
            downtrend = [self.old_prices[i] <= self.old_prices[i-1]
                         for i in range(1, self.n_prices)].count(True)
            downtrend /= (self.n_prices - 1)
            # simply Naive strategy: buy if we're on an uptrend, sell if we're on a downtrend
            if uptrend > self.threshold:
                order = Order(buy=True, price=price + self.price_inc,
                              qty=self.qty, identifier=len(self.orders))
            if downtrend > self.threshold:
                order = Order(sell=True, price=price - self.price_inc,
                              qty=self.qty, identifier=len(self.orders))
        self.old_prices.append(price)
        return order
