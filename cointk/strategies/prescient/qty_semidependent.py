from .core import PrescientStrategy
from ...order import OrderSpec


class QtySemidependent(PrescientStrategy):
    def __init__(self, qty=0.1):
        super().__init__()
        self.spikes = []  # (idx, price)
        self.spike_idx = 0
        self.qty = qty

    def init_pretest(self, fee):
        super().init_pretest(fee)
        self.spike_idx = 0

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

    def prevaluate(self, idx, ts, price, qty):
        if self.spike_idx + 2 < len(self.spikes):
            end_idx, end_price = self.spikes[self.spike_idx+1]
            curr_price = self.prices[idx+1]
            if idx > end_idx:
                self.spike_idx += 1
                end_idx, end_price = self.spikes[self.spike_idx+1]
            if end_price > curr_price:
                if (end_price - curr_price) / curr_price > self.fee:
                    return OrderSpec(buy=True, price=curr_price, qty=self.qty)
            if curr_price > end_price:
                if (curr_price - end_price) / curr_price > self.fee:
                    return OrderSpec(sell=True, price=curr_price, qty=self.qty)
        return OrderSpec(empty=True)
