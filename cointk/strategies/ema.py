from .core import Strategy
from ..order import Order
from collections import deque
import numpy as np


class EMAPriceCrossover(Strategy):
    '''
        We calculate the moving average of the stock, and buy if 
        current price is significantly higher and sell if it's significantly lower
        than the moving average. (Price Crossover)

        See for example http://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp
    '''

    def __init__(self, ma_length=100, qty=0.1, decision='increasing', gap_threshold=0.001, trend_threshold=10, verbose=0):
        '''
            If decision == 'increasing', then we will buy (amount = qty) once the price line
            crosses above the EMA and that gap keep increasing (similarly for selling)

            If decision == 'once', then we'll only buy up to (amount = qty) once every time
            crossover happens


            qty is the buying/selling limit at any given time. Set to -1 for inf
        
            trend_threshold is the min length a price crossover must last in order to be considered a "trend" and not fluxations

            gap_threshold is a fraction for how much above the price must the gap be to be considered a cross-over
        '''
        super().__init__()
        self.ma_length = ma_length  # length of Moving Average we care about
        self.alpha = 1/((ma_length+1)/2)  # alpha param in exponential MA
        # (1 - (1-self.alpha)**self.ma_length)/self.alpha is the sum of 1 + (1-alpha) + (1-alpha)^2 + ... + (1-alpha)^(n-1)
        self.weight_sum = sum((1-self.alpha)**i for i in range(self.ma_length))

        if verbose:
            print('alpha: {}, weight_sum: {}'.format(self.alpha, self.weight_sum))

        self.old_prices = deque()
        if qty == -1:
            self.qty = np.inf
        else:
            self.qty = qty
        self.decision = decision
        self.verbose = verbose
        self.identifier = 0
        self.trend_threshold = trend_threshold
        self.gap_threshold = gap_threshold
        self.emas = deque()
        self.last_gap = 0  # diff between last price & last EMA; used to track the price gaps for (decision = 'increasing')
        self.current_state = 0  # positive: increasing; negative: decreasing


    def gen_order(self, ts, price, qty, funds, balance):
        
        order = None
        qty = min(qty, self.qty)
        
        if len(self.old_prices) < self.ma_length:
            pass
            

        # len(self.old_prices) == self.ma_length
        elif len(self.emas) == 0:  # we've had the first ma_length data entries
            self.emas.append(sum(self.old_prices[-1-i] * (1-self.alpha)**i for i in range(self.ma_length)) / self.weight_sum) # get ewma for the first time
            
            if self.verbose > 1:
                print('Init EMA: ', self.emas)
                print('prices: ', self.old_prices)

        else:
            # calculate new EMA
            # we first "unadjust" the weighted sum (by scaling from 1 back to the sum of the weights),
            # then we subtract the "expired" price term, shift the weights, and add in the new price term
            ema = ((self.emas[-1] * self.weight_sum - self.old_prices[0] * (1-self.alpha)**(self.ma_length-1))
                * (1-self.alpha) + price) / self.weight_sum

            if self.verbose > 1: 
                if self.verbose > 3 or ts % 1000 == 0:
                    print('ema: ', ema)


            # switching into increasing from decreasing (crossover)
            if self.emas[-1] < self.old_prices[-1] and ema - price >= self.gap_threshold*(ema):
                # if self.verbose > 1:
                #     print("crossing over: ema: {}, price: {}".format(ema, price))

                if self.decision == 'increasing':
                    new_gap = ema - price
                    
                    order = Order(sell=True, price=price,
                              qty=self.qty, identifier=self.identifier)
                        
                    self.identifier += 1
                    self.last_gap = new_gap
                    self.current_state += 1
        
                else:  # just order once
                    order = Order(sell=True, price=price,
                              qty=self.qty, identifier=self.identifier)
            
            # already increasing
            elif self.current_state >= self.trend_threshold and self.decision == 'increasing':
                new_gap = ema - price
                if new_gap <= self.last_gap:  # buy as long as the price gap is increasing
                    order = Order(sell=True, price=price,
                          qty=self.qty, identifier=self.identifier)
                    
                    self.identifier += 1
                    self.last_gap = new_gap
                else:
                    self.last_gap = 0
                    self.current_state = 0      


            # selling
            elif self.emas[-1] > self.old_prices[-1] and price - ema >= self.gap_threshold*(ema):
                if self.verbose > 1:
                    print("crossing over: ema: {}, price: {}".format(ema, price))


                if self.decision == 'increasing':
                    new_gap = price - ema
                    
                    order = Order(buy=True, price=price,
                                  qty=self.qty, identifier=self.identifier)
                    self.identifier += 1
                    self.last_gap = new_gap
                    self.current_state -= 1

                else:
                    order = Order(buy=True, price=price,
                              qty=self.qty, identifier=self.identifier)

            elif self.current_state <= -self.trend_threshold and self.decision == 'increasing':
                new_gap = price - ema
                if new_gap >= self.last_gap:  # buy as long as the price gap is increasing
                    order = Order(buy=True, price=price,
                              qty=self.qty, identifier=self.identifier)
                    self.identifier += 1
                    self.last_gap = new_gap
                else:
                    self.last_gap = 0
                    self.current_state = 0
                        

            self.emas.append(ema)
            self.old_prices.popleft()

           
           

        self.old_prices.append(price)
        return order



    def get_emas(self):
        return self.emas
