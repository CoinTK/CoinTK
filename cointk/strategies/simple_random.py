from .core import Strategy
from ..order import Order
from collections import deque
import random


class RandomStrategy(Strategy):
    '''
        Random!!
    '''
    def __init__(self, p_buy=0.1, p_sell=0.1, seed=None, randomize_qty=''):
        '''
            randomize_qty = 'Linear' if you want to choose a random amount 
            between (0, qty) every time we buy or sell

            Otherwise it's assumed we buy/sell the maximum amount possible
        '''
        super().__init__()
        self.p_buy = p_buy
        self.p_sell = p_sell
        self.identifier = -1
        self.randomize_qty = randomize_qty

        random.seed(seed)
        


    def gen_order(self, ts, price, qty, funds, balance):
        '''
        randomly buy or sell based on a random number
        '''
        r = random.random()

        if r < self.p_buy + self.p_sell:
            if self.randomize_qty == 'linear':
                qty *= random.random()

            self.identifier += 1
            if r < self.p_buy:
                return Order(buy=True, price=price,
                              qty=qty, identifier=self.identifier)
            else:
                return Order(sell=True, price=price,
                              qty=qty, identifier=self.identifier)
        else:
            return None
