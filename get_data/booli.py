import json
import pandas as pd
import random
import re
import requests
import sys
import time

from bs4 import BeautifulSoup

def get_all_sold(area_id,
                 max_sold_price=6000000,
                 rooms=[2,3,4],
                 object_type='Lägenhet',
                 start_page=1):
    url     = f'https://booli.se/slutpriser/{area_id}.json'
    params  = {'maxSoldPrice': max_sold_price,
               'rooms': ','.join(map(str, rooms)),
               'objectType': object_type,
               'page': start_page}
    headers = {'User-Agent': 'Agent'}
    results = []
    while True:
        print(f'fetching page {params["page"]}...')
        resp = requests.get(url, params=params, headers=headers)
        if resp.status_code != 200:
            print(f'stopping extraction due to status code {resp.status_code}')
            break
        try:
            body = resp.json()
            results.extend(body['soldProperties'])
        except KeyError:
            break
        params['page'] += 1
        time.sleep(random.random() * 2)
    return results


def main(area_id, results_outfile, prev_file=None):
    if prev_file:
        df = pd.read_csv(prev_file)
    else:
        df = pd.DataFrame()
    # TODO
    df.to_csv(results_outfile, index=False)
    return df

if __name__ == '__main__':
    area_id         = sys.argv[1]
    results_outfile = sys.argv[2]
    prev_file       = sys.argv[3]
    main(area_id, prev_file, results_outfile)
