class Strategy(object):
    def __init__(self):
        self.orders = []

    def evaluate(self, ts, price, qty, funds, balance):
        order = self.gen_order(ts, price, qty, funds, balance)
        if order:
            self.orders.append(order)
        return order

    def fill_order(self, idx, price, qty):
        self.orders[idx].fill(price, qty)

    def reject_order(self, idx):
        self.orders[idx].reject()
