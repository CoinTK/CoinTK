import numpy as np
import csv
from datetime import datetime


def to_datetimes(array):
    return [datetime.utcfromtimestamp(x) for x in array]


def from_datetimes(array):
    return [x.timestamp() for x in array]


def subarray_with_stride(array, stride):
    return np.asarray([array[i] for i in range(0, len(array), stride)])


def load_data(fnm, name='data', train_prop=0.8,
              val_prop=0.1):
    data = np.load(fnm)[name]
    train_idx = int(len(data) * train_prop)
    train_data = data[:train_idx]
    val_idx = int(len(data) * (train_prop + val_prop))
    val_data = data[train_idx:val_idx]
    test_data = data[val_idx:]
    return train_data, val_data, test_data


def save_data(data, fnm, name='data'):
    np.savez(fnm, **{name: data})


def csv_to_npz(csv_fnm, npz_fnm, name='data'):
    with open(csv_fnm, 'r') as f:
        reader = csv.reader(f)
        data = np.zeros((sum(1 for row in reader), 3), dtype='float32')
        print(data.shape)
        f.seek(0)
        for i, row in enumerate(reader):
            data[i, :] = int(row[0]), float(row[1]), float(row[2])
    np.savez(npz_fnm, **{name: data})


def load_coinbase_usd():
    return load_data('data/coinbaseUSD.npz', 'data')
