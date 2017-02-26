from .core import Strategy
from ..order import Order
from collections import deque


class NaiveStrategyReverse(Strategy):
    '''
        REVERSE basic strategy: buy if we're on a rising price trend, sell if we've been losing money

        Essentially, we're betting against the market trend
    '''
    def __init__(self, n_prices=10, qty=0.01, threshold=0.8, price_inc=0.1):
        super().__init__()
        self.n_prices = n_prices
        self.old_prices = deque(maxlen=n_prices)
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
            
            # reverse Naive strategy: SELL if we're on an uptrend, BUY if we're on a downtrend
            if self.uptrend_count / len(self.old_prices) > self.threshold:
                order = Order(sell=True, price=price + self.price_inc,
                              qty=self.qty, identifier=len(self.orders))
            if self.downtrend_count / len(self.old_prices) > self.threshold:
                order = Order(buy=True, price=price - self.price_inc,
                              qty=self.qty, identifier=len(self.orders))
        self.old_prices.append(price)
        return order
