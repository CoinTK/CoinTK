from .core import Strategy
from ..order import Order
from collections import deque
import numpy as np
from ..data import to_datetimes, subarray_with_stride


class EMAPriceCrossover(Strategy):
    '''
        We calculate the exponential moving average of the stock, and buy if
        current price is significantly higher and sell if it's significantly
        lower than the moving average. (Price Crossover)

        More information:
        http://www.investopedia.com/articles/active-trading/052014/ \
        how-use-moving-average-buy-stocks.asp
    '''

    def __init__(self, ma_length=100, qty=0.1, decision_logic='follow_trend',
                 gap_threshold=0.001, trend_threshold=10, verbose=0):
        '''
            If decision_logic == 'follow_trend', then we will 
             continuously buy (amount = qty) once the crossover
             is shown to last and the gap
             between the two keep increasing (similarly for selling).

            If decision_logic == 'order_once', then we'll buy up to (amount = qty)
             every time crossover happens, regardless of how long the price
             stays above the EMA or how big the crossover is

            qty is the self-set buying/selling limit at any given time.
            Set to -1 for inf (so the only limitation is on the market)



            The following are only useful for decision_logic == 'follow_trend':

                trend_threshold is the min length a price crossover must last in
                 order to be considered a "trend" and not random fluxations.
                 Set to zero if we want to buy AS SOON AS crossover happens (not recommended)

                gap_threshold is a fraction determining the minimum price gap
                 to be considered a cross-over, again to lower fluxations

                Together, these two parameters make it so the algorithm only considers
                 price crossovers when it's a lasting and growing trend
                
                 e.g. once the price rises above the EMA, if it keep jumping up ==> buy

        '''

        super().__init__()
        self.ma_length = ma_length  # length of Moving Average we care about
          
        # alpha param in exponential MA
        # this determines how much we care about past prices
        self.alpha = 1/((ma_length+1)/2)

        # sum of the weights, to be adjusted to 1
        self.weight_sum = sum((1-self.alpha)**i for i in range(self.ma_length))

        # if verbose:
        #     print('alpha: {}, weight_sum: {}'.format(self.alpha,
        #                                              self.weight_sum))

        self.prices = deque()
        if qty == -1:
            self.qty = np.inf
        else:
            self.qty = qty
        self.decision_logic = decision_logic
        self.verbose = verbose
        self.identifier = 0
        self.trend_threshold = trend_threshold
        self.gap_threshold = gap_threshold
        self.emas = deque()
        self.ema_tss = deque()  # timestamp for EMAs, used for graphing

        # absolute value of the diff between price & EMA
        # used to track the price gaps for (decision_logic = 'follow_trend')
        self.last_gap = 0
        self.trend_length = 0  # positive => price < EMA; negative => price > EMA

                                # Its value tracks how long the gap has been growing
                                #  since the price crossover first happened

                                # e.g. trend_length = 4 means that 4 data points ago 
                                #  the price fell below the EMA, and each day since
                                #  the gap has been increasing, so we should consider selling

        self.initial_price = None  # used for graphing



    def gen_order(self, ts, price, qty, funds, balance):

        if self.initial_price is None:
            self.initial_price = price

        order = None
        qty = min(qty, self.qty)  # maximum amount we can buy/sell

        if len(self.prices) < self.ma_length:
            pass

        elif len(self.emas) == 0:  # we've had the first ma_length data entries
            # so we can calculate ema for the first time
            self.emas.append(sum(
                self.prices[-1-i] * (1-self.alpha)**i
                for i in range(self.ma_length))
                / self.weight_sum)
            
            self.ema_tss.append(ts)

            if self.verbose > 1:
                print("Inititing EMA...")
                # print('Init EMA: ', self.emas)
                # print('prices: ', self.prices)

        else:
            # calculate new EMA
            # we first "unadjust" the weighted sum (by scaling from 1
            # back to the sum of the weights),
            # then we subtract the "expired" price term, shift the weights,
            # and add in the new price term
            ema = ((self.emas[-1] * self.weight_sum -
                    self.prices[0] * (1-self.alpha)**(self.ma_length-1))
                    * (1-self.alpha) + price) / self.weight_sum

            if self.verbose > 2:
                if self.verbose > 4 or ts % 1000 == 0:
                    print('ema: ', ema)



            # follow_trend
            # first, we figure out what trend we're in (i.e. if a recent crossover just happened)
            if self.decision_logic == 'follow_trend':
                
                # price switching from above EMA to below EMA, with a gap > gap_threshhold
                #  (crossover, signally an downtrend)
                if self.emas[-1] < self.prices[-1] and \
                   ema - price >= self.gap_threshold * (ema):

                    if self.verbose > 1:
                        print("Price crossing from above to below: ema: {} -> {}, price: {} -> {}, \
                                gap_threshold: {}"
                              .format(self.emas[-1], ema, self.prices[-1], price, 
                                      self.gap_threshold * (ema)))

                    new_gap = ema - price

                    # don't place an order yet,
                    # as we need to wait trend_threshold data points

                    if self.trend_threshold == 0:
                        order = Order(sell=True, price=price,
                                     qty=self.qty, identifier=self.identifier)
                        self.identifier += 1
       
                    self.last_gap = new_gap
                    self.trend_length += 1

          
                # price switching from below EMA to above
                #  (crossover, signally an uptrend)
                elif (self.emas[-1] > self.prices[-1] and
                      price - ema >= self.gap_threshold*(ema)):

                    if self.verbose > 1:
                        print("crossing over: ema: {}, price: {}"
                              .format(ema, price))

                    new_gap = price - ema

                    if self.trend_threshold == 0:
                        order = Order(buy=True, price=price,
                                      qty=self.qty, identifier=self.identifier)
                        self.identifier += 1

                    self.last_gap = new_gap
                    self.trend_length -= 1

                    
                # the previous two cases are for detecting crossover

                # now let's track the length of the trend, to see if it's consistent enough
                #  to buy/sell



                # price is currently below EMA and we're on a downward trend
                # let's see if it continues
                elif self.trend_length > 0:
                    if self.verbose > 1:
                        print("On a downtrend...")

                    new_gap = ema - price
                    # the downtrend continues as long as the price gap is increasing
                    if new_gap >= self.last_gap:

                        if self.verbose > 1:
                            print(" gap is increasing: {} -> {}".format(
                                        self.last_gap, new_gap))


                        # if the trend length is long enough, we start selling
                        if self.trend_length >= self.trend_threshold:
                            order = Order(sell=True, price=price,
                                          qty=self.qty, identifier=self.identifier)
                            self.identifier += 1

                        self.trend_length += 1
                        self.last_gap = new_gap
                    else:  # trend stopped; reset

                        if self.verbose > 1:
                            print("Downtrend stopped (gap: {})".format(new_gap))


                        self.last_gap = 0
                        self.trend_length = 0



                # the price is already above EMA and we're on an upward trend
                # let's see if it continues
                elif self.trend_length < 0:

                    new_gap = price - ema
                    # the uptrend continues as long as the price gap is increasing
                    if new_gap >= self.last_gap:

                        if self.trend_length <= -self.trend_threshold:
                            order = Order(buy=True, price=price,
                                          qty=self.qty, identifier=self.identifier)
                            self.identifier += 1

                        self.trend_length -= 1
                        self.last_gap = new_gap
                    else:  # reset the trend
                        self.last_gap = 0
                        self.trend_length = 0



            # order_once
            # we only need to check for price crossovers

            elif self.decision_logic == 'order_once':

                # price drops from above EMA to below EMA
                if self.emas[-1] < self.prices[-1] and \
                   ema - price >= self.gap_threshold * (ema):

                    order = Order(sell=True, price=price,
                                  qty=self.qty, identifier=self.identifier)

                    self.identifier += 1

                # price rises from below EMA to above
                elif (self.emas[-1] > self.prices[-1] and
                   price - ema >= self.gap_threshold*(ema)):

                    order = Order(buy=True, price=price,
                                  qty=self.qty, identifier=self.identifier)
                    self.identifier += 1


            # update ema/prices

            self.emas.append(ema)
            self.ema_tss.append(ts)
            self.prices.popleft()

        self.prices.append(price)
        return order



    def additional_plots(self, plot_freq=10000, plot_args={}):
        ema = subarray_with_stride(self.emas, plot_freq)
        tss = to_datetimes(subarray_with_stride(self.ema_tss, plot_freq))
        return [{'x': tss,
                 'y': plot_args.setdefault('initial_funds', 1000) * ema / self.initial_price,
                 'name': 'EMA Price (scaled)'}]
