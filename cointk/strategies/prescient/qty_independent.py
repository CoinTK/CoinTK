from .core import PrescientStrategy
from ...order import OrderSpec


class QtyIndependent(PrescientStrategy):
    def __init__(self, qty=0.1):
        super().__init__()
        # a spike is the top of a peak or the bottom of a valley
        self.spikes = []  # (idx, price)
        self.runs = []  # (start_idx, start_price, up?)
        self.run_idx = 0
        self.qty = qty

    def init_pretest(self, fee):
        super().init_pretest(fee)
        self.run_idx = 0

    def read_data(self, tss, prices, qtys):
        super().read_data(tss, prices, qtys)
        uprun = self.prices[1] > self.prices[0]
        downrun = not uprun
        for i, price in enumerate(self.prices[:-1]):
            if uprun and price > self.prices[i+1]:
                uprun = False
                downrun = True
                self.spikes.append((i, price))
            elif downrun and price < self.prices[i+1]:
                downrun = False
                uprun = True
                self.spikes.append((i, price))

        # pprint(self.spikes)

        prev_price = self.spikes[0][1]
        prev_idx = 0
        for idx, price in self.spikes:
            if price > prev_price:
                if (price - prev_price) / prev_price > self.fee:
                    self.runs.append((prev_idx, prev_price, True))  # uprun
                    prev_price = price
                    prev_idx = idx
            elif price < prev_price:
                if (prev_price - price) / prev_price > self.fee:
                    self.runs.append((prev_idx, prev_price, False))  # downrun
                    prev_price = price
                    prev_idx = idx

    def prevaluate(self, idx, ts, price, qty):
        if self.run_idx < len(self.runs):
            start_idx, start_price, run_up = self.runs[self.run_idx]
            if idx + 1 >= start_idx:
                spec = OrderSpec(buy=run_up, sell=not run_up,
                                 price=start_price, qty=self.qty)
                self.run_idx += 1
                return spec
        return OrderSpec(empty=True)
