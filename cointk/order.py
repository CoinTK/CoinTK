class OrderSpec(object):
    def __init__(self, buy=False, sell=False, price=0, qty=0,
                 src_tuple=None, empty=False):
        if src_tuple is not None:
            self.buy, self.sell, self.price, self.qty, self.empty = src_tuple
        else:
            self.buy = buy
            self.sell = sell
            self.price = price
            self.qty = qty
            self.empty = empty

    def to_tuple(self):
        return (self.buy, self.sell, self.price, self.qty, self.empty)

    def __str__(self):
        if self.empty:
            return 'OrderSpec(None)'
        return 'OrderSpec({}, price={}, qty={})'.format(
            'buy' if self.buy else 'sell',
            self.price, self.qty)

    def __repr__(self):
        return self.__str__()


class Order(object):
    def __init__(self, buy=False, sell=False, price=0, qty=0, identifier=0,
                 spec=None, empty=False):
        if spec:
            self.buy = spec.buy
            self.sell = spec.sell
            self.price = spec.price
            self.qty = spec.qty
            self.empty = spec.empty
        else:
            self.buy = buy
            self.sell = sell
            self.price = price
            self.qty = qty
            self.empty = empty
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

    def gen_spec(self):
        return OrderSpec(self.buy, self.sell, self.price, self.qty)
