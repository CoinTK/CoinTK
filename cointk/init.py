from urllib.request import urlretrieve
import gzip
import os.path
from .data import csv_to_npz

data_dir = 'data'
coinbase_usd_url = 'http://api.bitcoincharts.com/v1/csv/coinbaseUSD.csv.gz'
coinbase_usd_fnm = os.path.join(data_dir, 'coinbaseUSD.csv')
coinbase_usd_npz = os.path.splitext(coinbase_usd_fnm)[0] + '.npz'

if not os.path.exists(coinbase_usd_npz):
    if not os.path.exists('data'):
        os.makedirs('data')

    print('=' * 50)
    print('Downloading coinabse-usd datset...')
    urlretrieve(coinbase_usd_url, coinbase_usd_fnm + '.gz')

    with gzip.open(coinbase_usd_fnm, 'rb') as infile:
        with open(coinbase_usd_fnm, 'wb') as outfile:
            for line in infile:
                outfile.write(line)

    csv_to_npz(coinbase_usd_fnm, coinbase_usd_npz)
