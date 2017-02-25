class Order(object):
    def __init__(self, buy=False, sell=False, price=0, qty=0, identifier=0):
        self.buy = buy
        self.sell = sell
        self.price = price
        self.qty = qty
        self.identifier = identifier
        self.processing = True
        self.filled = False
        self.filled_price = None
        self.filled_qty = None

    def fill(self, price, qty):
        self.processing = False
        self.filled = True
        self.filled_price = price
        self.filled_qty = qty

    def reject(self):
        self.processing = False
        self.filled = False
