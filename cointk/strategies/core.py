class Strategy(object):
    '''
        A general strategy framework for deciding when and how much to buy/sell

    '''
    def __init__(self):
        self.orders = []

    def init_backtest(self, funds, balance, worth):
        self.intial_funds = funds
        self.initial_balance = balance
        self.initial_worth = worth

    def evaluate(self, ts, price, qty, funds, balance):
        order = self.gen_order(ts, price, qty, funds, balance)
        if order:
            self.orders.append(order)
        return order

    def fill_order(self, idx, price, qty):
        self.orders[idx].fill(price, qty)

    def reject_order(self, idx):
        self.orders[idx].reject()

    def additional_plots(self):
        return []
