from random import random
from plotly.offline import plot
import plotly.graph_objs as go
from .data import load_data, subarray_with_stride, to_datetimes


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
    data = resolve_data(data, data_fnm, data_name, val, test)
    funds = initial_funds
    fund_history = [funds]
    balance = initial_balance
    balance_history = [balance]
    initial_worth = initial_funds + initial_balance * data[0][1]
    worth = initial_worth
    worth_history = [worth]
    ts_history = [data[0][0]]
    for i, (ts, price, qty) in enumerate(data[:-1]):
        next_ts, next_price, next_qty = data[i+1]
        order = strategy.evaluate(ts, price, qty, funds, balance)
        if order is None:
            continue
        if random() > fill_prob:
            strategy.reject_order(order.identifier)
            continue
        if order.buy:
            if not order.price >= next_price:
                strategy.reject_order(order.identifier)
                continue
            else:
                filled_qty = min(order.qty, next_qty)
                filled_price = next_price
                if filled_price * filled_qty > funds:
                    strategy.reject_order(order.identifier)
                    continue
                fund_delta = -filled_price * filled_qty
                balance_delta = filled_qty
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
        strategy.fill_order(order.identifier, filled_price, filled_qty)
        funds -= filled_price * filled_qty * fee
        funds += fund_delta
        balance += balance_delta
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
