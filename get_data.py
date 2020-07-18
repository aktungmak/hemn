import json
import pandas as pd
import re
import requests
import sys

from bs4 import BeautifulSoup

def extract_listing_links_from_search_results(search_url):
    index = 1
    links = []
    while True:
        print(f'trying {search_url % index}...')
        resp = requests.get(search_url % index)
        if resp.status_code != 200:
            print(f'stopping extraction due to status code {resp.status_code}')
            break
        soup = BeautifulSoup(resp.text, 'html.parser')
        ls = soup.find_all('div', {'class': 'sold-property-listing'})
        print(f'got {len(ls)} results from page {index}')
        if len(ls) == 0:
            print('stopping extraction due to empty results page')
            break
        links.extend([get_listing_link(l) for l in ls])
        index += 1
    return links

def get_listing_link(listing):
    return listing.find('a').attrs['href']

def json_from_full_listing(listing_url):
    print(f'fetching {listing_url}...')
    resp    = requests.get(listing_url)
    soup    = BeautifulSoup(resp.text, 'html.parser')
    script  = [s for s in soup.body('script') if s.string is not None and 'dataLayer' in s.string][0]
    match   = re.search('dataLayer = (.*);', script.string)
    jsonstr = match.groups()[0]
    dicts   = json.loads(jsonstr)
    listing = dicts[-1]['sold_property']
    listing['link'] = listing_url
    return pd.json_normalize(listing).to_dict(orient='records')[0]

if __name__ == '__main__':
    search_url   = sys.argv[1]
    urls_out     = sys.argv[2]
    results_out  = sys.argv[3]
    listing_urls = extract_listing_links_from_search_results(search_url)
    with open(urls_out, 'w') as f:
        f.write('\n'.join(listing_urls))

    results = []
    for listing_url in listing_urls:
        try:
            results.append(json_from_full_listing(listing_url))
        except Exception as e:
            print(e)
            continue
    df = pd.DataFrame(results)
    df.to_csv(results_out, index=False)
