import json
import pandas as pd
import random
import re
import requests
import sys
import time

from bs4 import BeautifulSoup

def get_all_sold(area_id,
                 max_sold_price=5000000,
                 rooms=[2,3,4],
                 object_type='Lägenhet',
                 after_date='2020-01-01',
                 start_page=1):
    url     = f'https://booli.se/slutpriser/{area_id}.json'
    params  = {'maxSoldPrice': max_sold_price,
               'minSoldDate': after_date,
               'rooms': ','.join(map(str, rooms)),
               'objectType': object_type,
               'page': start_page}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0'}
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
        time.sleep(1 + random.random() * 5)
    return results


def main(area_id, outfile):
    results = get_all_sold(area_id)
    df = pd.json_normalize(results, sep='_')
    df.to_csv(outfile, index=False)
    return df

if __name__ == '__main__':
    area_id = sys.argv[1]
    outfile = sys.argv[2]
    main(area_id, outfile)
