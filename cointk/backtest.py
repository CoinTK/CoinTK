from random import random
from plotly.offline import plot
import plotly.graph_objs as go
from .data import load_data, subarray_with_stride, to_datetimes

# read in the correct set of data
def resolve_data(data, fnm, name, val, test, train_prop=0.8, val_prop=0.1):
    if data is not None:
        return data
    train_data, val_data, test_data = load_data(fnm, name,
                                                train_prop, val_prop)
    if val:
        return val_data
    elif test:
        return test_data


def backtest(strategy, initial_funds=1000, initial_balance=0, fill_prob=0.5,
             fee=0.0025, data=None, data_fnm='data/coinbaseUSD.npz',
             data_name='data', val=True, test=False):
    data = resolve_data(data, data_fnm, data_name, val, test) # default to validation
    funds = initial_funds # US dollars
    fund_history = [funds]
    balance = initial_balance # bitcoin amounts
    balance_history = [balance]
    initial_worth = initial_funds + initial_balance * data[0][1]
    worth = initial_worth # total value converted to dollars
    worth_history = [worth]
    ts_history = [data[0][0]]

    # each tuple is the log of an actual transaction at timestamp ts for the listed price/qty
    # we don't have historical data on the "Order Book", so we can only infer what kind of order/sell strategy would have worked based on the actual transactions
    # namely, if we sell at a lower price or buy at a higher price for the same or less quantity, we should succeed
    for i, (ts, price, qty) in enumerate(data[:-1]):
        next_ts, next_price, next_qty = data[i+1]
        order = strategy.evaluate(ts, price, qty, funds, balance)
        if order is None:
            continue

        # in real markets there's a chance that your order won't succeed, say if someone beats you to buying;
        # so we use fill_prob to simulate that "fail chance"

        # this essentially estimates the chance that if we send the same next-historical-transaction, we'll get the deal first
        if random() > fill_prob:
            strategy.reject_order(order.identifier)
            continue

        # try to buy
        if order.buy:
            # we can only guarantee buying if our price is higher than the historical transacted price
            if not order.price >= next_price:
                strategy.reject_order(order.identifier)
                continue
            else:
                # we can only guarantee a quantity based on historical transactions
                filled_qty = min(order.qty, next_qty)
                filled_price = next_price
                if filled_price * filled_qty > funds:
                    strategy.reject_order(order.identifier)
                    continue
                fund_delta = -filled_price * filled_qty
                balance_delta = filled_qty
        
        # try to sell; same limitations apply as above
        if order.sell:
            if not order.price <= next_price:
                strategy.reject_order(order.identifier)
                continue
            else:
                filled_qty = min(order.qty, next_qty)
                filled_price = next_price
                if filled_qty > balance:
                    strategy.reject_order(order.identifier)
                    continue
                fund_delta = filled_price * filled_qty
                balance_delta = -filled_qty

        # if order succeeded:
        strategy.fill_order(order.identifier, filled_price, filled_qty)
        funds -= filled_price * filled_qty * fee # pay transaction fee
        funds += fund_delta
        balance += balance_delta

        # historical tracking of what our algorithm predicts
        fund_history.append(funds)
        balance_history.append(balance)
        ts_history.append(next_ts)
        worth = funds + balance * next_price
        worth_history.append(worth)

    print('=' * 50)
    print('Backtest summary:')
    print('Funds: {} -> {}'.format(initial_funds, funds))
    print('Balance: {} -> {}'.format(initial_balance, balance))
    print('Net worth: {} -> {}'.format(initial_worth, worth))
    buy_hold_worth = (initial_funds / data[0][1]
                      + initial_balance) * data[-1][1]
    print('Buy hold equivelent: {} -> {}'.format(initial_worth,
                                                 buy_hold_worth))

    plot_data = subarray_with_stride(data, 100)
    print(plot_data.shape)
    price_trace = go.Scatter(x=to_datetimes(plot_data[:, 0]),
                             y=plot_data[:, 1])
    worth_trace = go.Scatter(
        x=to_datetimes(ts_history),
        y=worth_history,
        yaxis='y2')
    traces = [price_trace, worth_trace]
    layout = go.Layout(
        title='Trading performance over time',
        yaxis=dict(
            title='BTC_USD Price'
        ),
        yaxis2=dict(
            title='Worth (USD)',
            side='right',
            overlaying='y'
        )
    )
    plot(go.Figure(data=traces, layout=layout))

    return dict(fund_history=fund_history,
                balance_history=balance_history,
                ts_history=ts_history,
                worth_history=worth_history)
