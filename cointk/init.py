from urllib.request import urlretrieve
import gzip
import os.path
from .data import csv_to_npz

coinbase_usd_url = 'http://api.bitcoincharts.com/v1/csv/coinbaseUSD.csv.gz'
data_dir = 'data'
coinbase_usd_fnm = os.path.join(data_dir, 'coinbaseUSD')
coinbase_usd_csv = coinbase_usd_fnm + '.csv'
coinbase_usd_npz = coinbase_usd_fnm + '.npz'
coinbase_usd_gz = coinbase_usd_csv + '.gz'

if not os.path.exists(coinbase_usd_npz):
    if not os.path.exists('data'):
        os.makedirs('data')

    if not os.path.exists(coinbase_usd_csv):
        print('=' * 50)
        print('Downloading coinabse-usd datset...')
        urlretrieve(coinbase_usd_url, coinbase_usd_gz)

        with gzip.open(coinbase_usd_gz, 'rb') as infile:
            with open(coinbase_usd_csv, 'wb') as outfile:
                for line in infile:
                    outfile.write(line)

    csv_to_npz(coinbase_usd_csv, coinbase_usd_npz)
