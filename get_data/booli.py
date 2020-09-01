import json
import pandas as pd
import random
import re
import requests
import sys
import time

from bs4 import BeautifulSoup

def get_all_sold_in_area(area_id, object_type='Lägenhet'):
    host = 'https://booli.se'
    page = 1
    results = []
    while True:
        url  = f'/slutpriser/{area_id}.json?objectType={object_type}&page={page}'
        print(f'fetching {url}...')
        resp = requests.get(host + url, headers={'User-Agent': 'Agent'})
        if resp.status_code != 200:
            print(f'stopping extraction due to status code {resp.status_code}')
            break
        try:
            body = resp.json()
            results.extend(body['soldProperties'])
        except KeyError:
            break
        page += 1
        time.sleep(random.randint(2, 7))
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
