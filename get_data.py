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
        links.extend([listing_link(l) for l in ls])
        index += 1
    return list(set(links))

def listing_link(listing):
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

def address_to_lat_long(street_address, city):
    address = street_address.split(',')[0] + ', ' + city + ', Stockholm'
    url     = f'https://api.opencagedata.com/geocode/v1/json?q={address}&key=d0fdad792afd495ca1dab0282d9c989f'
    try:
        resp = requests.get(url, headers={'User-Agent': 'Agent'}).json()
        lat  = (resp['results'][0]['bounds']['northeast']['lat'] +
                resp['results'][0]['bounds']['southwest']['lat']) / 2
        lon  = (resp['results'][0]['bounds']['northeast']['lng'] +
                resp['results'][0]['bounds']['southwest']['lng']) / 2
    except Exception as e:
        print(f'failed to find {address}: {e}')
        return None, None
    return lat, lon

def main(search_url, results_outfile, prev_file=None):
    if prev_file:
        df = pd.read_csv(prev_file)
    else:
        df = pd.DataFrame({'link':[]})
    listing_urls = extract_listing_links_from_search_results(search_url)
    for listing_url in listing_urls:
        if listing_url in df.link.values:
            print(f'skipping {listing_url} since already retrieved')
            continue
        try:
            listing_json = json_from_full_listing(listing_url)
            lat, lon     = address_to_lat_long(listing_json['street_address'],
                                               listing_json['location'])
            listing_json['lat'] = lat
            listing_json['lon'] = lon
            df           = df.append(listing_json, ignore_index=True)
        except Exception as e:
            print(e)
            continue
    df.to_csv(results_outfile, index=False)
    return df

if __name__ == '__main__':
    search_url      = sys.argv[1]
    prev_file       = sys.argv[2]
    results_outfile = sys.argv[3]
    main(search_url, prev_file, results_outfile)
